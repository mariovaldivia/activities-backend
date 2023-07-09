""" Customer tests """
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Vehicle, VehicleType

class VehicleTests(APITestCase):

    def setUp(self):
        self.camioneta = VehicleType.objects.create(name='Camioneta')

    def test_customer_list(self):
        """ """
        url = reverse('main:customers-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
