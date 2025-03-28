from django.db import models


class Trip(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    current_location = models.JSONField()
    pickup_location = models.JSONField()
    dropoff_location = models.JSONField()

    # Cycle hours (e.g., 70h/8days)
    current_cycle = models.IntegerField(default=70)
    cycle_days = models.IntegerField(default=8)

    # Additional assumptions
    # e.g. fueling, pickup/dropoff times, etc.
    fuel_interval_miles = models.IntegerField(default=1000)
    pickup_dropoff_time_hours = models.FloatField(default=1.0)
    rests = models.JSONField(null=True, blank=True)
    stops = models.JSONField(null=True, blank=True)

    # This could be used to store a JSON of route details from the external API
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Trip {self.id} from {self.pickup_location} to {self.dropoff_location}"


class ELDLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="eld_logs")
    date = models.DateField(auto_now=True)
    driving_hours = models.FloatField(null=True)
    rest_hours = models.FloatField(null=True)
    day_number = models.IntegerField(null=True)
    distance = models.FloatField(null=True)

    # Additional fields if necessary (off-duty, sleeper berth, etc.)

    def __str__(self):
        return f"ELD Log for Trip {self.trip.id} on {self.date}"
