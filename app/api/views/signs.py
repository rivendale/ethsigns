"""Module for Zodiac resource"""
from app.api.models.signs import NFT
from app import api, db
from app.api import signs_ns
from app.api.helpers.constants import ZODIAC_ANIMALS
from app.api.helpers.signs import (check_existing_month_signs,
                                   check_existing_user,
                                   check_existing_year_signs, date_validator,
                                   dict_hash, return_not_found)
from app.api.models import DaySign, MonthSign, User, Zodiacs
from app.api.models.users import SignHash
from app.api.schema import (day_signs_schema, month_signs_schema, signs_schema,
                            year_signs_schema, paginated_schema, nft_schema)
from app.api.validators.validators import (day_sign_validation,
                                           month_sign_update_validation,
                                           month_sign_validation,
                                           sign_validation)
from config import Config
from flask_restplus import Resource


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
        sign_data = {k: str(v) for k, v in sign_data.items()}

        sign_data['base_index'] = ZODIAC_ANIMALS.get(sign_data.get("name", '').title())
        sign = Zodiacs(sign_data)
        sign.save()
        return sign, 201

    @signs_ns.doc(description="list year's signs")
    @signs_ns.marshal_with(year_signs_schema, envelope='signs', as_list=True)
    def get(self):
        """
        List years zodiac signs

        Returns:
            (tuple): Returns status and list of zodiac signs
        """

        signs = Zodiacs.query.order_by(Zodiacs.base_index.asc()).all()
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

    @signs_ns.doc(description="update year sign")
    @signs_ns.expect(sign_validation(create=False))
    @signs_ns.marshal_with(year_signs_schema, envelope='sign')
    def patch(self, sign_id):
        """
        Update year zodiac sign

        Args:
            sign_id (int): year sign ID
        Returns:
            sign (obj): year sign data
        """
        sign_validation(create=False).parse_args(strict=True)
        sign_data = signs_ns.payload
        sign_data = {k: str(v) for k, v in sign_data.items()}
        sign = Zodiacs.query.filter_by(
            id=sign_id).first()
        if not sign:
            return_not_found(signs_ns, 'sign')
        sign.update(**sign_data)
        return sign, 200


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
                  }, "address": {
                      "description": "User address",
                      "required": False,
                      "type": "int"
                  }})
    @date_validator
    @signs_ns.marshal_with(signs_schema, envelope='sign')
    def get(self, data, **kwargs):
        """
        Function to retrieve a sign
        Args:
            sign_id (int): sign ID
        Returns:
            sign (obj): sign data
        """
        year = data.get("year", '')
        month = data.get("month", '')
        day = data.get("day", '')
        address = data.get("address", '')
        del data['address']
        month = MonthSign.query.filter_by(month=month).first()
        base_year = 1948
        base_index = (year-base_year) % 12
        sign = Zodiacs.query.filter_by(
            base_index=base_index).first()
        day = DaySign.query.filter_by(day=day).first()
        hash_data = dict_hash(data)
        minted = False
        if address:
            user = check_existing_user({'address': address})
            result = db.session.query(User.address, SignHash.signhash).filter(
                SignHash.signhash == hash_data).filter(
                    User.address == user.address).first()
            if result:
                minted = True

        setattr(sign, "month", month)
        setattr(sign, "day", day)
        setattr(sign, "hash", hash_data)
        setattr(sign, "minted", minted)
        setattr(sign, "minting_fee", Config.MINTING_FEE)
        return sign


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
    @signs_ns.marshal_with(month_signs_schema, envelope='signs', as_list=True)
    def get(self):
        """
        List months zodiac signs

        Returns:
            (tuple): Returns status and list of zodiac signs
        """

        signs = MonthSign.query.order_by(MonthSign.month.asc()).all()
        return signs, 200


@api.route('/signs/day/')
class CreateListdaySignsResource(Resource):
    """
    Resource to handle:
        - list days zodiac signs
    """

    @signs_ns.doc(description="list day's signs")
    @signs_ns.marshal_with(day_signs_schema, envelope='signs', as_list=True)
    def get(self):
        """
        List days zodiac signs

        Returns:
            (tuple): Returns status and list of zodiac signs
        """

        signs = DaySign.query.all()
        return signs, 200


@api.route('/signs/day/<int:sign_id>/')
class GetUpdateDaySignsResource(Resource):
    """
    Resource to handle:
        - get day zodiac sign
        - update day zodiac sign
    """

    @signs_ns.doc(description="get day sign")
    @signs_ns.marshal_with(day_signs_schema, envelope='sign')
    def get(self, sign_id):
        """
        Get days zodiac signs

        Args:
            sign_id (int): day sign ID
        Returns:
            sign (obj): day sign data
        """

        sign = DaySign.query.filter_by(
            id=sign_id).first()
        if not sign:
            return_not_found(signs_ns, 'sign')

        return sign, 200

    @signs_ns.doc(description="update day sign")
    @signs_ns.expect(day_sign_validation())
    @signs_ns.marshal_with(day_signs_schema, envelope='sign')
    def patch(self, sign_id):
        """
        Update day zodiac sign

        Args:
            sign_id (int): day sign ID
        Returns:
            sign (obj): day sign data
        """

        day_sign_validation().parse_args(strict=True)
        sign_data = signs_ns.payload
        sign = DaySign.query.filter_by(
            id=sign_id).first()
        if not sign:
            return_not_found(signs_ns, 'sign')
        sign.update(**sign_data)
        return sign, 200


@api.route('/nfts/')
class GetNFTs(Resource):
    """
    Resource to handle:
        - get NFTs
    """

    @signs_ns.doc(description="get NFTs")
    @signs_ns.marshal_with(paginated_schema, envelope='nfts')
    def get(self, page=1, per_page=10):
        """
        Get NFTs

        Returns:
            signs (list): NFTs
        """
        signs = NFT.query.order_by(NFT.token_id.desc()).paginate(
            page, per_page, error_out=False)
        data = {
            'page': signs.page,
            'pages': signs.pages,
            'per_page': signs.per_page,
            'total': signs.total,
            'items': signs.items,
        }
        return data, 200


@api.route('/nfts/<int:token_id>')
class GetNFT(Resource):
    """
    Resource to handle:
        - get NFT
    """

    @signs_ns.doc(description="get NFT")
    @signs_ns.marshal_with(nft_schema, envelope='nft')
    def get(self, token_id):
        """
        Get NFT

        Returns:
            signs (list): NFT
        """
        sign = NFT.query.filter_by(token_id=token_id).first()

        return sign, 200


@api.route('/signs/month/<int:sign_id>/')
class GetUpdateMonthSignsResource(Resource):
    """
    Resource to handle:
        - get month zodiac sign
        - update Month zodiac sign
    """

    @signs_ns.doc(description="get month sign")
    @signs_ns.marshal_with(month_signs_schema, envelope='sign')
    def get(self, sign_id):
        """
        Get Months zodiac signs

        Args:
            sign_id (int): Month sign ID
        Returns:
            sign (obj): Month sign data
        """

        sign = MonthSign.query.filter_by(
            id=sign_id).first()
        if not sign:
            return_not_found(signs_ns, 'sign')

        return sign, 200

    @signs_ns.doc(description="update month sign")
    @signs_ns.expect(month_sign_update_validation())
    @signs_ns.marshal_with(month_signs_schema, envelope='sign')
    def patch(self, sign_id):
        """
        Update Month zodiac sign

        Args:
            sign_id (int): Month sign ID
        Returns:
            sign (obj): Month sign data
        """

        sign_data = signs_ns.payload
        month_sign_update_validation().parse_args(strict=True)
        sign = MonthSign.query.filter_by(
            id=sign_id).first()
        if not sign:
            return_not_found(signs_ns, 'sign')
        sign.update(**sign_data)
        return sign, 200
