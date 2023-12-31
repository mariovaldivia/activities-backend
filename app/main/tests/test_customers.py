""" Customer tests """
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Customer
USER_MODEL = get_user_model()

class CustomerTests(APITestCase):

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username='mvaldivia',
            email="mvaldivia@nbeta.cl",
            password='123456',
        )
        customer_1 = Customer.objects.create(
            name='BHP Escondida',
            identification='1122334455',
            address="Av Balmaceda 111, Antofagasta"
        )
        customer_2 = Customer.objects.create(
            name='Minera Zaldivar',
            identification='1133554422',
            address="Av Prat 4343, Antofagasta"
        )

    def test_customer_list(self):
        """ """
        url = reverse('main:customers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_customer_creation(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.force_login(self.user)
        data = {
            'name': 'Pucobre',
            'identification': 'AB123456',
            'address': 'Copayapu 2342'

        }
        url = reverse('main:customers-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

