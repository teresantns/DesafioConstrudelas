from django.db import models
from django.db import models
from localflavor.br.models import BRCPFField


class Client(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Nome')
    cpf = BRCPFField('CPF ', blank=False, primary_key=True, help_text='Formato: 00011122233')
    phone = models.CharField(max_length=11, blank=False,
                             help_text='Formato DDD + Número', verbose_name='Telefone')
    email = models.EmailField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    points = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        details = f'Cliente: {self.name} | cpf: {self.cpf}'
        return details


class Referral(models.Model):
    source_cpf = BRCPFField('CPF do usuário de origem',
                            blank=False, unique=False)
    target_cpf = BRCPFField('CPF do usuário de destino',
                            blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        details = f'Indicador: {self.source_cpf} | Indicado: {self.target_cpf}'
        return details
