"""Module for zodiac schema"""
import ast

from flask_restplus import fields
from app.api import signs_ns
from .month_signs import month_signs_schema
from .day_signs import day_signs_schema


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


year_signs_schema = {
    'id': fields.Integer(description='The Sign identifier'),
    'name': fields.String(description='Sign name'),
    'description': fields.String(description='Sign description'),
    'element': fields.String(description='Sign element'),
    'force': fields.String(description='Sign force'),
    'image_url': fields.String(description='Sign Image Url'),
    'positive_traits': FormatNested(attribute='positive_traits',
                                    description="Sign's positive traits"),
    'negative_traits': FormatNested(attribute='negative_traits',
                                    description="Sign's negative traits"),
    'best_compatibility': FormatNested(attribute='best_compatibility',
                                       description="Sign's best compatibility"),
    'worst_compatibility': FormatNested(attribute='worst_compatibility',
                                        description="Sign's worst compatibility"),
    'report': FormatNested(attribute='report', description="Sign's report"),
}

signs_schema = year_signs_schema.copy()
year_signs_schema = signs_ns.model('Zodiacs', year_signs_schema)


signs_schema.update({
    'hash': fields.String(description='Sign Hash'),
    'month_animal': fields.Nested(month_signs_schema, skip_none=True,
                                  attribute="month", description="Sign's month details"),
    'day_animal': fields.Nested(day_signs_schema, skip_none=True,
                                attribute="day", description="Sign's day details"),
})
signs_schema = signs_ns.model('Zodiacs', signs_schema)
