from flask_restplus import fields
from flask_restplus import marshal
from app.api import signs_ns
from .year_signs import minimal_year_signs


class Signs(fields.Raw):
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
        signs = [marshal(sign, minimal_year_signs)
                 for sign in value]

        return signs


user_schema = {
    'id': fields.Integer(description='The User identifier'),
    'address': fields.String(description='User Etherium address'),
    "signs": Signs(attribute='signs')
}

user_schema = signs_ns.model('User', user_schema)
