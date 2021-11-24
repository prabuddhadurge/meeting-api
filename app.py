""" Meetings API entry point """
from flask import Flask

from controller import API

APP = Flask(__name__)
API.init_app(APP)
APP.run(host='0.0.0.0', debug=True, port=5000)
