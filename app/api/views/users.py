"""Module for user resource"""
from app import api
from app.api import signs_ns
from app.api.helpers.signs import (
    check_existing_user,
    user_address_validator, validate_action)
from app.api.models import User, SignHash
from app.api.schema import (user_schema)
from flask_restplus import Resource


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
