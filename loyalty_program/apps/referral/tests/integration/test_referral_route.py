from freezegun import freeze_time
from datetime import datetime
from unittest.mock import ANY

from django.test import TestCase
from rest_framework.test import RequestsClient

from ...models import Referral
from ..utils import create_user, generate_valid_cpf


class TestReferralView(TestCase):
    """
    Testing the methods on the 'referral/<str:cpf>/' endpoint (GET).
    """

    def setUp(self):
        """
        Initializing the RequestsClient for all tests.
        """

        self.client = RequestsClient()

    def test_should_retrieve_referral_with_200(self):
        """
        Testing if the GET method retrieves a specific referral successfully.
        """

        target_cpf = generate_valid_cpf()
        creation_time = datetime.now().astimezone().isoformat()
        # this is the Datetime format used by Django
        with freeze_time(creation_time):
            create_user()
            Referral.objects.create(
                source_cpf="11987098390",
                target_cpf=target_cpf,
                status=False
            )

        URL = f'http://127.0.0.1:8000/referral/{target_cpf}/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = [
            {'id': 1, 'source_cpf': '11987098390',
             'target_cpf': target_cpf, 'created_at': creation_time,
             'updated_at': creation_time, 'status': False}]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_404_for_user_without_referrals(self):
        """
        Testing if GET method on 'referral/<str:cpf>/' endpoint
        returns a 404 response if the user with the cpf on url path
        hasn't received any referrals        
        """

        unreferred_cpf = generate_valid_cpf()
        URL = f'http://127.0.0.1:8000/referral/{unreferred_cpf}/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = ['error: No active referral towards this person.']

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, expected_json_response)

