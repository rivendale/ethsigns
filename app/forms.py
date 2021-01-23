from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import *

class SignsForm(FlaskForm):
    birthyear = IntegerField('Year', validators=[DataRequired()])
    birthmonth = IntegerField('Month', validators=[DataRequired()])
    birthday = IntegerField('Day', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ManageSigns(FlaskForm):
    startyear = IntegerField('Year', validators=[DataRequired()])
    startmonth = IntegerField('Month', validators=[DataRequired()])
    startday = IntegerField('Day', validators=[DataRequired()])
    beforetype = StringField('Before Type', validators=[DataRequired()])
    beforesign = StringField('Before Sign', validators=[DataRequired()])
    duringtype = StringField('During Type', validators=[DataRequired()])
    duringsign = StringField('During Sign', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
