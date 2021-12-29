"""
Utilities being used in our tests. We have a function to generate random
valid CPF numbers, a function that creates a valid client in the database,
and a function to create referrals.
"""
from ..models import Client, Referral


def generate_valid_cpf():
    """
    This function generates a random valid CPF. We are going to use it for populating the
    tables and testing our API. (return cpf in string format)
    """
    from random import randint
    numero = str(randint(100000000, 999999999))
    # variável que vamos criar para conferir o cpf (tirando os dois últimos digitos)
    novo_cpf = numero
    cpf_lista = [int(i) for i in novo_cpf]

    maxs = 10
    while True:
        soma = 0
        for n, r in enumerate(range(maxs, 1, -1)):
            soma += r * cpf_lista[n]

        d = 0 if (11 - (soma % 11)) > 9 else (11 - (soma % 11))

        novo_cpf += str(d)  # colocando o digito novo no cpf
        cpf_lista.append(d)  # colocando o digito na lista do cpf
        if len(novo_cpf) < 11:
            maxs += 1  # aumentando o range do for para 11
            continue
        return novo_cpf


def create_user():
    """
    Creates a standard client we will use for our tests. Note that
    we know that this is a valid client, with a valid serializer.
    """
    return Client.objects.create(
        cpf="11987098390",
        name="Luisa Souza",
        phone="31998877554",
        email="luisa@gmail.com"
    )

def create_referral():
    """
    Creates a referral from our stardard client to a random valid CPF.
    """

    return Referral.objects.create(
        source_cpf="11987098390",
        target_cpf=generate_valid_cpf(),
        status=False
    )