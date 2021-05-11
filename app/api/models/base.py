"""Module for generic model operations mixin."""
from app import db


class ModelOperations(object):
    """Mixin class with generic model operations."""

    def save(self):
        """
        Save a model instance
        """

        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        update entries
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        db.session.commit()

    def add_sign(self, sign):
        """
        update entries
        """
        self.signs.append(sign)
        db.session.commit()

    def remove_sign(self, sign):
        """
        update entries
        """
        self.signs.remove(sign)
        db.session.commit()
