import calendar
import datetime
from functools import wraps

from app.api import signs_ns as ns
from app.api.models.signs import MonthSign, Zodiacs
from flask import request


def check_existing_year_signs(sign):
    """
    Function to check if signs already exists
    Args:
        sign(dict): sign object
    Return:
        user(obj): sign object
    """
    z_sign = Zodiacs.query.filter_by(
        name=sign['name']).first()
    if z_sign:
        ns.abort(400, errors={"sign": "Sign already exist"}, message="sign exists!")
    return z_sign


def check_existing_month_signs(sign):
    """
    Function to check if signs already exists
    Args:
        sign(dict): sign object
    Return:
        user(obj): sign object
    """
    z_sign = MonthSign.query.filter_by(
        month=sign['month']).first()
    if z_sign:
        ns.abort(400, errors={"sign": "Sign already exist"}, message="sign exists!")
    return z_sign


def return_not_found(ns, entity):
    """
    Function return a not found message
    Args:
        entity (str): entity name
    Return:
        (str): entity not found message
    """
    ns.abort(404, errors={"sign": f"{entity} not found!"},
             message="Entity not found")


def date_validator(func):
    """Validates date of birth parameter

    Raises error if date of birth is invalid

    Args:
        func(function): Decorated function

    Returns:
        function

    Raises:
        Throws error if date is not valid
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        query = request.args.to_dict()

        # normalize the query keys
        norm_query = {
            key.lower().strip(): value
            for key, value in query.items()
        }
        data = {}
        try:
            year = int(norm_query.get('year', ""))
            month = int(norm_query.get('month', ""))
            day = int(norm_query.get('day', ""))
            data['year'] = year
            data['month'] = month
            try:
                dob = datetime.datetime(year=year, month=month, day=day)
                data['day'] = calendar.day_name[dob.weekday()]
            except ValueError as error:
                ns.abort(400, errors={"date_of_birth": str(error)},
                         message="Error!")
        except ValueError:
            ns.abort(400, errors={"date_of_birth": "Date values should be integers"},
                     message="Error!")
        return func(*args, data, **kwargs)

    return decorated_function
