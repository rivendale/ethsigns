
from app import db
from .base import ModelOperations


association_table = db.Table('user_signs', db.Model.metadata,
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('metamask_user.id')),
                             db.Column('sign_id', db.Integer, db.ForeignKey('zodiacs.id'))
                             )


class MetamaskUser(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), index=True, unique=True)
    signs = db.relationship("Zodiacs",
                            secondary=association_table)

    def __repr__(self):
        return '<User {}>'.format(self.address)

    def __init__(self, user):
        """Constructor object
        Args:
            user (dict): user data to be saved in DB
        Returns:
            None"""
        self.address = user.get('address')
