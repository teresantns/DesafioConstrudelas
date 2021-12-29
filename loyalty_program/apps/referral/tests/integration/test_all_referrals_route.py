from freezegun import freeze_time
from datetime import datetime
from unittest.mock import ANY

from django.test import TestCase
from rest_framework.test import RequestsClient

from ...models import Client
from ..utils import create_user, generate_valid_cpf, create_referral


class TestAllReferralsView(TestCase):
    """
    Testing the methods on the 'all-referrals/' and 
    'all-referrals/<str:cpf>/' endpoints.
    """

    def setUp(self):
        """
        Initializing the RequestsClient for all tests.
        """

        self.client = RequestsClient()
        self.creation_time = datetime.now().astimezone().isoformat()
        # this is the Datetime format used by Django
        with freeze_time(self.creation_time):
            create_user()
            create_referral()
            create_referral()

    def test_should_retrieve_all_referrals_with_200(self):
        """
        Testing if the GET method retrieves all referrals successfully.
        """

        URL = 'http://127.0.0.1:8000/all-referrals/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = [
            {'id': 1, 'source_cpf': '11987098390',
             'target_cpf': ANY, 'created_at': self.creation_time,
             'updated_at': self.creation_time, 'status': False},
            {'id': 2, 'source_cpf': '11987098390',
             'target_cpf': ANY, 'created_at': self.creation_time,
             'updated_at': self.creation_time, 'status': False}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response, expected_json_response)

    def test_should_retrieve_all_user_referrals_with_200(self):
        """
        Testing if GET method on 'all-referrals/<str:cpf>/' endpoint
        returns all referrals made by user with the cpf on the url path.
        """

        URL = 'http://127.0.0.1:8000/all-referrals/11987098390'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = [
            {'id': 1, 'source_cpf': '11987098390',
             'target_cpf': ANY, 'created_at': self.creation_time,
             'updated_at': self.creation_time, 'status': False},
            {'id': 2, 'source_cpf': '11987098390',
             'target_cpf': ANY, 'created_at': self.creation_time,
             'updated_at': self.creation_time, 'status': False}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response, expected_json_response)
    
    def test_should_return_404_for_unregistered_user_referrals(self):
        """
        Testing if GET method on 'all-referrals/<str:cpf>/' endpoint
        returns a 404 response if the cpf is not registered in the database.
        """

        unregistered_cpf = generate_valid_cpf()

        URL = f'http://127.0.0.1:8000/all-referrals/{unregistered_cpf}/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = ["error: User not on database"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_404_for_user_without_referrals(self):
        """
        Testing if GET method on 'all-referrals/<str:cpf>/' endpoint
        returns a 404 response if the user with the cpf on url path
        hasn't made any referrals.
        """

        Client.objects.create(
            cpf="51805510649",
            name="New cLient",
            phone="31992818778",
            email="client@gmail.com"
        )

        URL = f'http://127.0.0.1:8000/all-referrals/51805510649/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = ["error: User doesn't have registered referrals"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, expected_json_response)


