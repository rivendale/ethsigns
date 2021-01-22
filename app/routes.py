from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import *
from datetime import datetime

@app.route('/',methods=['GET', 'POST'], defaults={"sym":"BLANK"})
@app.route('/index',methods=['GET', 'POST'], defaults={"sym":"BLANK"})
@app.route('/index/<sym>/', methods=['GET', 'POST'])
def index(sym):
    form = SignsForm()
    if form.validate_on_submit():
        chkmonth = form.birthmonth.data
        chkday = form.birthday.data
        chkyear = form.birthyear.data
        return redirect(url_for('index', sym=chkmonth))


    if sym == "BLANK":
        sym = " "

    return render_template('index.html', sym=sym,form=form,title='Home')
