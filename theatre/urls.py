from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    TheatreHallViewSet,
    PlayViewSet,
    ActorViewSet,
    GenreViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)


router = routers.DefaultRouter()
router.register("theater-halls", TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre"
