from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class SignsForm(FlaskForm):
    birthyear = IntegerField('Year', validators=[DataRequired()])
    birthmonth = IntegerField('Month', validators=[DataRequired()])
    birthday = IntegerField('Day', validators=[DataRequired()])
    submit = SubmitField('Submit')
