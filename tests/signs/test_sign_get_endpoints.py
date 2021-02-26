"""Tests for endpoints to get signs"""

from config import AppConfig
from flask import json

BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetSignDetails:
    """Test for the get sign details endpoint"""

    def test_list_signs_succeeds(
            self, client, init_db, new_test_sign):
        """
        Test that sign details are successfully returned when a valid
        sign id is provided
        """
        new_test_sign.save()
        response = client.get(
            f'{BASE_URL}/signs/year/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        sign_data = response_json['signs']
        assert type(sign_data) == list
        assert sign_data[0]['id'] == new_test_sign.id
        assert sign_data[0]['name'] == new_test_sign.name
        assert sign_data[0]['element'] == new_test_sign.element

    def test_get_sign_with_valid_id_succeeds(
            self, client, init_db, new_test_sign):
        """
        Test that sign details are successfully returned when a valid
        sign id is provided
        """
        new_test_sign.save()
        response = client.get(
            f'{BASE_URL}/signs/year/{new_test_sign.id}/')
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
        response = client.get(f'{BASE_URL}/signs/year/11/')
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 404
        assert response_json['errors']['sign'] == 'sign not found!'

    def test_list_month_signs_succeeds(
            self, client, init_db, new_month_sign):
        """
        Test that month signs can be listed
        """
        new_month_sign.save()
        response = client.get(
            f'{BASE_URL}/signs/month/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        sign_data = response_json['signs']
        assert type(sign_data) == list
        assert sign_data[0]['id'] == new_month_sign.id
        assert sign_data[0]['animal'] == new_month_sign.animal

    def test_query_year_sign_succeeds(
            self, client, init_db, new_test_sign):
        """
        Test that sign details are successfully returned when a valid DOB is provided
        """
        new_test_sign.save()
        response = client.get(
            f'{BASE_URL}/signs/query/?year=1974&month=12&day=2')
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['id'] == new_test_sign.id
        assert sign_data['name'] == new_test_sign.name
        assert sign_data['element'] == new_test_sign.element

    def test_query_year_sign_with_out_of_range_date_fails(
            self, client, init_db):
        """
        Test that sign details are successfully returned when a valid DOB is provided
        """
        response = client.get(
            f'{BASE_URL}/signs/query/?year=1974&month=111&day=2')
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['date_of_birth'] == 'month must be in 1..12'

    def test_query_year_sign_with_invalid_date_fails(
            self, client, init_db):
        """
        Test that sign details are successfully returned when a valid DOB is provided
        """
        response = client.get(
            f'{BASE_URL}/signs/query/?year=1974&month=!!!&day=2')
        response_json = json.loads(response.data.decode("utf-8"))
        assert response.status_code == 400
        assert response_json['errors']['date_of_birth'] == 'Date values should be integers'

    def test_list_day_signs_succeeds(
            self, client, init_db, new_day_sign):
        """
        Test that day signs can be listed
        """
        new_day_sign.save()
        response = client.get(
            f'{BASE_URL}/signs/day/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        sign_data = response_json['signs']
        assert type(sign_data) == list
        assert sign_data[0]['id'] == new_day_sign.id
        assert sign_data[0]['animal'] == new_day_sign.animal

    def test_get_day_sign_succeeds(
            self, client, init_db, new_day_sign_two):
        """
        Test that day sign can be fetched
        """
        new_day_sign_two.save()
        response = client.get(
            f'{BASE_URL}/signs/day/{new_day_sign_two.id}/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['id'] == new_day_sign_two.id
        assert sign_data['animal'] == new_day_sign_two.animal

    def test_get_month_sign_succeeds(
            self, client, init_db, new_month_sign_two):
        """
        Test that month sign can be fetched
        """
        new_month_sign_two.save()
        response = client.get(
            f'{BASE_URL}/signs/month/{new_month_sign_two.id}/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 200
        sign_data = response_json['sign']
        assert sign_data['id'] == new_month_sign_two.id
        assert sign_data['animal'] == new_month_sign_two.animal

    def test_get_non_existent_month_sign_fails(
            self, client, init_db):
        """
        Test that error is thrown when non existent month sign is fetched
        """
        response = client.get(
            f'{BASE_URL}/signs/month/11/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert response_json['errors']['sign'] == "sign not found!"

    def test_get_non_existent_day_sign_fails(
            self, client, init_db):
        """
        Test that error is thrown when non existent day sign is fetched
        """
        response = client.get(
            f'{BASE_URL}/signs/day/11/')
        response_json = json.loads(response.data.decode("utf-8"))

        assert response.status_code == 404
        assert response_json['errors']['sign'] == "sign not found!"
