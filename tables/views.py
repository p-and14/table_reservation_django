from rest_framework.generics import ListCreateAPIView, DestroyAPIView

from tables.models import Table, Reservation
from tables import serializers


class TableView(ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = serializers.TableSerializer


class TableDeleteView(DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = serializers.TableDeleteSerializer


class ReservationView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = serializers.ReservationSerializer


class ReservationDeleteView(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = serializers.ReservationDeleteSerializer
