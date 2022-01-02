"""
This file contais the views for the project's endpoints. 
All classes and methods have their own docstring documentation with a 
brief description of how they work. For detailed documentation and examples
of how the API deals with invalid or bad requests, please refer to the 
Postman documentation, linked in the repository README.md file.
"""

from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response

from .models import Client, Referral
from .serializers import ClientSerializer, ReferralSerializer
from .utils import delete_referrals_older_than_30_days

import logging
logger = logging.getLogger(__name__)


class MainPage(generics.ListAPIView):
    """
    Description of API endpoints according to their function. 
    """
    """
    This is only so that the local host endpoint gives information on 
    the API endpoints, which are more detailed on the documentation.
    """

    def get(self, request):
        urls = {'User detail and update': 'user/<str:cpf>/',
                'List of all referrals registered': 'all-referrals/',
                'List of all referrals performed by an user registered': 'all-referrals/<str:cpf>/',
                'Information on specific referral': 'referral/<str:cpf>/',
                'Create new referral': 'create-referral/',
                'Accept specific referral': 'accept-referral/<str:cpf>/',
                }
        logger.info("Received request to get the main page.")
        return Response(urls, status=status.HTTP_200_OK)


class CreateUserView(generics.ListCreateAPIView):
    """
    Creates a new client, with the requested data
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request):
        """
        It expects:
        - GET as http method;
        
        It returns:
        - HTTP status = 200;
        - A message like this:
            [
                "waiting on client creation"
            ]
        """

        logger.info("Waiting for user to create new client.")
        return Response(["waiting on client creation"], status=status.HTTP_200_OK)

    
    def post(self, request):
        """
        Creates a new user
        
        It expects:
            - POST as http method;
            - A JSON like this:
            {
                "cpf": "94353687433",
                "name": "José Coelho",
                "phone": "11956555877",
                "email": "jose.coelho@gmail.com"
            }
        
        It returns:
             - HTTP status = 201;
             - A JSON like this:
               {
                    "Created user:": {
                        "cpf": "94353687433",
                        "name": "José Coelho",
                        "phone": "11956555877",
                        "email": "jose.coelho@gmail.com",
                        "created_at": "2022-01-02T18:23:36.749961-03:00",
                        "updated_at": "2022-01-02T18:23:36.750023-03:00",
                        "points": 0
                    }
                }
        """

        request_data = request.data
        logger.info(
            "Received a request to create a new client with the following data: %s:", request_data)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if request.data['cpf'].isalnum():
                serializer.save()
                logger.info(
                        "Requested data is valid, created the user and returning 201!")
                return Response({'Created user:': serializer.data}, status=status.HTTP_200_OK)
            
            logger.info("CPF is not all numeric, returning 400.")
            return Response({'Error': 'Please enter CPF just with numbers.'}, status=status.HTTP_400_BAD_REQUEST)

        
        logger.warning("Received data is invalid, returning 400 and the errors.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(generics.RetrieveUpdateAPIView):
    """
    Gets and/or change the data of a specific user.
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'cpf'

    def get(self, request, cpf):
        """
        Gets the data of a specific user.

        It expects:
        - GET as http method;
        - The CPF specified on the url;

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                "cpf": "11987098390",
                "name": "Luisa Souza",
                "phone": "31998877554",
                "email": "luisa@gmail.com",
                "created_at": "2021-12-22T18:31:48.327319-03:00",
                "updated_at": "2021-12-22T18:39:51.509125-03:00",
                "points": 0
            }
        """

        logger.info("Received a request to fetch a specific User")

        user = get_object_or_404(Client, cpf=cpf)
        serializer = ClientSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, cpf):
        """
        Saves the changes made for the requested user

        It expects:
        - PUT as http method;
        - The CPF specified on the url;
        - A JSON like this:
            {
                "cpf": "11987098390",
                "name": "Luisa Souza",
                "phone": "31998877554",
                "email": "luisa_souza@gmail.com"
            }

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                  "Updated user:": {
                    "cpf": "11987098390",
                    "name": "Luisa Souza",
                    "phone": "31998877554",
                    "email": "luisa_souza@gmail.com",
                    "created_at": "2021-12-22T18:31:48.327319-03:00",
                    "updated_at": "2021-12-24T15:42:27.480610-03:00",
                    "points": 0
                }
            }
        """

        request_data = request.data
        logger.info(
            "Received a request to update a specific User, with the following data: %s", request_data)

        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            if cpf == request.data['cpf']:
                serializer.save()
                logger.info(
                    "Requested data is valid, updating the user and returning 200!")
                return Response({'Updated user:': serializer.data}, status=status.HTTP_200_OK)
            else:
                logger.warning(
                    "User is trying to change their CPF, returning 400.")
                return Response({"error": "cannot change user CPF"}, status=status.HTTP_400_BAD_REQUEST)

        logger.warning("Received data is invalid, returning 400.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetReferralsView(generics.ListAPIView):
    """
    Gets the data of all referrals on database.
    """
    """
    It expects:
    - GET as http method;
    
    It returns:
    - HTTP status = 200;
    - A JSON like this:
        [
            {
                "id": 1,
                "source_cpf": "12631049675",
                "target_cpf": "51805510649",
                "created_at": "2021-12-21T15:22:23.097487-03:00",
                "updated_at": "2021-12-23T15:04:34.881831-03:00",
                "status": true
            },
            ...
        ]
    """

    logger.info("Received a request to fetch a list of all Referrals")

    delete_referrals_older_than_30_days()
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer


class GetUserReferralsView(generics.RetrieveAPIView):
    """
    Gets the data of all referrals on database made by specific user.
    """

    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    lookup_field = 'source_cpf'

    def get(self, request, cpf):
        """
        Returns a list of referrals performed by specific user.

        It expects:
        - GET as http method;
        - The CPF specified on the url;

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            [
            {
                "id": 3,
                "source_cpf": "52768135070",
                "target_cpf": "58874265786",
                "created_at": "2021-12-21T18:50:30.355478-03:00",
                "updated_at": "2021-12-21T18:50:30.355534-03:00",
                "status": false
            },
            ...
        ]
        """

        logger.info(
            "Received a request to fetch a list of all Referrals made by user: %s", cpf)

        delete_referrals_older_than_30_days()
        is_client_on_db = Client.objects.filter(cpf=cpf).exists()

        if is_client_on_db:
            if Referral.objects.filter(source_cpf=cpf).exists():
                referrals = Referral.objects.filter(source_cpf=cpf)
                serializer = ReferralSerializer(referrals, many=True)

                logger.info("Data checks, returning referrals and 200!")
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                logger.warning("User doesn't have referrals, returning 404.")
                return Response(["error: User doesn't have registered referrals"], status=status.HTTP_404_NOT_FOUND)
        else:
            logger.warning("User is not registered, returning 404.")
            return Response(["error: User not on database"], status=status.HTTP_404_NOT_FOUND)


class GetReferralView(generics.RetrieveAPIView):
    """
    Gets the data of a specific referral on database by the cpf of referred person.
    """

    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    lookup_field = 'target_cpf'

    def get(self, request, cpf):
        """
        Returns a specific referral made towards the person with the given cpf.

        It expects:
        - GET as http method;
        - The CPF specified on the url;

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                "id": 1,
                "source_cpf": "12631049675",
                "target_cpf": "51805510649",
                "created_at": "2021-12-21T15:22:23.097487-03:00",
                "updated_at": "2021-12-23T15:04:34.881831-03:00",
                "status": true
            }
        """

        logger.info("Received a request to fetch a specific Referral")
        delete_referrals_older_than_30_days()
        if Referral.objects.filter(target_cpf=cpf).exists():
            referrals = Referral.objects.filter(target_cpf=cpf)
            serializer = ReferralSerializer(referrals, many=True)

            logger.info("Data checks, returning referral and 200!")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.warning(
                "This person doesn't have active referrals, returning 404.")
            return Response(["error: No active referral towards this person."], status=status.HTTP_404_NOT_FOUND)


class CreateReferralView(generics.ListCreateAPIView):
    """
    Creates a Referral
    """

    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    def get(self, request):
        """
        It expects:
        - GET as http method;

        It returns:
        - HTTP status = 200;
        - A message like this:
            [
                "waiting on referral creation"
            ]
        """

        logger.info("Waiting for user to create a referral.")
        return Response(["waiting on referral creation"], status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a referral.

        It expects:
        - POST as http method;
        - A JSON like this:
        {
            "source_cpf": "12631049675",
            "target_cpf": "12262411239",
            "status": false
        }

        It returns:
        - HTTP status = 201;
        - A JSON like this:
            {
                "Referral registered": {
                    "id": 8,
                    "source_cpf": "12631049675",
                    "target_cpf": "12262411239",
                    "created_at": "2021-12-24T19:46:17.978403-03:00",
                    "updated_at": "2021-12-24T19:46:17.978446-03:00",
                    "status": false
                }
            }
        """

        request_data = request.data
        logger.info(
            "Received a request to create a referral with the following data: %s:", request_data)
        delete_referrals_older_than_30_days()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if Client.objects.filter(cpf=request.data['source_cpf']).exists():
                if request.data['source_cpf'] == request.data['target_cpf']:

                    logger.warning(
                        "User is trying to refer themselves, returning 400.")
                    return Response(["error: User cannot refer themselves"], status=status.HTTP_400_BAD_REQUEST)

                else:
                    if Client.objects.filter(cpf=request.data['target_cpf']).exists():

                        logger.warning(
                            "User is trying to refer someone who is already on database, returning 400.")
                        return Response(["error: Referred person is already registered"],
                                        status=status.HTTP_400_BAD_REQUEST)

                    else:
                        serializer.save()

                        logger.info(
                            "Data checks, creating referral and returning 201!")
                        return Response({"Referral registered": serializer.data}, status=status.HTTP_201_CREATED)

            else:
                logger.warning(
                    "Non-registered user is trying to refer someone, returning 400.")
                return Response(["error: User must be registered to make a referral"], status=status.HTTP_404_NOT_FOUND)

        elif Referral.objects.filter(target_cpf=request.data['target_cpf']).exists():
            logger.warning(
                "User is trying to refer someone with an active referral, returning 400.")
            return Response("error: This person was already referred.",
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            logger.warning("Requested data is invalid, returnin 400")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptReferralView(generics.RetrieveUpdateAPIView):
    """
    Gets and updates referral, allowing its acceptance.
    """

    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    lookup_field = 'target_cpf'

    def get(self, request, cpf):
        """
        Gets a specific referral, allowing its acceptance. The referred 
        person's CPF is passed on the URL path.

        It expects:
        - GET as http method;
        - The CPF specified on the url;

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                "id": 5,
                "source_cpf": "12631049675",
                "target_cpf": "10370335317",
                "created_at": "2021-12-21T23:36:47.608175-03:00",
                "updated_at": "2021-12-22T23:17:14.602338-03:00",
                "status": false
            }
        """

        logger.info("Received a request to fetch a specific Referral")
        delete_referrals_older_than_30_days()
        if Referral.objects.filter(target_cpf=cpf).exists():
            referrals = Referral.objects.get(target_cpf=cpf)
            serializer = ReferralSerializer(referrals)
            logger.info("Data checks, returning referral and 200!")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.warning("No referrals with this CPF, returning 404")
            return Response({"error": "No active referral registered for this CPF"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, cpf):
        """
        Updates the specified referral.

        It expects:
        - PUT as http method;
        - The CPF of reffered person specified on the url;
        - A JSON like this:
            {
                "id": 5,
                "source_cpf": "12631049675",
                "target_cpf": "10370335317",
                "status": true
            }

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                "Updated referral:": {
                    "id": 5,
                    "source_cpf": "12631049675",
                    "target_cpf": "10370335317",
                    "created_at": "2021-12-21T23:36:47.608175-03:00",
                    "updated_at": "2021-12-24T20:14:46.355914-03:00",
                    "status": true
                }
            }

        """

        request_data = request.data
        logger.info(
            "Received a request to update a specific User, with the following data: %s", request_data)

        referral = Referral.objects.get(target_cpf=cpf)
        serializer = ReferralSerializer(
            referral, data=request.data, partial=True)
        referrent = Client.objects.get(cpf=referral.source_cpf)
        updated_status = request.data['status']

        if serializer.is_valid():
            if request.data['target_cpf'] == cpf and request.data['source_cpf'] == referral.source_cpf:
                if updated_status:
                    with transaction.atomic():
                        """
                        Using atomic to ensure both actions will happen, or neither of them.
                        The number of points can be changed to be consistent with the existing point system
                        """
                        referrent.points += 10
                        referrent.save()
                        serializer.save()

                    logger.info(
                        "User accepted the referral! Giving points to referrer and returning 200!")
                    return Response({'Updated referral:': serializer.data}, status=status.HTTP_200_OK)

                else:
                    serializer.save()
                    logger.info("User didn't accept referral, returning 200.")
                    return Response({'Updated referral:': serializer.data}, status=status.HTTP_200_OK)

            else:
                logger.warning("User is trying to change CPFs, returning 400.")
                return Response({"error": "cannot change users CPF"}, status=status.HTTP_400_BAD_REQUEST)

        logger.warning("Requested data is invalid, returning 400.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
