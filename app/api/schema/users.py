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
