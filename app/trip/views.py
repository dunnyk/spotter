from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Trip, ELDLog
from .serializers import TripSerializer
from .helper import SpotterHelper
from django.http import HttpResponse


def test(request):
    return HttpResponse({"Testing the app health"})


class TripViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def create(self, request, *args, **kwargs):
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = serializer.save()

        # Here is where you call the route calculation and ELD generation logic
        spotter = SpotterHelper(trip)
        trip_data = spotter.aggregator()
        trip.stops = trip_data.get("route").get("stops").get("fuel")
        trip.rests = trip_data.get("route").get("stops").get("rest")
        trip.metadata = trip_data
        trip.save()

        logs_data = trip_data.get("eld_data").get("daily_logs")
        for log in logs_data:
            daily_log = {
                "distance": log.get("distance"),
                "day_number": log.get("day_number"),
                "rest_hours": log.get("off_duty"),
                "driving_hours": log.get("driving"),
            }
            ELDLog.objects.create(trip=trip, **daily_log)

        # Re-serialize with updated data
        # response_data = TripSerializer(trip).data
        return Response(trip_data, status=status.HTTP_201_CREATED)
