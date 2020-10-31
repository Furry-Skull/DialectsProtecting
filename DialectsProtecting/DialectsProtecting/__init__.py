"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import DialectsProtecting.views
import DialectsProtecting.Database