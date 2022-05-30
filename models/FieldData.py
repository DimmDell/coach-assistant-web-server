import math

import pandas
from firebase_admin import db

class FieldData(object):
    """docstring"""

    def __init__(self):
        """Constructor"""
        (self.__assists, self.__goals, self.__missedPasses, self.__passes, self.__redCard, self.__rounds, self.__shots,
         self.__shotsOnTarget, self.__tackles, self.__timePlayed,
         self.__yellowCard, self.__saves, self.__conceded,) = (0, 0, 0, 0, False, 0, 0, 0, 0, 0, False, 0, 0)

    @property
    def saves(self):
        return self.__saves

    @saves.setter
    def saves(self, m):
        self.__saves = m

    @property
    def conceded(self):
        return self.__conceded

    @conceded.setter
    def conceded(self, m):
        self.__conceded = m

    @property
    def yellowCard(self):
        return self.__yellowCard

    @yellowCard.setter
    def yellowCard(self, m):
        self.__yellowCard = m

    @property
    def timePlayed(self):
        return self.__timePlayed

    @timePlayed.setter
    def timePlayed(self, m):
        self.__timePlayed = m

    @property
    def tackles(self):
        return self.__tackles

    @tackles.setter
    def tackles(self, m):
        self.__tackles = m

    @property
    def shotsOnTarget(self):
        return self.__shotsOnTarget

    @shotsOnTarget.setter
    def shotsOnTarget(self, m):
        self.__shotsOnTarget = m

    @property
    def shots(self):
        return self.__shots

    @shots.setter
    def shots(self, m):
        self.__shots = m

    @property
    def rounds(self):
        return self.__rounds

    @rounds.setter
    def rounds(self, m):
        self.__rounds = m

    @property
    def redCard(self):
        return self.__redCard

    @redCard.setter
    def redCard(self, m):
        self.__redCard = m

    @property
    def passes(self):
        return self.__passes

    @passes.setter
    def passes(self, m):
        self.__passes = m

    @property
    def missedPasses(self):
        return self.__missedPasses

    @missedPasses.setter
    def missedPasses(self, m):
        self.__missedPasses = m

    @property
    def goals(self):
        return self.__goals

    @goals.setter
    def goals(self, g):
        self.__goals = g

    @property
    def assists(self):
        return self.__assists

    @assists.setter
    def assists(self, a):
        self.__assists = a

    def processGame(self, game):
        starters = game['starting']
        subs = game['substitutions']
        ref = db.reference('/players').get()
        for ind, p in enumerate(starters + subs):
            if ref[p['id']]['position'] == 'Вратарь':
                self.conceded += int(p['gameStats']['conceded'])
                self.saves += int(p['gameStats']['saves'])
            self.assists += int(p['gameStats']['assists'])
            self.goals += int(p['gameStats']['goals'])
            self.missedPasses += int(p['gameStats']['missedPasses'])
            self.passes += int(p['gameStats']['passes'])
            self.redCard += 1 if p['gameStats']['redCard'] == 'true' else 0
            self.rounds += int(p['gameStats']['rounds'])
            self.shots += int(p['gameStats']['shots'])
            self.shotsOnTarget += int(p['gameStats']['shotsOnTarget'])
            self.tackles += int(p['gameStats']['tackles'])
            self.timePlayed += int(p['gameStats']['timePlayed']['minutes']) * 60
            self.yellowCard += 1 if p['gameStats']['yellowCard'] == 'true' else 0

    def getReport(self, gameID):
        res = 0
        if self.goals == self.conceded:
            res = 0
        elif self.goals < self.conceded:
            res = -1
        else:
            res = 1
        return {
            "gameID": gameID,
            "shots": self.shots,
            "conceded": self.conceded,
            "saves": self.saves,
            "shotsOnTarget": self.shotsOnTarget,
            "passes": self.passes,
            "missedPasses": self.missedPasses,
            "rounds": self.rounds,
            "tackles": self.tackles,
            "yellowCard": self.yellowCard,
            "redCard": self.redCard,
            "assists": self.assists,
            "goals": self.goals,
            "difference": self.goals - self.conceded,
            "result": res
        }

    def appendGame(self, game):
        self.processGame(game)
        rep = self.getReport(game['id'])
        df = pandas.DataFrame(data=rep, index=[0])
        print(df.to_dict('records')[0])
        db.reference('dictStats/{0}'.format(game['id'])).set(df.to_dict('records')[0])

