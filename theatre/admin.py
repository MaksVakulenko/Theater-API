from django.contrib import admin
from .models import (
    TheatreHall,
    Play,
    Actor,
    Genre,
    Performance,
    Reservation,
)


@admin.register(TheatreHall)
class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ["name", "rows", "seats_in_row"]
    search_fields = ["name"]


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ["title"]
    filter_horizontal = ["actors", "genres"]
    search_fields = ["title"]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ["play", "theatre_hall", "show_time"]
    list_filter = ["show_time", "theatre_hall"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    list_filter = ["created_at"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "full_name")
    search_fields = ("first_name", "last_name")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
