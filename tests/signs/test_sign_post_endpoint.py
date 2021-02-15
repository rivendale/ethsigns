"""
Module of tests for sign endpoints
"""
from config import AppConfig
from flask import json
from tests.mocks.signs import VALID_YEAR_SIGN, VALID_MONTH_SIGN

BASE_URL = AppConfig.API_BASE_URL_V1


class TestSignsEndpoints:
    """
    Tests endpoint for adding a zodiac sign
    """

    def test_add_sign_with_valid_request_succeeds(
            self, client, init_db, headers):
        """
        Should return an 201 status code and new sign data when data provided
        in request is valid
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 201
        assert response_json['sign']['name'] == 'Tiger'

    def test_add_sign_with_existing_sign_fails(self, client, init_db, new_test_sign, headers):
        """
        Should return an 400 status code when the sign exist in database

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            headers(dict): fixture for the headers
        """
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['sign'] == 'Sign already exist'

    def test_add_sign_with_invalid_list_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the list of values is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['best_compatibility'] = ""
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['best_compatibility'] == \
            'Best compatibility: Provide a list of values'

    def test_add_sign_with_invalid_list_item_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the list items are not string

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['best_compatibility'] = [123]
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['best_compatibility'] == \
            'Best compatibility: Only strings allowed'

    def test_add_sign_with_invalid_element_option_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the element option is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['element'] = "element"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['element'] == \
            "Element: Options are ['Water', 'Wood', 'Fire', 'Metal']"

    def test_add_sign_with_invalid_element_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the element is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['element'] = "&&&&&&"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['element'] == \
            "Element: Provide a valid element"

    def test_add_sign_with_invalid_force_option_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the force option is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['force'] = "force"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['force'] == \
            "Force: Options are ['Yang', 'Yin']"

    def test_add_sign_with_invalid_force_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the force is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['force'] = "&&&&&&&"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['force'] == \
            "Force: Provide a valid force"

    def test_add_sign_with_invalid_name_option_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the name option is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['name'] = "name"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['name'] == \
            "Name: Options are ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']"

    def test_add_sign_with_invalid_name_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the name is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['name'] = "&&&&&&"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['name'] == \
            "Name: Cannot be empty"

    def test_add_sign_with_invalid_url_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the url is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_YEAR_SIGN['image_url'] = "&&&&&&"
        response = client.post(f'{BASE_URL}/signs/year/',
                               data=json.dumps(VALID_YEAR_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['image_url'] == \
            "Image url: Provide a valid url"

    def test_add_month_sign_with_valid_request_succeeds(self, client, init_db, headers):
        """
        Should return an 201 status code and new month sign data when data provided
        in request is valid
        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.post(f'{BASE_URL}/signs/month/',
                               data=json.dumps(VALID_MONTH_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 201
        assert response_json['sign']['animal'] == 'Tiger'

    def test_add_month_sign_with_existing_sign_fails(self, client, init_db, new_month_sign, headers):
        """
        Should return an 400 status code when the sign exist in database

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            headers(dict): fixture for the headers
        """
        response = client.post(f'{BASE_URL}/signs/month/',
                               data=json.dumps(VALID_MONTH_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['sign'] == 'Sign already exist'

    def test_add_month_sign_with_invalid_animal_option_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the animal option is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_MONTH_SIGN['animal'] = "animal"
        response = client.post(f'{BASE_URL}/signs/month/',
                               data=json.dumps(VALID_MONTH_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['animal'] == \
            "Options are ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']"

    def test_add_month_sign_with_invalid_month_value_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the month value is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_MONTH_SIGN['month'] = "month"
        response = client.post(f'{BASE_URL}/signs/month/',
                               data=json.dumps(VALID_MONTH_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['month'] == "Month must be an integer"

    def test_add_month_sign_with_non_existing_month_fails(self, client, init_db, headers):
        """
        Should return an 400 status code when the month value is invalid

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        VALID_MONTH_SIGN['month'] = 13
        response = client.post(f'{BASE_URL}/signs/month/',
                               data=json.dumps(VALID_MONTH_SIGN), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['month'] == "Month out of range"
