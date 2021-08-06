"""Module for user resource"""
from app.api.contract.contract_actions import (
    get_total_tokens, get_wallet_account_balance)
from app import api
from app.api import signs_ns
from app.api.schema import admin_schema
from flask_restplus import Resource


@api.route('/admin/wallet')
class AdminWalletResource(Resource):
    """
    Resource to handle:
        - get admin wallet balance
    """
    @signs_ns.doc(description="Get admin wallet balance")
    @signs_ns.marshal_with(admin_schema, envelope='wallet')
    def get(self, **kwargs):
        """
        get admin wallet balance

        Returns:
            (dict): Returns wallet balance
        """

        return {
            "wallet_balance": get_wallet_account_balance(),
            "total_tokens": get_total_tokens()}, 200
