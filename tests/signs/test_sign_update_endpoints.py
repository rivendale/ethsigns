"""Tests for endpoints to get signs"""

from config import AppConfig
from flask import json

BASE_URL = AppConfig.API_BASE_URL_V1


class TestUpdateSignDetails:
    """Test for the update sign details endpoint"""

    def test_update_day_sign_succeeds(
            self, client, init_db, new_day_sign, headers):
        """
        Test that day sign can be updated
        """
        new_day_sign.save()
        response = client.patch(
            f'{BASE_URL}/signs/day/{new_day_sign.id}/',
            data=json.dumps({"animal": "Snake"}), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['animal'] == "Snake"

    def test_update_non_existent_day_sign_fails(
            self, client, init_db, headers):
        """
        Test that non existent day sign can be updated
        """
        response = client.patch(
            f'{BASE_URL}/signs/day/123/',
            data=json.dumps({"animal": "Snake"}), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 404
        assert response_json['errors']['sign'] == "sign not found!"

    def test_update_month_sign_succeeds(
            self, client, init_db, new_month_sign, headers):
        """
        Test that month sign can be updated
        """
        new_month_sign.save()
        response = client.patch(
            f'{BASE_URL}/signs/month/{new_month_sign.id}/',
            data=json.dumps({"animal": "Snake"}), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['animal'] == "Snake"

    def test_update_non_existent_month_sign_fails(
            self, client, init_db, headers):
        """
        Test that non existent month sign can be updated
        """
        response = client.patch(
            f'{BASE_URL}/signs/month/123/',
            data=json.dumps({"animal": "Snake"}), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 404
        assert response_json['errors']['sign'] == "sign not found!"

    def test_update_year_sign_succeeds(
            self, client, init_db, new_test_sign, headers):
        """
        Test that year sign can be updated
        """
        new_test_sign.save()
        response = client.patch(
            f'{BASE_URL}/signs/year/{new_test_sign.id}/',
            data=json.dumps({"best_compatibility": ["Horse", "Dog"]}), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['best_compatibility'] == ["Horse", "Dog"]

    def test_update_non_existent_year_sign_fails(
            self, client, init_db, headers):
        """
        Test that non existent year sign can be updated
        """
        response = client.patch(
            f'{BASE_URL}/signs/year/123/',
            data=json.dumps({"best_compatibility": ["Horse", "Dog"]}), headers=headers)
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 404
        assert response_json['errors']['sign'] == "sign not found!"
