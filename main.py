"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os

import firebase_admin
from firebase_admin import db
from firebase import ref
from random import randrange
from models.FieldData import FieldData
from importances import getImportances
import time
from scoreFuncs import fieldScore, goalKeeperScore


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        id_param = json.loads(post_data.decode('utf-8'))
        logging.info("id of game to process:  {0}".format(id_param['id']))

        gameRef = db.reference("events/completeGames/{0}".format(id_param['id']))
        game = db.reference("events/completeGames/{0}".format(id_param['id'])).get()
        tracker = FieldData()
        tracker.appendGame(game)
        
        importances = getImportances()
        
        db.reference('/').update({ 'weights': importances })

        for ind, player in enumerate(game['starting']):
            if player['position'] != 'Вратарь':
                score = fieldScore(player['gameStats'], importances)
                print('player id score:', score)
                db.reference('players/{0}/scores'.format(player['id'])).update({game['id']: score})
                gameRef.child('starting').child(str(ind)).update({'score': score})
            else:
                score = goalKeeperScore(player['gameStats'], importances)            
                print('goalkeeper id score:', score)
                db.reference('players/{0}/scores'.format(player['id'])).update({game['id']: score})
                gameRef.child('starting').child(str(ind)).update({'score': score})

        self._set_response()
        self.wfile.write('importances'.encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    portino = os.getenv('PORT', default=8000)

    server_address = ('', int(portino))
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
