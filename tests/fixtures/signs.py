"""Module with sign fixtures """

# Third Party Modules
import pytest
from app.api.models.signs import Zodiacs, MonthSign, DaySign
from app.models import Sign
from app import db


@pytest.fixture(scope='module')
def new_test_sign(app):

    return Zodiacs({
        "name": "Tiger",
        "force": "Yang",
        "element": "Wood",
        "base_index": 2,
        "image_url": "http://image.png",
        "best_compatibility": "['Horse', 'Dog']",
        "worst_compatibility": "['Snake', 'Monkey']",
        "positive_traits": "['Ambitious', 'Brave', 'Dynamic']",
        "negative_traits": "['Aggressive', 'Arrogant', 'Disobedient']",
        "report": "['Your personality represents power, courage, and action ']"
    })


@pytest.fixture(scope='function')
def new_month_sign(app):

    return MonthSign({
        "month": 2,
        "animal": "Tiger"
    })


@pytest.fixture(scope='function')
def new_day_sign(app):

    return DaySign({
        "day": "Tuesday",
        "animal": "Pig"
    })


@pytest.fixture(scope='module')
def new_sign(app):

    sign = Sign(**{
        "year": 1995,
        "month": 1,
        "day": 31,
        "bsign": "dog",
        "btype": "wood",
        "dsign": "pig",
        "dtype": "wood"
    })
    db.session.add(sign)


@pytest.fixture(scope='module')
def test_sign_two(app):

    sign_two = Sign(**{
        "year": 1996,
        "month": 2,
        "day": 3,
        "bsign": "pig",
        "btype": "fire",
        "dsign": "dog",
        "dtype": "fire"
    })
    db.session.add(sign_two)
