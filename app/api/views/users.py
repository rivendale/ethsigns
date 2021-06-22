"""Module for user resource"""
from app.api.contract.contract_actions import get_account_tokens
from app import api
from app.api import signs_ns
from app.api.helpers.signs import (check_existing_user,
                                   user_address_validator, validate_action)
from app.api.models import SignHash, User, MintSign
from app.api.schema import mint_sign_schema, user_schema
from flask_restplus import Resource

from ..validators.validators import mint_token_validator
from datetime import datetime


@api.route('/users/')
class CreateRetrieveUserResource(Resource):
    """
    Resource to handle:
        - adding a user sign
        - list user signs
    """
    @signs_ns.doc(description="create a new user",
                  params={"address": {
                      "description": "Etherium address",
                      "required": True,
                      "type": "str"}})
    @signs_ns.marshal_with(user_schema, envelope='user')
    @user_address_validator
    def get(self, data, **kwargs):
        """
        Add a user

        Returns:
            (tuple): Returns relevant user details
        """
        user = data.get("user")
        address = data.get("address")
        if not user:
            user = User({"address": address})
            user.save()
        return user, 201


@api.route('/users/<sign_hash>/')
class AddRemoveAssetToUsersResource(Resource):
    """
    Resource to handle:
        - assigning an asset to a user
    """

    @signs_ns.doc(description="Allocate zodiac sign to user",
                  params={"action": {
                      "description": "Zodiac action",
                      "required": True,
                      "type": "str"},
                      "address": {
                      "description": "User address",
                      "required": True,
                      "type": "str"}})
    @signs_ns.marshal_with(user_schema, envelope='user')
    @validate_action
    def get(self, *args, **kwargs):
        """
        Allocate zodiac sign to user

        Args:
            sign_hash (str): zodiac sign ID
        Returns:
            user (obj): user data
        """
        data, = args

        user = data.get("user")
        action = data.get("action")
        sign_hash = kwargs.get("sign_hash")
        sign = SignHash.query.filter_by(signhash=sign_hash).first()
        if not sign:
            sign = SignHash({"sign_hash": sign_hash}).save()
        if action == "add":
            user.add_sign(sign)

        if action == "remove":
            if sign not in user.sign_hashes:
                signs_ns.abort(
                    400, errors={"error": "User does not have the provided sign"})
            user.remove_sign(sign)
        return user, 200


@api.route('/users/verify/<sign_hash>/<address>/')
class VerifyAssetResource(Resource):
    """
    Resource to handle:
        - verify that an address owns an asset
    """

    @signs_ns.doc(description="Verify Sign ownership")
    def get(self, sign_hash, address, **kwargs):
        """
        Verify Sign ownership

        Args:
            sign_hash (int): zodiac sign hash
        Returns:
            user (obj): user data
        """
        valid = False
        user = check_existing_user({"address": address})
        sign = SignHash.query.filter_by(signhash=sign_hash).first()

        # if not sign:
        #     return_not_found(signs_ns, 'sign hash')

        if sign in user.sign_hashes:
            valid = True
        return {"valid": valid}, 200


@api.route('/users/tokens/<address>/')
class UserTokensResource(Resource):
    """
    Resource to handle:
        - get user tokens
    """

    @signs_ns.doc(description="Get User tokens")
    def get(self, address, **kwargs):
        """
        Get User tokens

        Args:
            address (int): user address
        Returns:
            tokens (str): user tokens
        """
        tokens = []
        check_existing_user({"address": address})
        try:
            tokens = get_account_tokens(address)
        except Exception as e:
            print(e)
            pass

        return tokens, 200


@api.route('/users/mint/')
class MintTokenZodiacResource(Resource):
    """
    Class to handle:
        - retrieving a sign based on certain query parameters
    """

    @signs_ns.marshal_with(mint_sign_schema, envelope='sign')
    @signs_ns.expect(mint_token_validator(create=True))
    def post(self, *args, **kwargs):
        """
        Function to mint token
        Returns:
            sign (obj): sign data
        """
        mint_data = mint_token_validator().parse_args(strict=True)
        mint_data['created_at'] = datetime.now()

        mint_sign = MintSign(data=mint_data)
        mint_sign.save()
        user = check_existing_user({'address': mint_data['user_address']})
        user.add_mint(mint_sign)

        sign_hash = mint_data.get("sign_hash")
        sign = SignHash({"sign_hash": sign_hash}).save()
        user.add_sign(sign)

        return mint_sign
