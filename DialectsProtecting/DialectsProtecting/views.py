from flask import render_template
from DialectsProtecting import app
from DialectsProtecting import Database

@app.route('/')
@app.route('/home')
def home():
    a=Database.Database()
    if a.register(7,8)==0:
        print ("cnmd")
    #主页
    if a.login(7,8)==2:
        print (2)
    elif a.login(3,3)==1:
        print (1)
    elif a.login(3,3)==0:
        print (0)
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