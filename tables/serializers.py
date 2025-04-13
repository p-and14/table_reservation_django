from datetime import timedelta

from django.db.models import F, Q
from rest_framework import serializers

from tables.models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class TableDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
    
    def validate_duration_minutes(self, duration_minutes):
        if duration_minutes < 5:
            raise serializers.ValidationError(
                    "Минимальное время бронирования - 5 минут"
                )
        elif duration_minutes > 24 * 60:
            raise serializers.ValidationError(
                    "Максимальное время бронирования - 24 часа"
                )
        
        return duration_minutes
    
    def validate(self, attrs):
        reservation_time = attrs.get("reservation_time")
        duration_minutes = attrs.get("duration_minutes")
        table = attrs.get("table")
        reservations_overlap = Reservation.objects.filter(table_id=table).only(
            "reservation_time", "duration_minutes"
            ).filter(
            Q(reservation_time__gt=reservation_time - timedelta(minutes=1) * F("duration_minutes"))
            &
            Q(reservation_time__lt=reservation_time + timedelta(minutes=duration_minutes))).exists()

        if reservations_overlap:
            raise serializers.ValidationError(
                    {"duration_minutes": "Время занято. Попробуйте изменить время брони",
                     "reservation_time": "Время занято. Попробуйте изменить длительность брони"}
                )

        return attrs


class ReservationDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id"]
