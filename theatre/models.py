from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seats_in_row = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    @property
    def total_seats(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField("Actor", blank=True)
    genres = models.ManyToManyField("Genre", blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    # def available_seats(self):
    #     total_seats = self.theatre_hall.rows * self.theatre_hall.seats_in_row
    #     booked_seats = self.tickets.count()
    #     return total_seats - booked_seats

    def __str__(self):
        # return f"{self.play.title} -
        # {self.show_time} (Available:
        # {self.available_seats()})"
        return f"{self.play.title} - {self.show_time}"


class Reservation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username}"


class Ticket(models.Model):
    row = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    seat = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("performance", "row", "seat")

    def __str__(self):
        return f"Ticket {self.id}: Row {self.row}, Seat {self.seat}"
