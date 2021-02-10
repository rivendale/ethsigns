from flask_login.utils import logout_user
from app import app, db
from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_user, login_required
from app.forms import LoginForm, ManageSigns, SignsForm, RegistrationForm
from app.models import Sign, User


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


@app.route('/', methods=['GET', 'POST'], defaults={"sym": " ", "typ": " "})
@app.route('/index', methods=['GET', 'POST'], defaults={"sym": " ", "typ": " "})
@app.route('/index/<typ>/<sym>/', methods=['GET', 'POST'])
def index(typ, sym):
    form = SignsForm()
    if form.validate_on_submit():
        chkmonth = form.birthmonth.data
        chkday = form.birthday.data
        typ = " "
        sym = " "
        checksign = Sign.query.filter_by(year=form.birthyear.data).first()
        # import pdb; pdb.set_trace()
        if checksign is not None:
            if (chkmonth > checksign.month):
                typ = checksign.dtype
                sym = checksign.dsign
            else:
                if (chkday >= checksign.day):
                    typ = checksign.dtype
                    sym = checksign.dsign
                else:
                    typ = checksign.btype
                    sym = checksign.bsign
        return redirect(url_for('index', typ=typ, sym=sym))

    return render_template('index.html', sym=sym, typ=typ, form=form, title='Home')


@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    form = ManageSigns()
    if form.validate_on_submit():
        checkfirst = Sign.query.filter_by(year=form.startyear.data).first()
        addsign = Sign(year=form.startyear.data, month=form.startmonth.data,
                       day=form.startday.data,
                       bsign=form.beforesign.data, btype=form.beforetype.data,
                       dsign=form.duringsign.data, dtype=form.duringtype.data)
        if checkfirst is None:
            db.session.add(addsign)
            db.session.commit()
            flash('Year added')
        else:
            Sign.query.filter_by(year=form.startyear.data).delete()
            db.session.commit()
            db.session.add(addsign)
            db.session.commit()
            flash('Updated entry')
        return redirect(url_for('manage'))
    signs = Sign.query.order_by(Sign.year.asc()).all()
    return render_template('manage.html', signs=signs, form=form, title='Data Management')


@app.route('/rmsym/<year>')
@login_required
def rmsym(year):
    checkfirst = Sign.query.filter_by(year=year).first()
    if checkfirst is None:
        flash('Not found or other error')
        return redirect(url_for('manage'))
    else:
        Sign.query.filter_by(year=year).delete()
        db.session.commit()
        flash('Deleted ')
        db.session.commit()
    return redirect(url_for('manage'))
