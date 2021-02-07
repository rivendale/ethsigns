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
