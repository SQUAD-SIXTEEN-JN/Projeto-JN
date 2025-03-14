import os
from dotenv import load_dotenv

import pyrebase

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "projectId": os.getenv("projectId"),
    "storageBucket": os.getenv("storageBucket"),
    "messagingSenderId": os.getenv("messagingSenderId"),
    "appId": os.getenv("appId"),
    "measurementId": os.getenv("measurementId"),
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()