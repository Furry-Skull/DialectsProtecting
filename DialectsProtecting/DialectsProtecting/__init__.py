"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import DialectsProtecting.Database
database = Database.Database()
currentUsername = None
currentPassword = None

import DialectsProtecting.views