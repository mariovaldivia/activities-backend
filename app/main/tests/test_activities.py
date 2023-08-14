""" Customer tests """
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Customer, Activity

USER_MODEL = get_user_model()


class ActivityTests(APITestCase):

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
        self.customer_2 = Customer.objects.create(
            name='Minera Zaldivar',
            identification='1133554422',
            address="Av Prat 4343, Antofagasta"
        )
        self.activity_id = None

    def test_activity_list(self):
        """ """
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.force_login(self.user)
        url = reverse('main:activities-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)

    def test_activity_creation(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.force_login(self.user)
        data = {
            'description': 'test activity',
            'detail': 'Esta es una actividad de prueba',
            'customer': self.customer_1.id,
            'start': '2023-01-10',
            'finish': '2023-01-10',
        }
        url = reverse('main:activities-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by'], self.user.id)
        self.assertEqual(response.data['status'], 'R')


        self.activity_id = response.data['id']
        url = reverse('main:activities-add-worker',
                      kwargs={'pk': response.data['id']})
        data = {
            'worker': self.user.id,
            'role': 'supervisor'
        }
        response = self.client.post(url, data=data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data['created_by'], self.user.id)

        url = reverse('main:activities-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # def test_add_worker(self):
    #     """ Add worker to activity created """
    #     print(self.activity_id)

    def test_activity_incorrect_date(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        # self.client.force_login(self.user)
        data = {
            'description': 'test activity',
            'customer': self.customer_1.id,
            'start': '2023-01-10',
            'finish': '2023-01-01',
        }
        url = reverse('main:activities-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data['created_by'], self.user.id)
