"""
In this file we will create tests to verify that our API endpoints
are wrorking properly and returning consistent errors.
"""
from django.test import TestCase
from rest_framework.test import RequestsClient

from ..models import Client, Referral


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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'User detail and update': 'user/<str:cpf>/',
                'List of all referrals registered': 'all-referrals/',
                'List of all referrals performed by an user registered': 'all-referrals/<str:cpf>/',
                'Information on specific referral': 'referral/<str:cpf>/',
                'Create new referral': 'create-referral/',
                'Accept specific referral': 'accept-referral/<str:cpf>/',
                })
