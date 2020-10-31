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
    if a.login(3,9)==2:
        print (2)
    elif a.login(3,3)==1:
        print (1)
    elif a.login(3,3)==0:
        print (0)
    return render_template(
        'index.html',
        projectName='DialectsProtecting',
    )