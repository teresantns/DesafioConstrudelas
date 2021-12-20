from rest_framework import serializers
from .models import Client, Referral


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client class.
    """
    class Meta:
        model = Client
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    """
    Serializer for the Referral class.
    """
    class Meta:
        model = Referral
        fields = '__all__'
