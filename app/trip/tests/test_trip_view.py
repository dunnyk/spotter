from defer import return_value
from .base_test import TestBaseCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from unittest.mock import patch, Mock
from app.trip.tests.fixtures import SAMPLE_TRIP_DATA

# from rest_framework.response import Response


class MockRequest:
    status_code = 200

    @staticmethod
    def json():
        return SAMPLE_TRIP_DATA


class TripAPITest(TestBaseCase):

    @patch("requests.post", return_value=MockRequest)
    def test_create_trip(self, request_mock):
        """Test creating a trip successfully."""

        data = {
            "current_location": [36.812374486076045, -1.2760919692021566],
            "pickup_location": [35.26852461652837, 0.513816223317221],
            "dropoff_location": [39.664199789049384, -4.043061393609565],
            "current_cycle": 15,
        }

        response = self.client.post(self.create_trip_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Dict
        self.assertIsInstance(response.json(), dict)
        self.assertIn("geometry", response.json().get("route"))
