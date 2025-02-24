from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Play, Performance, TheatreHall
from theatre.serializers import PlaySerializer, PerformanceSerializer, PerformanceListSerializer
from datetime import datetime


class PlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin123",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_play(self):
        payload = {
            "title": "Hamlet",
            "description": "Classic Shakespeare tragedy",
            "actors": [],
            "genres": []
        }
        response = self.client.post("/api/theatre/plays/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Play.objects.get().title, "Hamlet")

    def test_retrieve_play(self):
        play = Play.objects.create(
            title="Romeo and Juliet",
            description="Classic love story"
        )
        response = self.client.get(f"/api/theatre/plays/{play.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], play.title)

    def test_update_play(self):
        play = Play.objects.create(
            title="Macbeth",
            description="Original description"
        )
        payload = {"description": "Updated description"}

        response = self.client.patch(
            f"/api/theatre/plays/{play.id}/",
            payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Play.objects.get(id=play.id).description,
            "Updated description"
        )

    def test_delete_play(self):
        play = Play.objects.create(
            title="Hamlet",
            description="Test description"
        )
        response = self.client.delete(f"/api/theatre/plays/{play.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Play.objects.count(), 0)

    def test_validation_error(self):
        payload = {
            "title": "",
            "description": "Test description"
        }
        response = self.client.post("/api/theatre/plays/", payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PerformanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin123",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

        self.play = Play.objects.create(
            title="Test Play",
            description="Test Description"
        )
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall",
            rows=10,
            seats_in_row=10
        )
        self.base_performance_data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2024-03-10T19:00:00Z"
        }

    def test_create_performance(self):
        response = self.client.post(
            "/api/theatre/performances/",
            self.base_performance_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Performance.objects.count(), 1)

    def test_list_performances(self):
        Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-10T19:00:00Z"
        )
        response = self.client.get("/api/theatre/performances/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_performance(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-10T19:00:00Z"
        )
        response = self.client.get(
            f"/api/theatre/performances/{performance.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], performance.id)

    def test_update_performance(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-10T19:00:00Z"
        )
        updated_data = self.base_performance_data.copy()
        updated_data["show_time"] = "2024-03-11T20:00:00Z"

        response = self.client.put(
            f"/api/theatre/performances/{performance.id}/",
            updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["show_time"],
            "2024-03-11T20:00:00Z"
        )

    def test_delete_performance(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-10T19:00:00Z"
        )
        response = self.client.delete(
            f"/api/theatre/performances/{performance.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Performance.objects.count(), 0)
