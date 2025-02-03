from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserApiTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "password123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = "http://localhost:8000/api/login/"
        self.refresh_url = "http://localhost:8000/api/refresh/"
        self.logout_url = "http://localhost:8000/api/logout/"
        self.profile_url = "http://localhost:8000/api/me/"

    def test_register_user(self):
        url = "http://127.0.0.1:8000/api/register/"
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)
        self.assertIn('id', response.data)

    def test_login_user(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        refresh_token = str(refresh)
        response = self.client.post(self.refresh_url, {"refresh_token": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_invalid_refresh_token(self):
        response = self.client.post(self.refresh_url, {"refresh_token": "invalid_token"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        new_data = {"username": "new_username"}
        response = self.client.put(self.profile_url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, new_data['username'])

    def test_logout_user(self):
        refresh = RefreshToken.for_user(self.user)
        refresh_token = str(refresh)
        response = self.client.post(self.logout_url, {"refresh_token": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], "User logged out.")
