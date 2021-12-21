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
        - The ID specified on the url;

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
