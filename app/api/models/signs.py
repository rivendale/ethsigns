from app import db
from .base import ModelOperations


class Zodiacs(db.Model, ModelOperations):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, nullable=False)
    image_url = db.Column(db.String(250))
    base_index = db.Column(db.Integer, index=True, unique=True)
    positive_traits = db.Column(db.String(500), index=True)
    negative_traits = db.Column(db.String(500), index=True)
    best_compatibility = db.Column(db.String(500), index=True)
    worst_compatibility = db.Column(db.String(500), index=True)
    report = db.Column(db.String(4000), index=True)

    def __init__(self, sign):
        """
        Constructor object
        Args:
            sign (dict): zodiac sign data to be saved in DB
        Returns:
            None
        """
        self.name = sign.get('name')
        self.image_url = sign.get('image_url')
        self.base_index = sign.get('base_index')
        self.positive_traits = sign.get('positive_traits')
        self.negative_traits = sign.get('negative_traits', '')
        self.best_compatibility = sign.get('best_compatibility', '')
        self.worst_compatibility = sign.get('worst_compatibility', '')
        self.report = sign.get('report', '')

    def __repr__(self):
        return '<Name {}>'.format(self.name)
