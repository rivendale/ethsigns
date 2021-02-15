"""Module for Zodiac resource"""
from app.api.helpers.signs import (check_existing_year_signs,
                                   return_not_found, date_validator,
                                   check_existing_month_signs)
from app import api
from flask_restplus import Resource

from app.api.schema import year_signs_schema
from app.api.schema import month_signs_schema
from app.api import signs_ns
from app.api.validators.validators import sign_validation, month_sign_validation
from app.api.models import Zodiacs, MonthSign
from app.api.helpers.constants import ZODIAC_ANIMALS


@api.route('/signs/year/')
class CreateListZodiacResource(Resource):
    """
    Resource to handle:
        - adding a zodiac sign
        - list zodiac signs
    """
    @signs_ns.doc(description="create a new sign")
    @signs_ns.expect(sign_validation())
    @signs_ns.marshal_with(year_signs_schema, envelope='sign')
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
        check_existing_year_signs(sign_data)
        sign_data['positive_traits'] = str(sign_data['positive_traits'])
        sign_data['negative_traits'] = str(sign_data['negative_traits'])
        sign_data['best_compatibility'] = str(sign_data['best_compatibility'])
        sign_data['worst_compatibility'] = str(sign_data['worst_compatibility'])
        sign_data['report'] = str(sign_data['report'])
        sign_data['base_index'] = ZODIAC_ANIMALS.get(sign_data.get("name", '').title())
        sign = Zodiacs(sign_data)
        sign.save()
        return sign, 201


@api.route('/signs/month/')
class CreateListMonthSignsResource(Resource):
    """
    Resource to handle:
        - adding a month's zodiac sign
        - list months zodiac signs
    """
    @signs_ns.doc(description="create a new month sign")
    @signs_ns.expect(month_sign_validation())
    @signs_ns.marshal_with(month_signs_schema, envelope='sign')
    def post(self):
        """
        Add a month's zodiac sign

        Returns:
            (tuple): Returns status and relevant zodiac details
        """
        sign_data = month_sign_validation().parse_args(strict=True)
        check_existing_month_signs(sign_data)
        sign = MonthSign(sign_data)
        sign.save()
        return sign, 201

    @signs_ns.doc(description="list month's signs")
    @signs_ns.marshal_with(month_signs_schema, envelope='signs')
    def get(self):
        """
        List months zodiac signs

        Returns:
            (tuple): Returns status and list of zodiac signs
        """

        signs = MonthSign.query.order_by(MonthSign.month.asc()).all()
        return signs, 200


@api.route('/signs/year/<int:sign_id>/')
class GetPatchDeleteZodiacResource(Resource):
    """
    Class to handle:
        - retrieving a single sign
        - updating a single sign
        - deleting a single sign
    """
    @signs_ns.doc(description="fetch specific sign using sign Id")
    @signs_ns.marshal_with(year_signs_schema, envelope='sign')
    def get(self, sign_id):
        """
        Function to retrieve a sign
        Args:
            sign_id (int): sign ID
        Returns:
            sign (obj): sign data
        """
        sign = Zodiacs.query.filter_by(
            id=sign_id).first()
        if not sign:
            return_not_found(signs_ns, 'sign')

        return sign


@api.route('/signs/query/')
class GetUserZodiacResource(Resource):
    """
    Class to handle:
        - retrieving a sign based on certain query parameters
    """
    @signs_ns.doc(description="fetch sign based on certain parameters",
                  params={"year": {
                      "description": "Year of birth",
                      "required": False,
                      "type": "int"
                  }, "month": {
                      "description": "Month of birth",
                      "required": False,
                      "type": "int"
                  }, "day": {
                      "description": "Day of birth",
                      "required": False,
                      "type": "int"
                  }})
    @date_validator
    @signs_ns.marshal_with(year_signs_schema, envelope='sign')
    def get(self, data, **kwargs):
        """
        Function to retrieve a sign
        Args:
            sign_id (int): sign ID
        Returns:
            sign (obj): sign data
        """
        year = data.get("year", '')
        base_year = 1948
        base_index = (year-base_year) % 12
        sign = Zodiacs.query.filter_by(
            base_index=base_index).first()
        return sign
