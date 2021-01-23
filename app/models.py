from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, index=True, unique=True)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    bsign = db.Column(db.String(10))
    btype = db.Column(db.String(10))
    dsign = db.Column(db.String(10))
    dtype = db.Column(db.String(10))

    def __repr__(self):
        return '<Year {}>'.format(self.year)
