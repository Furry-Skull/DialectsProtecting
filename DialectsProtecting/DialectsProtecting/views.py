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
        'register.html',
    )

@app.route('/login', methods=(["GET","POST"]))
def login():
    if request.method == 'POST':
        form = request.form
        user = User(username=form['username'],email=form['email'],password=form['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(form)
    return render_template('/account/login.html')

@app.route('/register', methods=(["GET","POST"]))
def register():
    if request.method == 'POST':
        form = request.form
        user = User(username=form['username'],email=form['email'],password=form['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(form)
    return render_template('/account/register.html')