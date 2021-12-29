from freezegun import freeze_time
from datetime import datetime

from django.test import TestCase
from rest_framework.test import RequestsClient

from ...models import Referral, Client
from ..utils import create_user, generate_valid_cpf


class TestCreateReferralView(TestCase):
    """
    Testing the methods on the 'create-referral/' endpoint. 
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

    def test_should_return_200_and_wait_for_referral(self):
        """
        Testing if the GET method on endpoint.
        """

        URL = 'http://127.0.0.1:8000/create-referral/'
        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = ["waiting on referral creation"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, expected_json_response)

    def test_should_post_referral_with_201(self):
        """
        Testing if the POST method on endpoint successfully creates the 
        referral for a valid input on request.
        """

        referred_cpf = generate_valid_cpf()
        URL = 'http://127.0.0.1:8000/create-referral/'
        creation_time = datetime.now().astimezone().isoformat()
        body = {
            'source_cpf': '11987098390',
            'target_cpf': referred_cpf,
            'status': False
        }

        with freeze_time(creation_time):
            response = self.client.post(URL, body)
            json_response = response.json()

        expected_json_response = {
            "Referral registered": {
                "id": 1,
                "source_cpf": "11987098390",
                "target_cpf": referred_cpf,
                "created_at": creation_time,
                "updated_at": creation_time,
                "status": False
            }
        }

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Referral.objects.count(), 1)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_404_if_referrer_is_unregistered(self):
        """
        Testing if the POST method on endpoint returns a 404 response if 
        the user trying to refer someone isn't registered on database.   
        """

        URL = 'http://127.0.0.1:8000/create-referral/'
        body = {
            'source_cpf': generate_valid_cpf(),
            'target_cpf': generate_valid_cpf(),
            'status': False
        }

        response = self.client.post(URL, body)
        json_response = response.json()

        expected_json_response = [
            'error: User must be registered to make a referral']

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Referral.objects.count(), 0)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_400_if_referent_is_already_registered(self):
        """
        Testing if the POST method on endpoint returns a 400 response if 
        the user is trying to refer someone already registered on database.   
        """

        Client.objects.create(
            cpf="51805510649",
            name="New cLient",
            phone="31992818778",
            email="client@gmail.com"
        )

        URL = 'http://127.0.0.1:8000/create-referral/'
        body = {
            'source_cpf': 11987098390,
            'target_cpf': 51805510649,
            'status': False
        }

        response = self.client.post(URL, body)
        json_response = response.json()

        expected_json_response = [
            'error: Referred person is already registered']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Referral.objects.count(), 0)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_400_if_user_refers_themselves(self):
        """
        Testing if the POST method on endpoint returns a 400 response if 
        the user is trying to refer themselves.   
        """

        URL = 'http://127.0.0.1:8000/create-referral/'
        body = {
            'source_cpf': 11987098390,
            'target_cpf': 11987098390,
            'status': False
        }

        response = self.client.post(URL, body)
        json_response = response.json()

        expected_json_response = ['error: User cannot refer themselves']

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Referral.objects.count(), 0)
        self.assertEqual(json_response, expected_json_response)

    def test_should_Return_400_if_referent_was_already_referred(self):
        """
        Testing if the POST method on endpoint returns a 400 response if 
        the user is trying to refer someone with an active referral.   
        """

        target_cpf = generate_valid_cpf()
        Referral.objects.create(
            source_cpf="11987098390",
            target_cpf=target_cpf,
            status=False
        )
        URL = 'http://127.0.0.1:8000/create-referral/'
        body = {
            'source_cpf': 11987098390,
            'target_cpf': target_cpf,
            'status': False
        }

        response = self.client.post(URL, body)
        json_response = response.json()

        expected_json_response = 'error: This person was already referred.'

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Referral.objects.count(), 1)
        self.assertEqual(json_response, expected_json_response)

    def test_should_Return_400_if_referring_invalid_cpf(self):
        """
        Testing if the POST method on endpoint returns a 400 response if 
        the user is trying to refer an invalid cpf number.   
        """

        URL = 'http://127.0.0.1:8000/create-referral/'
        body = {
            'source_cpf': 11987098390,
            'target_cpf': 11111111111,
            'status': False
        }

        response = self.client.post(URL, body)
        json_response = response.json()

        expected_json_response = {"target_cpf": ["Invalid CPF number."]}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Referral.objects.count(), 0)
        self.assertEqual(json_response, expected_json_response)
