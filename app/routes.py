from app import app, db
from flask import render_template, url_for, redirect, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, login_required
from app.forms import *
from app.models import *
from datetime import datetime

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    form = ManageSigns()

    if form.validate_on_submit():
        addsign = Sign(year=form.startyear.data, month=form.startmonth.data,day=form.startday.data, bsign=form.beforesign.data , btype=form.beforetype.data,dsign=form.duringsign.data,dtype=form.duringtype.data)
        db.session.add(addsign)
        db.session.commit()
        flash('Year added')
        return redirect(url_for('manage'))
    signs = Sign.query.order_by(Sign.year.asc()).all()
    return render_template('manage.html', signs=signs,form=form,title='Data Management')
