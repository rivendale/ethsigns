"""Module for user resource"""
from datetime import datetime

from app import api, db
from app.api import signs_ns
from app.api.contract.contract_actions import (
    complete_pending_transactions,
    verify_admin)
#    get_account_tokens)
from app.api.helpers.signs import (check_existing_user, user_address_validator,
                                   validate_action)
from app.api.models import MintSign, SignHash, User
from app.api.schema import mint_sign_schema, user_schema, paginated_schema
from config import Config
from flask_restplus import Resource

from ..validators.validators import mint_token_validator


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
        # sign = SignHash.query.filter_by(signhash=sign_hash).first()
        result = db.session.query(User.address, SignHash.signhash).filter(
            SignHash.signhash == sign_hash).filter(User.address == user.address).first()

        # if not sign:
        #     return_not_found(signs_ns, 'sign hash')
        if result:
            valid = True
        return {"valid": valid,
                }, 200


@api.route('/users/tokens/<address>/')
class UserTokensResource(Resource):
    """
    Resource to handle:
        - get user tokens
    """

    @signs_ns.doc(description="Get User tokens")
    @signs_ns.marshal_with(paginated_schema, envelope='nfts')
    def get(self, address, page=1, per_page=10, **kwargs):
        """
        Get User tokens

        Args:
            address (int): user address
        Returns:
            tokens (str): user tokens
        """
        user = check_existing_user({"address": address})

        items = user.user_nfts
        data = {
            'items': items,
            'page': page,
            'pages': len(items) // per_page,
            'per_page': per_page,
            'total': len(items),
        }
        # breakpoint()
        # try:
        #     tokens = get_account_tokens(address)
        # except Exception as e:
        #     print(e)
        #     pass

        return data, 200


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

        user = check_existing_user({'address': mint_data['user_address']})
        if not mint_data.get('transaction_hash', None) and not\
                sum([user.pending_mints, user.tokens_minted]) >= 1:
            mint_data['transaction_hash'] = "free"
        mint_sign = MintSign(data=mint_data)
        mint_sign.save()
        user.add_mint(mint_sign)

        sign_hash = mint_data.get("sign_hash")
        sign = SignHash({"sign_hash": sign_hash}).save()
        user.add_sign(sign)
        complete_pending_transactions.delay()

        return mint_sign


@api.route('/users/stats/<address>/')
class UserStatsResource(Resource):
    """
    Resource to handle:
        - get user stats
    """

    @signs_ns.doc(description="Get User stats")
    def get(self, address, **kwargs):
        """
        Get User stats

        Args:
            address (int): user address
        Returns:
            stats (dict): user stats
        """
        user = check_existing_user({"address": address})
        # breakpoint()
        is_admin = verify_admin(address)
        minted_tokens_count = db.session.query(MintSign).count()
        stats = {
            "tokens_minted": minted_tokens_count,
            "remaining_mints": int(Config.MAX_TOKEN_COUNT - minted_tokens_count),
            "pending_mints": user.pending_mints,
            'free_mint': minted_tokens_count <= 100 and
            sum([user.pending_mints, user.tokens_minted]) == 0
        }
        if is_admin:
            stats["is_admin"] = is_admin

        return stats, 200
