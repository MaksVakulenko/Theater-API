from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Genre, Actor, TheatreHall
from theatre.serializers import GenreSerializer, ActorSerializer, TheatreHallSerializer


class GenreTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin123",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_genre(self):
        payload = {"name": "Drama"}
        response = self.client.post("/api/theatre/genres/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.get().name, "Drama")

    def test_list_genres(self):
        Genre.objects.create(name="Comedy")
        Genre.objects.create(name="Tragedy")

        response = self.client.get("/api/theatre/genres/")
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ActorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin123",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_actor(self):
        payload = {
            "first_name": "Tom",
            "last_name": "Cruise"
        }
        response = self.client.post("/api/theatre/actors/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        actor = Actor.objects.get()
        self.assertEqual(actor.first_name, "Tom")
        self.assertEqual(actor.last_name, "Cruise")

    def test_list_actors(self):
        Actor.objects.create(first_name="Brad", last_name="Pitt")
        Actor.objects.create(first_name="Leonardo", last_name="DiCaprio")

        response = self.client.get("/api/theatre/actors/")
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class TheatreHallTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin123",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_theatre_hall(self):
        payload = {
            "name": "Main Hall",
            "rows": 20,
            "seats_in_row": 25
        }
        response = self.client.post("/api/theatre/theater-halls/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hall = TheatreHall.objects.get()
        self.assertEqual(hall.name, "Main Hall")
        self.assertEqual(hall.rows, 20)
        self.assertEqual(hall.seats_in_row, 25)

    def test_list_theatre_halls(self):
        TheatreHall.objects.create(name="Small Hall", rows=10, seats_in_row=15)
        TheatreHall.objects.create(name="VIP Hall", rows=5, seats_in_row=10)

        response = self.client.get("/api/theatre/theater-halls/")
        halls = TheatreHall.objects.all()
        serializer = TheatreHallSerializer(halls, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)