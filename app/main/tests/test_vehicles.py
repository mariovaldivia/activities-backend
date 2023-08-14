""" Vehicle tests """
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import Vehicle, VehicleType

USER_MODEL = get_user_model()

class VehicleTests(APITestCase):

    def setUp(self):
        self.user = USER_MODEL.objects.create_user(
            username='mvaldivia',
            email="mvaldivia@nbeta.cl",
            password='123456',
        )
        self.camioneta = VehicleType.objects.create(name='Camioneta')

    def test_vehicles_list(self):
        """ """
        url = reverse('main:vehicles-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

    def test_vehicle_creation(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.force_login(self.user)
        data = {
            'type': self.camioneta.id,
            'brand': 'Toyota',
            'model': 'Hilux',
            'plate': 'AABB12'
        }
        url = reverse('main:vehicles-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type'], self.camioneta.id)
