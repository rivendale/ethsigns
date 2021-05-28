
from app import db
from .base import ModelOperations


class SignHash(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    signhash = db.Column(db.String(500), index=True, unique=True)

    def __repr__(self):
        return '<SignHash {}>'.format(self.id)

    def __init__(self, signhash):
        """Constructor object
        Args:
            signhash (dict): signhash data to be saved in DB
        Returns:
            None"""
        self.signhash = signhash.get('sign_hash')


association_table = db.Table('user_sign_hashes', db.Model.metadata,
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('metamask_user.id')),
                             db.Column('sign_hash', db.Integer,
                                       db.ForeignKey('sign_hash.id'))
                             )


class MetamaskUser(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), index=True, unique=True)
    sign_hashes = db.relationship("SignHash",
                                  secondary=association_table)

    def __repr__(self):
        return '<MetamaskUser {}>'.format(self.address)

    def __init__(self, user):
        """Constructor object
        Args:
            user (dict): user data to be saved in DB
        Returns:
            None"""
        self.address = user.get('address')
