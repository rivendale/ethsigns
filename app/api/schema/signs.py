"""Module for zodiac schema"""
import ast

from app.api import signs_ns
from flask_restplus import fields


class FormatNested(fields.Raw):
    """
    Nested values Formatter
    """

    def format(self, value):
        """
        Return a formatted object
        Args:
            value (str): string object value
        Returns:
            (dict): formatted object
        """
        values = ast.literal_eval(value)
        return values


signs_schema = {
    'id': fields.Integer(description='The Sign unique identifier'),
    'name': fields.String(description='Sign unique name'),
    'image_url': fields.String(description='Sign Image Url'),
    'positive_traits': FormatNested(attribute='positive_traits', description="Sign's positive traits"),
    'negative_traits': FormatNested(attribute='negative_traits', description="Sign's negative traits"),
    'best_compatibility': FormatNested(attribute='best_compatibility', description="Sign's best compatibility"),
    'worst_compatibility': FormatNested(attribute='worst_compatibility', description="Sign's worst compatibility"),
    'report': FormatNested(attribute='report', description="Sign's report"),
}

signs_schema = signs_ns.model('Zodiacs', signs_schema)
