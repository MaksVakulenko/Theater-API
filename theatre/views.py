from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from theatre.models import (
    TheatreHall,
    Play,
    Actor,
    Genre,
    Performance,
    Reservation,
    Ticket,
)
from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly
from theatre.serializers import (
    TheatreHallSerializer,
    PlaySerializer,
    ActorSerializer,
    GenreSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ReservationListSerializer,
    ReservationDetailSerializer,
)


class TheatreHallViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlayViewSet(viewsets.ModelViewSet):
    """
    List all plays, or retrieve a single play by title.
    Optionally, filter by title, genres(id), or actors(id).
    """

    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='title', type=str),
            OpenApiParameter(name='genres', type=str),
            OpenApiParameter(name='actors', type=str),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
            Returns filtered queryset based on query parameters:
            - title: Filter by play title
            - genres: Filter by genre IDs (comma-separated)
            - actors: Filter by actor IDs (comma-separated)
        """
        return super().list(request, *args, **kwargs)

    def get_queryset(self):

        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        if title:
            return self.queryset.filter(title__icontains=title)
        if genres:
            genres_ids = self._params_to_ints(genres)
            return self.queryset.filter(genres__id__in=genres_ids)
        if actors:
            actors_ids = self._params_to_ints(actors)
            return self.queryset.filter(actors__id__in=actors_ids)

        return self.queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .prefetch_related("tickets")
        .annotate(
            available_seats=(
                    F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                    - Count("tickets")
            )
        )
    )
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='date', type=str),
            OpenApiParameter(name='play', type=int),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Returns filtered queryset based on query parameters:
            - date: Filter by date str
            - play: Filter by play IDs (comma-separated)
        """
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        date = self.request.query_params.get("date")
        play_id_str = self.request.query_params.get("play")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if play_id_str:
            queryset = queryset.filter(play_id=int(play_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__performance__play", "tickets__performance__theatre_hall"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "tickets__performance__play",
            "tickets__performance__theatre_hall"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        if self.action == "retrieve":
            return ReservationDetailSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
