from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from theatre.models import Performance, TheatreHall, Play, Reservation, Ticket


class TicketReservationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

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

    def test_create_reservation_with_invalid_data(self):
        payload = {
            "tickets": [
                {
                    "row": self.theatre_hall.rows + 1,
                    "seat": 1,
                    "performance": self.performance.id
                }
            ]
        }

        response = self.client.post("/api/theatre/reservations/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reservations(self):
        reservation = Reservation.objects.create(user=self.user)
        ticket = Ticket.objects.create(
            reservation=reservation,
            performance=self.performance,
            row=1,
            seat=1
        )

        response = self.client.get("/api/theatre/reservations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(
            reservation=reservation,
            performance=self.performance,
            row=1,
            seat=1
        )

        response = self.client.get(f"/api/theatre/reservations/{reservation.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_seat_validation(self):
        payload = {
            "tickets": [
                {
                    "row": 20,
                    "seat": 1,
                    "performance": self.performance.id
                }
            ]
        }
        response = self.client.post("/api/theatre/reservations/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_ticket_validation(self):
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "performance": self.performance.id
                }
            ]
        }
        self.client.post("/api/theatre/reservations/", payload)

        response = self.client.post("/api/theatre/reservations/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
