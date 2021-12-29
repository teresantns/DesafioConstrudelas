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

    def test_client_serializer_errors(self):
        """
        Testing if the client serializer gives the correct errors 
        for invalid data input
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
        previous test class) is correctly created, with the respective fields
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


class TestReferralsSerializer(TestCase):
    """
    Test class for unit testing the Referral serializer
    """

    def setUp(self):  # setting up data for the test class
        self.valid_referral = {
            "source_cpf": "11987098390",
            "target_cpf": "51805510649",
            "status": False
        }
        self.invalid_referral = {
            "source_cpf": "11111111111",
            "target_cpf": "0123",
            "status": False
        }

        self.serializer_valid_referral = ReferralSerializer(
            data=self.valid_referral)
        self.serializer_invalid_referral = ReferralSerializer(
            data=self.invalid_referral)

    def test_referral_serializer_validation(self):
        """
        Testing if the referral serializer gives the correct errors 
        or invalid data input
        """

        self.serializer_valid_referral.is_valid()
        self.serializer_invalid_referral.is_valid()

        self.assertEqual(self.serializer_valid_referral.is_valid(), True)
        self.assertEqual(self.serializer_invalid_referral.is_valid(), False)

    def test_referral_serializer_errors(self):
        """
        Testing if the client serializer gives the correct errors 
        for invalid data input
        """

        self.serializer_invalid_referral.is_valid()

        self.assertIn(
            'source_cpf', self.serializer_invalid_referral.errors.keys())
        self.assertIn(
            'target_cpf', self.serializer_invalid_referral.errors.keys())


class TestReferralModel(TestCase):
    """
    Test class for unit testing the Referral model
    """

    @classmethod
    def setUpTestData(cls):
        cls.referral = Referral.objects.create(
            source_cpf="11987098390",
            target_cpf="51805510649",
            status=False
        )

    def test_create_referral(self):
        """
        Testing if a referral (assuming their serializer is valid, as per the 
        previous test class) is correctly created, with the respective fields
        """

        created_referral = Referral.objects.first()

        self.assertEqual(Referral.objects.count(), 1)

        self.assertEqual(created_referral.source_cpf, '11987098390')
        self.assertEqual(created_referral.target_cpf, '51805510649')
        self.assertEqual(created_referral.status, False)
        self.assertIsNotNone(created_referral.created_at)
        self.assertIsNotNone(created_referral.updated_at)
