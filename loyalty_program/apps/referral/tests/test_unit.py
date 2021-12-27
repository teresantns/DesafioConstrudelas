from django.test import TestCase

from ..models import Client, Referral
from ..serializers import ClientSerializer, ReferralSerializer


class TestClientsSerializer(TestCase):
    """
    Test class for unit testing the Client serializer
    """

    def setUp(self):  # setting up data for the test class
        self.client_to_be_created = {
            "cpf": "11987098390",
            "name": "Luisa Souza",
            "phone": "31998877554",
            "email": "luisa@gmail.com"
        }
        self.client_to_fail_cpf = {
            "cpf": "11111111111",
            "name": "Luisa Souza",
            "phone": "31998877554",
            "email": "luisa@gmail.com"
        }
        self.client_to_fail_email = {
            "cpf": "11987098390",
            "name": "Luisa Souza",
            "phone": "31998877554",
            "email": "luisa.com"
        }

    def test_client_serializer_validation(self):
        """
        Testing if the ClientSerializer correctly validates the data
        i.e, is not valid if the CPF or email fields are incorrect
        """
        serializer_correct = ClientSerializer(data=self.client_to_be_created)
        serializer_cpf = ClientSerializer(data=self.client_to_fail_cpf)
        serializer_email = ClientSerializer(data=self.client_to_fail_email)

        self.assertEqual(serializer_correct.is_valid(), True)
        self.assertEqual(serializer_cpf.is_valid(), False)
        self.assertEqual(serializer_email.is_valid(), False)

    def test_serializer_errors(self):
        """
        Testing if the serializer gives the correct errors for invalid
        data input
        """

        serializer_cpf = ClientSerializer(data=self.client_to_fail_cpf)
        serializer_email = ClientSerializer(data=self.client_to_fail_email)

        serializer_cpf.is_valid()
        serializer_email.is_valid()

        self.assertIn('cpf', serializer_cpf.errors.keys())
        self.assertIn('email', serializer_email.errors.keys())


class TestClientsModel(TestCase):
    """
    Test class for unit testing the Client model
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client.objects.create(
            cpf="11987098390",
            name="Luisa Souza",
            phone="31998877554",
            email="luisa@gmail.com"
        )

    def test_create_client(self):
        """
        Testing if a client (assuming their serializer is valid, as per the 
        previous test class) is correctly created
        """

        created_client = Client.objects.first()

        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(created_client.name, 'Luisa Souza')
        self.assertEqual(created_client.cpf, '11987098390')
        self.assertEqual(created_client.phone, '31998877554')
        self.assertEqual(created_client.email, 'luisa@gmail.com')
        self.assertEqual(created_client.points, 0)
        self.assertIsNotNone(created_client.created_at)
        self.assertIsNotNone(created_client.updated_at)
