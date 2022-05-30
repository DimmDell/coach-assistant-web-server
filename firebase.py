import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('./some-file-name.json')

databaseURL = 'some-url.com'
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})

ref = db.reference("/")
