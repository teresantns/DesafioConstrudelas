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
                "cpf": "a valid cpf",
                "name": "some name",
                "phone": "some telephone number",
                "email": "some valid email",
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
                "cpf": "a valid cpf",
                "name": "some name",
                "phone": "some telephone number",
                "email": "some valid email"
            }

        It returns:
        - HTTP status = 200;
        - A JSON like this:
            {
                "Updated user:": {
                    "cpf": "a valid cpf",
                    "name": "some name",
                    "phone": "some telephone number",
                    "email": "some valid email",
                    "created_at": "2021-12-20T20:10:34.538825-03:00",
                    "updated_at": "2021-12-21T13:57:52.904942-03:00",
                    "points": 0
                }
            }
        """
        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if cpf == request.data['cpf']:
                serializer.save()
                return Response({'Updated user:': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "cannot change user CPF"}, status=status.HTTP_400_BAD_REQUEST)
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
            "source_cpf": "a valid cpf",
            "target_cpf": "another valid cpf",
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
                "source_cpf": "cpf on url",
                "target_cpf": "another valid cpf",
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
                return Response(["error: User doesn't have registered referrals"], status=status.HTTP_404_NOT_FOUND)
        else:
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
                "source_cpf": "a valid cpf",
                "target_cpf": "cpf on url",
                "created_at": "2021-12-21T15:22:23.097487-03:00",
                "updated_at": "2021-12-21T15:22:23.097652-03:00",
                "status": false
            }
        """

        if Referral.objects.filter(target_cpf=cpf).exists():
            referrals = Referral.objects.filter(target_cpf=cpf)
            serializer = ReferralSerializer(referrals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
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
        return Response(["waiting on referral creation"], status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a referral.

        It expects:
        - POST as http method;
        - A JSON like this:
        {
            "source_cpf": "a valid cpf",
            "target_cpf": "another valid cpf",
            "status": false
        }

        It returns:
        - HTTP status = 201;
        - A JSON like this:
            {
                "id": 1,
                "source_cpf": "a valid cpf",
                "target_cpf": "another valid cpf",
                "created_at": "2021-12-21T15:22:23.097487-03:00",
                "updated_at": "2021-12-21T15:22:23.097652-03:00",
                "status": false
            }
        """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if Client.objects.filter(cpf=request.data['source_cpf']).exists():
                if request.data['source_cpf'] == request.data['target_cpf']:
                    return Response(["error: User cannot refer themselves"], status=status.HTTP_400_BAD_REQUEST)

                else:
                    if Client.objects.filter(cpf=request.data['target_cpf']).exists():
                        return Response(["error: Referred person is already registered"],
                                        status=status.HTTP_400_BAD_REQUEST)

                    else:
                        serializer.save()
                        return Response({"Referral registered": serializer.data}, status=status.HTTP_201_CREATED)

            else:
                return Response(["error: User must be registered to make a referral"], status=status.HTTP_404_NOT_FOUND)

        elif Referral.objects.filter(target_cpf=request.data['target_cpf']).exists() and serializer.is_valid():
            return Response("error: This person was already referred.",
                            status=status.HTTP_400_BAD_REQUEST)

        else:
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
        docstring here!
        """

        if Referral.objects.filter(target_cpf=cpf).exists():
            referrals = Referral.objects.filter(target_cpf=cpf)
            serializer = ReferralSerializer(referrals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No active referral registered for this CPF"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, cpf):
        """
        docstring goes here
        """
        referral = Referral.objects.get(target_cpf=cpf)
        serializer = ReferralSerializer(referral, data=request.data, partial=True)

        if serializer.is_valid():
            # if request.data[status] == True:
            #     pass  # add conditions for cpf fields -- or make them by default non editable or read only??

            serializer.save()
            return Response({'Updated referral:': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
