# encoding: utf-8

from flask import Flask
app = Flask(__name__)

from DialectsProtecting import manage
from DialectsProtecting import config