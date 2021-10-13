"""Module for zodiac schema"""
import ast

from flask_restplus import fields
from app.api import signs_ns
from app.api.helpers.signs import get_element
from .month_signs import month_signs_schema
from .day_signs import day_signs_schema
import json
import random


class GetElement(fields.Raw):
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
        element_data = self.elements.get(value.lower())
        data = {
            'positive_traits': random.sample(element_data.get('positive_traits'), 3),
            'negative_traits': random.sample(element_data.get('negative_traits'), 3),
        }
        return data


class FormatElement(fields.Raw):
    """
    Nested values Formatter
    """
    f = open('app/api/fixtures/elements.json',)
    elements = json.load(f)
    f.close()

    def format(self, value):
        """
        Return a formatted object
        Args:
            value (str): string object value
        Returns:
            (dict): formatted object
        """
        element_data = self.elements.get(value.lower())
        data = {
            'positive_traits': random.sample(element_data.get('positive_traits'), 3),
            'negative_traits': random.sample(element_data.get('negative_traits'), 3),
        }
        return data


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
    'element': fields.String(attribute=lambda x:  get_element(x.year)
                             if hasattr(x, "year") else x.element,
                             description='Sign element'),
    "element_attributes": FormatElement(attribute=lambda x:  get_element(x.year)
                                        if hasattr(x, "year") else x.element,
                                        description='Sign element attributes'),
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
    'minted': fields.Boolean(description='Sign minted'),
    'free': fields.Boolean(description='Sign free'),
    'month_animal': fields.Nested(month_signs_schema, skip_none=True,
                                  attribute="month", description="Sign's month details"),
    'day_animal': fields.Nested(day_signs_schema, skip_none=True,
                                attribute="day", description="Sign's day details"),
    'minting_fee': fields.Float(description='Minting fee'),
})
signs_schema = signs_ns.model('Zodiacs', signs_schema)


nft_schema = {
    'token_id': fields.Integer(description='Token ID'),
    'image_url': fields.String(description='NFT image url'),
    'token_url': fields.String(description='NFT url'),
    'gateway_token_url': fields.String(description='NFT gateway url'),
    'user_address': fields.String(description='NFT owner'),
    'metadata_url': fields.String(description='NFT metadata url'),
    'token_metadata': fields.Raw(attribute='token_metadata',
                                 description="Token Metadata"),
}
nft_schema = signs_ns.model('NFT', nft_schema)
paginated_schema = {
    'page': fields.Integer(description='Page'),
    'pages': fields.Integer(description='Pages'),
    'per_page': fields.Integer(description='Items Per page'),
    'total': fields.Integer(description='Token ID'),
    'items': fields.Nested(nft_schema, skip_none=True,
                           description="Tokens"),

}

paginated_schema = signs_ns.model('NFTs', paginated_schema)
