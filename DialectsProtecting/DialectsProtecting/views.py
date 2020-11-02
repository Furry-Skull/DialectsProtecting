from flask import render_template
from DialectsProtecting import app
from DialectsProtecting import Database

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'home.html',
        isLogin = False,
    )

#登录界面
@app.route('/login')
def loginPage():
    return render_template('/login.html')

#提交登录信息
@app.route('/form/login', methods=(["GET","POST"]))
def loginForm():
    if request.method == 'POST':
        form = request.form
        user = User(username=form['username'],email=form['email'],password=form['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(form)
    return render_template('/account/login.html')

#提交注册信息
@app.route('/form/register', methods=(["GET","POST"]))
def registerForm():
    if request.method == 'POST':
        form = request.form
        user = User(username=form['username'],email=form['email'],password=form['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(form)
    return render_template('/account/register.html')