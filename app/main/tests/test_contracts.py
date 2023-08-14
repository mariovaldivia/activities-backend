""" Contracts tests """
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Customer, Contract
USER_MODEL = get_user_model()

class CustomerTests(APITestCase):

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username='mvaldivia',
            email="mvaldivia@nbeta.cl",
            password='123456',
        )
        self.customer_1 = Customer.objects.create(
            name='BHP Escondida',
            identification='1122334455',
            address="Av Balmaceda 111, Antofagasta"
        )
        customer_2 = Customer.objects.create(
            name='Minera Zaldivar',
            identification='1133554422',
            address="Av Prat 4343, Antofagasta"
        )

    def test_contracts_list(self):
        """ """
        url = reverse('main:contracts-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_contract_creation(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.force_login(self.user)
        data = {
            'customer': self.customer_1.id,
            'description': 'Instalacion equipos',
            'identification': 'ABC1234',
            'detail': 'Instalacion de equipos de comunicaciones',
            'start': '2023-08-01',
            'finish': '2023-12-31'

        }
        url = reverse('main:contracts-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_name'], self.customer_1.name)

        data = {
            'customer': self.customer_1.id,
            'description': 'puesta en marcha de sistema',
            'identification': 'ABC1234',
            'detail': 'puesta en marcha de sistema de comunicaciones',
            'start': '2023-08-01',
            'finish': '2023-12-31'

        }
        url = reverse('main:contracts-list')
        response = self.client.post(url, data=data, format='json')
        # print(response.data['identification'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['customer_name'], self.customer_1.name)
