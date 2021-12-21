"""
This file contais the views for the project's endpoints. 
All classes and methods have their own docstring documentation with a 
brief description of how they work. For detailed documentation and examples
of how the API deals with invalid or bad requests, please refer to the 
Postman documentation, linked in the repository README.md file.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client, Referral
from .serializers import ClientSerializer, ReferralSerializer


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
                "cpf": "12631049675",
                "name": "Teresa Seabra Antunes",
                "phone": "31992818778",
                "email": "tseabra.antunes@gmail.com",
                "created_at": "2021-12-20T20:10:34.538825-03:00",
                "updated_at": "2021-12-21T12:01:53.208761-03:00",
                "points": 0
            }
        """
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
                "cpf": "12631049675",
                "name": "Teresa Seabra Antunes",
                "phone": "31992818778",
                "email": "tseabra.antunes@gmail.com"
            }

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                "Updated user:": {
                    "cpf": "12631049675",
                    "name": "Teresa Seabra Antunes",
                    "phone": "31992818778",
                    "email": "tseabra.antunes@gmail.com",
                    "created_at": "2021-12-20T20:10:34.538825-03:00",
                    "updated_at": "2021-12-21T13:57:52.904942-03:00",
                    "points": 0
                }
            }
        """
        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Updated user:': serializer.data}, status=status.HTTP_200_OK)
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
            "updated_at": "2021-12-21T15:22:23.097652-03:00",
            "status": false
            },
            ...
        ]
    """
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
                "id": 1,
                "source_cpf": "12631049675",
                "target_cpf": "51805510649",
                "created_at": "2021-12-21T15:22:23.097487-03:00",
                "updated_at": "2021-12-21T15:22:23.097652-03:00",
                "status": false
            },
            ...
        ]
        """

        is_client_on_db = Client.objects.filter(cpf=cpf).exists()
        if is_client_on_db:
            if Referral.objects.filter(source_cpf=cpf).exists():
                referrals = Referral.objects.filter(source_cpf=cpf)
                serializer = ReferralSerializer(referrals, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(["User doesn't have registered referrals"], status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(["User not on database"], status=status.HTTP_404_NOT_FOUND)


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
                "updated_at": "2021-12-21T15:22:23.097652-03:00",
                "status": false
            },
        """

        if Referral.objects.filter(target_cpf=cpf).exists():
            referrals = Referral.objects.filter(target_cpf=cpf)
            serializer = ReferralSerializer(referrals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(["No active referral towards this person."], status=status.HTTP_404_NOT_FOUND)