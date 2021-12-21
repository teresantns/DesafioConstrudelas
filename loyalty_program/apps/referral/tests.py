from django.shortcuts import get_object_or_404
from django.test import TestCase
from .models import Client

# Create your tests here.

cpf = '12531049675'
is_client_on_db = get_object_or_404(Client, cpf=cpf)
print(is_client_on_db)
