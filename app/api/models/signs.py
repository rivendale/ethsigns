from app import db
from .base import ModelOperations


class Zodiacs(db.Model, ModelOperations):
    """
    Year zodiac sign model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, nullable=False)
    element = db.Column(db.String(60), index=True, nullable=False)
    force = db.Column(db.String(60), index=True, nullable=False)
    image_url = db.Column(db.String(250))
    base_index = db.Column(db.Integer, index=True, unique=True)
    positive_traits = db.Column(db.String(300), index=True)
    negative_traits = db.Column(db.String(300), index=True)
    best_compatibility = db.Column(db.String(300), index=True)
    worst_compatibility = db.Column(db.String(00), index=True)
    report = db.Column(db.String(4000), index=True)
    description = db.Column(db.String(250))

    def __init__(self, sign):
        """Constructor object
        Args:
            sign (dict): zodiac sign data to be saved in DB
        Returns:
            None"""
        self.name = sign.get('name')
        self.force = sign.get('force')
        self.element = sign.get('element')
        self.image_url = sign.get('image_url')
        self.base_index = sign.get('base_index')
        self.positive_traits = sign.get('positive_traits')
        self.negative_traits = sign.get('negative_traits')
        self.best_compatibility = sign.get('best_compatibility')
        self.worst_compatibility = sign.get('worst_compatibility')
        self.report = sign.get('report')
        self.description = sign.get('description')

    def __repr__(self):
        return '<Zodiac - {}>'.format(self.name)


class MonthSign(db.Model, ModelOperations):
    """
    Month zodiac sign model
    """
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, index=True,
                      nullable=False, unique=True)
    animal = db.Column(db.String(60), index=True, nullable=False)

    def __init__(self, sign):
        """Constructor object
        Args:
            sign (dict): zodiac sign data to be saved in DB
        Returns:
            None"""
        self.month = sign.get('month')
        self.animal = sign.get('animal')

    def __repr__(self):
        return '<MonthSign - {}>'.format(self.month)


class DaySign(db.Model, ModelOperations):
    """
    Day zodiac sign model
    """
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(60), index=True,
                    nullable=False, unique=True)
    animal = db.Column(db.String(60), index=True, nullable=False)

    def __init__(self, sign):
        """Constructor object
        Args:
            sign (dict): zodiac sign data to be saved in DB
        Returns:
            None"""
        self.day = sign.get('day')
        self.animal = sign.get('animal')

    def __repr__(self):
        return '<DaySign - {}>'.format(self.day)
