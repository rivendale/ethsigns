from app.api.helpers.constants import ZODIAC_ANIMALS
import re
from flask_restplus import reqparse


STRING_REGEX = re.compile(r"^[a-zA-Z0-9]+(([' .-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$")
URL_REGEX = re.compile(r"^(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)")


def header_parser(token="token"):
    """
    Function to add Authorization to the request header parser
    Args:
        token (str): user token
    Return:
        parser (obj): request parser
    """
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization',
                        required=True,
                        help=f"Bearer {{{token}}}", location='headers')
    return parser


def validate_list_values(values):
    """
    Function to add validate list objects
    Args:
        values (list): list of values to be validated
    Raises:
        (ValueError): Raise ValueError if list is invalid
    Return:
        values (list): valid list object
    """
    if not isinstance(values, list):
        raise ValueError("Provide a list of values")
    for i in values:
        if not isinstance(i, str):
            raise ValueError("Only strings allowed")

    return values


def validate_name(value):
    """
    Function to validate the name
    Args:
        value (str): name to be validated
    Raises:
        (ValueError): Raise ValueError if the name invalid
    Return:
        value (str): valid name
    """
    animals = [x.upper() for x in [*ZODIAC_ANIMALS]]
    if not re.match(STRING_REGEX, value):
        raise ValueError("Provide a valid name")

    if value.upper() not in animals:
        raise ValueError(f"Options are {[*ZODIAC_ANIMALS]}")

    return value


def validate_url(value):
    """
    Function to validate the url
    Args:
        value (str): url to be validated
    Raises:
        (ValueError): Raise ValueError if the url invalid
    Return:
        value (str): valid url
    """
    if not re.match(URL_REGEX, value):
        raise ValueError("Provide a valid url")

    return value


def sign_validation(create=True):
    """
    Function to add sign validation to the parser
    Args:
        create (Bool): 'required' option
    Return:
        parser (obj): request parser
    """

    parser = reqparse.RequestParser(trim=True, bundle_errors=True)
    parser.add_argument('name',
                        type=validate_name,
                        required=create,
                        help='Name:', location='json',)
    parser.add_argument('positive_traits',
                        type=validate_list_values,
                        required=create,
                        help='Positive traits:',
                        case_sensitive=False, location='json')
    parser.add_argument('negative_traits',
                        type=validate_list_values,
                        required=create,
                        help='Negative traits:',
                        case_sensitive=False, location='json')
    parser.add_argument('positive_traits',
                        type=validate_list_values,
                        required=create,
                        help='Positive traits:',
                        case_sensitive=False, location='json')
    parser.add_argument('best_compatibility',
                        type=validate_list_values,
                        required=create,
                        help='Best compatibility:',
                        case_sensitive=False, location='json')
    parser.add_argument('worst_compatibility',
                        type=validate_list_values,
                        required=create,
                        help='Worst compatibility:',
                        case_sensitive=False, location='json')
    parser.add_argument('report',
                        type=validate_list_values,
                        required=create,
                        help='Report:',
                        case_sensitive=False, location='json')
    parser.add_argument('image_url',
                        type=validate_url,
                        required=create, help='Image url: ',
                        case_sensitive=False)

    return parser
