"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DialectsProtecting import app

@app.route('/')
@app.route('/home')
def home():
    #主页
    return render_template(
        'home.html',
    )