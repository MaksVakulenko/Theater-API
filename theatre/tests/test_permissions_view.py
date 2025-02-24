from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Play, Performance, TheatreHall


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="userpass123"
        )
        self.admin_user = get_user_model().objects.create_user(
            email="admin@test.com",
            password="adminpass123",
            is_staff=True
        )

        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall",
            rows=10,
            seats_in_row=10
        )
        self.play = Play.objects.create(
            title="Test Play",
            description="Test Description"
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-10T19:00:00Z"
        )

    def test_plays_endpoint_authentication(self):
        response = self.client.get("/api/theatre/plays/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/theatre/plays/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("/api/theatre/plays/", {
            "title": "New Play",
            "description": "Description"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/theatre/plays/", {
            "title": "Admin Play",
            "description": "Description"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_performances_endpoint_authentication(self):
        response = self.client.get("/api/theatre/performances/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/theatre/performances/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservations_endpoint_authentication(self):
        response = self.client.get("/api/theatre/reservations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/theatre/reservations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)