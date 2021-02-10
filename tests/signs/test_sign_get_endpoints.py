"""Tests for endpoints to get signs"""

from config import AppConfig
from flask import json
from tests.mocks.signs import VALID_SIGN

BASE_URL = AppConfig.API_BASE_URL_V1




class TestGetSignDetails:
    """Test for the get sign details endpoint"""

    def test_get_sign_with_valid_id_succeeds(
            self, client, init_db, new_test_sign):
        """
        Test that sign details are successfully returned when a valid
        sign id is provided
        """
        new_test_sign.save()
        response = client.get(
            f'{BASE_URL}/signs/{new_test_sign.id}/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['id'] == new_test_sign.id
        assert sign_data['name'] == new_test_sign.name
        assert sign_data['element'] == new_test_sign.element

    def test_get_sign_details_with_invalid_id_fails(
            self, client, init_db, new_test_sign):
        """
        Test that an error message is returned when an invalid sign_id is
        provided
        """
        response = client.get(f'{BASE_URL}/signs/11/')
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 404
        assert response_json['errors']['sign'] == 'sign not found!'
