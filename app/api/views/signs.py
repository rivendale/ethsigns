"""Module for Zodiac resource"""
from app import api
from flask_restplus import Resource

from app.api.schema.signs import signs_schema
from app.api import signs_ns
from app.api.validators.validators import sign_validation
from app.api.models import Zodiacs
from app.api.helpers.constants import ZODIAC_ANIMALS


@api.route('/signs/')
class ZodiacResource(Resource):
    """Resource class for adding a zodiac sign"""

    @signs_ns.doc(description="create a new sign")
    @signs_ns.expect(sign_validation())
    @signs_ns.marshal_with(signs_schema, envelope='sign')
    def post(self):
        """
        Add a zodiac sign

        Raises:
            (ValidationError): Used to raise exception if validation during
            creation of a zodiac sign fails

        Returns:
            (tuple): Returns status, success message and relevant zodiac details
        """

        sign_data = sign_validation().parse_args(strict=True)
        sign_data['positive_traits'] = str(sign_data['positive_traits'])
        sign_data['negative_traits'] = str(sign_data['negative_traits'])
        sign_data['best_compatibility'] = str(sign_data['best_compatibility'])
        sign_data['worst_compatibility'] = str(sign_data['worst_compatibility'])
        sign_data['report'] = str(sign_data['report'])
        sign_data['base_index'] = ZODIAC_ANIMALS.get(
            sign_data.get("name", '').title())
        sign = Zodiacs(sign_data)
        sign.save()
        return sign, 201
