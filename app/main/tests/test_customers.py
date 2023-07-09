""" Customer tests """
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Customer

class CustomerTests(APITestCase):

    def setUp(self):
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
