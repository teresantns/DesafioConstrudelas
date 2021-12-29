from freezegun import freeze_time
from datetime import datetime

from django.test import TestCase
from rest_framework.test import RequestsClient

from ..utils import generate_valid_cpf, create_user


class TestMainPage(TestCase):
    """
    Testing the MainPage endpoint.
    """

    def setUp(self):
        """
        Initializing our API client to test our http methods
        """
        self.client = RequestsClient()

    def test_should_get_main_page_with_http_200(self):
        """
        Testing if the main page's response is 200 - OK (MainPage view)
        """
        response = self.client.get('http://127.0.0.1:8000')
        expected_json = {'User detail and update': 'user/<str:cpf>/',
                         'List of all referrals registered': 'all-referrals/',
                         'List of all referrals performed by an user registered': 'all-referrals/<str:cpf>/',
                         'Information on specific referral': 'referral/<str:cpf>/',
                         'Create new referral': 'create-referral/',
                         'Accept specific referral': 'accept-referral/<str:cpf>/',
                         }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json)


class TestUpdateUserView(TestCase):
    """
    Testing the methods on the 'user/<str:cpf>/' endpoint
    (GET and PUT).
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

    def test_should_retrieve_specific_user_with_200(self):
        """
        Testing if the users can be searched, with the GET method
        by their cpf on the url path.
        """

        URL = 'http://127.0.0.1:8000/user/11987098390/'

        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = {
            "cpf": "11987098390", "name": "Luisa Souza",
            "phone": "31998877554", "email": "luisa@gmail.com",
            "created_at": self.creation_time,
            "updated_at": self.creation_time, "points": 0
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_404_for_nonexisting_client(self):
        """
        Testing if the API returns a 'not found' response when trying to
        get information on a not registered user (GET method).
        """

        unregistered_cpf = generate_valid_cpf()
        URL = f'http://127.0.0.1:8000/user/{unregistered_cpf}/'

        response = self.client.get(URL)
        json_response = response.json()

        expected_json_response = {"detail": "Not found."}

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response, expected_json_response)

    def test_should_update_user_with_valid_input(self):
        """
        Testing if the PUT method on endpoint successfully updates the client
        information for a valid input on request.
        """

        URL = 'http://127.0.0.1:8000/user/11987098390/'
        update_time = datetime.now().astimezone().isoformat()
        body = {
            "cpf": "11987098390", "name": "Luisa Souza",
            "phone": "31998877554", "email": "luisa_souza@gmail.com"
        }

        with freeze_time(update_time):
            response = self.client.put(URL, data=body)
            json_response = response.json()

        expected_json_response = {
            "Updated user:": {
                "cpf": "11987098390",
                "name": "Luisa Souza",
                "phone": "31998877554",
                "email": "luisa_souza@gmail.com",
                "created_at": self.creation_time,
                "updated_at": update_time,
                "points": 0
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_400_if_changing_cpf(self):
        """
        Testing if the PUT method on endpoint returns a bad response
        if user is trying to update their CPF number.
        """

        URL = 'http://127.0.0.1:8000/user/11987098390/'
        body = {
            "cpf": "51805510649", "name": "Luisa Souza",
            "phone": "31998877554", "email": "luisa@gmail.com"
        }

        response = self.client.put(URL, data=body)
        json_response = response.json()

        expected_json_response = {"error": "cannot change user CPF"}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_400_if_invalid_cpf(self):
        """
        Testing if the PUT method on endpoint returns a bad response
        if user is trying to update their CPF number with an invalid CPF.
        """

        URL = 'http://127.0.0.1:8000/user/11987098390/'
        body = {
            "cpf": "1198709839", "name": "Luisa Souza",
            "phone": "31998877554", "email": "luisa@gmail.com"
        }

        response = self.client.put(URL, data=body)
        json_response = response.json()

        expected_json_response = {"cpf": ["Invalid CPF number."]}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response, expected_json_response)

    def test_should_return_400_if_invalid_email(self):
        """
        Testing if the PUT method on endpoint returns a bad response
        if user is trying to update their CPF number with an invalid CPF.
        """

        URL = 'http://127.0.0.1:8000/user/11987098390/'
        body = {
            "cpf": "11987098390", "name": "Luisa Souza",
            "phone": "31998877554", "email": "luisa"
        }

        response = self.client.put(URL, data=body)
        json_response = response.json()

        expected_json_response = {'email': ['Enter a valid email address.']}

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response, expected_json_response)
