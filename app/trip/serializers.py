from rest_framework import serializers
from .models import Trip, ELDLog


class ELDLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ELDLog
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    eld_logs = ELDLogSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "current_location",
            "pickup_location",
            "dropoff_location",
            "current_cycle",
            "cycle_days",
            "fuel_interval_miles",
            "pickup_dropoff_time_hours",
            "metadata",
            "eld_logs",
        ]
