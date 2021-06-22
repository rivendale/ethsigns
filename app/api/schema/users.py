from flask_restplus import fields
from flask_restplus import marshal
from app.api import signs_ns


sign_hashes_schema = {
    'id': fields.Integer(description='The Sign identifier'),
    'signhash': fields.String(description='Sign Hashes'),
}

sign_hashes_schema = signs_ns.model('SignHash', sign_hashes_schema)


class SignHashes(fields.Raw):
    """
    sign Formatter
    """

    def format(self, value):
        """
        Return a formatted sign details
        Args:
            value (list): List of user signs objects
        Returns:
            (dict): formatted signs
        """
        sign_hashes = [marshal(hash, sign_hashes_schema)
                       for hash in value]

        return sign_hashes


user_schema = {
    'id': fields.Integer(description='The User identifier'),
    'address': fields.String(description='User Etherium address'),
    "sign_hashes": SignHashes(attribute='sign_hashes')
}

user_schema = signs_ns.model('User', user_schema)


mint_sign_schema = {
    'id': fields.Integer(description='The User identifier'),
    'dob': fields.Date(description='User DOB'),
    'created_at': fields.DateTime(description="Instance created at"),
    'user_address': fields.String(description='User Etherium address'),
    'transaction_hash': fields.String(description='Transaction Hash'),
    'minted': fields.Boolean(description='Sign Minted status'),
}

mint_sign_schema = signs_ns.model('MintSign', mint_sign_schema)
