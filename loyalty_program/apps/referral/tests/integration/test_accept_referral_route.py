from freezegun import freeze_time
from datetime import datetime, timedelta
from unittest.mock import ANY

from django.test import TestCase
from rest_framework.test import RequestsClient

from ...models import Referral, Client
from ..utils import create_user, generate_valid_cpf


class TestAcceptReferralView(TestCase):
    """
    Testing the methods on the 'accept-referral/' endpoint. 
    """

    def setUp(self):
        """
        Initializing the RequestsClient for all tests, as well as creating 
        an user and a referral.
        """

        self.creation_time = datetime.now().astimezone().isoformat()
        # this is the Datetime format used by Django
        self.target_cpf = generate_valid_cpf()
        with freeze_time(self.creation_time):
            create_user()
            Referral.objects.create(
                source_cpf="11987098390",
                target_cpf=self.target_cpf,
                status=False
            )

        self.client = RequestsClient()

    def test_should_return_200_and_specific_referral(self):
        """
        Testing if the GET method on endpoint.
        """

        URL = f'http://127.0.0.1:8000/accept-referral/{self.target_cpf}/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = {
            'id': 1, 'source_cpf': '11987098390',
            'target_cpf': self.target_cpf, 'created_at': self.creation_time,
            'updated_at': self.creation_time, 'status': False}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_404_for_cpf_without_referral(self):
        """
        Testing if GET method on 'accept-referral/<str:cpf>/' endpoint
        returns a 404 response if the user with the cpf on url path
        isn't connected to a valid referral on database.        
        """

        unreferred_cpf = generate_valid_cpf()
        URL = f'http://127.0.0.1:8000/accept-referral/{unreferred_cpf}/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = {
            'error': 'No active referral registered for this CPF'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, expected_json_response)

    def test_should_post_referral_with_201(self):
        """
        Testing if the PUT method on endpoint successfully updates the 
        referral in order to accept it (status = True) and that the user
        recieves points for the referral approval.
        """

        URL = f'http://127.0.0.1:8000/accept-referral/{self.target_cpf}/'
        update_time = datetime.now().astimezone().isoformat()
        body = {
            'source_cpf': '11987098390',
            'target_cpf': self.target_cpf,
            'status': True
        }

        with freeze_time(update_time):
            response = self.client.put(URL, body)
            json_response = response.json()

        expected_json_response = {
            "Updated referral:": {
                "id": 1,
                "source_cpf": "11987098390",
                "target_cpf": self.target_cpf,
                "created_at": self.creation_time,
                "updated_at": update_time,
                "status": True
            }
        }

        client = Client.objects.get(cpf=11987098390)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Referral.objects.count(), 1)
        self.assertEqual(json_response, expected_json_response)
        self.assertEqual(client.points, 10)

    def test_should_return_400_if_updating_To_invalid_cpf(self):
        """
        Testing if the PUT method on endpoint returns a 400 response if
        user is trying to update the referent cpf with an invalid number.
        """

        URL = f'http://127.0.0.1:8000/accept-referral/{self.target_cpf}/'
        update_time = datetime.now().astimezone().isoformat()
        body = {
            'source_cpf': '11987098390',
            'target_cpf': '11111111111',
            'status': True
        }

        response = self.client.put(URL, body)
        json_response = response.json()

        expected_json_response = {"target_cpf": ["Invalid CPF number."]}

        client = Client.objects.get(cpf=11987098390)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Referral.objects.count(), 1)
        self.assertEqual(json_response, expected_json_response)
        self.assertEqual(client.points, 0)

    def test_should_return_400_if_changing_referent_cpf(self):
        """
        Testing if the PUT method on endpoint returns a 400 response if
        user is trying to update the referent cpf.
        """

        URL = f'http://127.0.0.1:8000/accept-referral/{self.target_cpf}/'
        update_time = datetime.now().astimezone().isoformat()
        body = {
            'source_cpf': '11987098390',
            'target_cpf': generate_valid_cpf(),
            'status': True
        }

        response = self.client.put(URL, body)
        json_response = response.json()

        expected_json_response = {'error': 'cannot change users CPF'}

        client = Client.objects.get(cpf=11987098390)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Referral.objects.count(), 1)
        self.assertEqual(json_response, expected_json_response)
        self.assertEqual(client.points, 0)

    def test_should_not_return_expired_referrals(self):
        """
        Testing if expired referrals are actually deleted from the database.
        """

        target_cpf = generate_valid_cpf()
        expired_date = datetime.now() - timedelta(days=30)
        expired_date_formatted = expired_date.astimezone().isoformat()

        with freeze_time(expired_date_formatted):
            Referral.objects.create(
                source_cpf="11987098390",
                target_cpf=target_cpf,
                status=False
            )

        self.assertEqual(Referral.objects.count(), 2)
        # before calling a method that deletes expired referrals

        URL = f'http://127.0.0.1:8000/accept-referral/{target_cpf}/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = {
            'error': 'No active referral registered for this CPF'}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, expected_json_response)

        self.assertEqual(Referral.objects.count(), 1)
        # after calling a method that deletes expired referrals
