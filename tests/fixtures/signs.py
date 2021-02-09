"""Module with sign fixtures """

# Third Party Modules
import pytest
from app.api.models.signs import Zodiacs


@pytest.fixture(scope='module')
def new_test_sign(app):

    return Zodiacs({
        "name": "Tiger",
        "force": "Yang",
        "element": "Wood",
        "image_url": "http://image.png",
        "best_compatibility": "['Horse', 'Dog']",
        "worst_compatibility": "['Snake', 'Monkey']",
        "positive_traits": "['Ambitious', 'Brave', 'Dynamic']",
        "negative_traits": "['Aggressive', 'Arrogant', 'Disobedient']",
        "report": "['Your personality represents power, courage, and action ']"
    })
