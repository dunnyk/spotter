import math
import polyline
import requests
from typing import List, Tuple

from rest_framework.serializers import ValidationError

from app import settings

API_KEY = settings.API_KEY
FUELING_MILEAGE = 100
DRIVING_LIMIT_HRS = 10


class SpotterHelper:
    def __init__(self, trip):
        self.trip = trip
        self.current_cycle = trip.current_cycle
        self.current_location = trip.current_location
        self.pickup_location = trip.pickup_location
        self.dropoff_location = trip.dropoff_location

    def distance_covered(
        self, coord1: Tuple[float, float], coord2: Tuple[float, float]
    ) -> float:
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return 3958.8 * c

    def get_decoded_geometry(self, encoded_polyline: str) -> List[Tuple[float, float]]:
        """
            Decode a Google Maps encoded polyline into a list of latitude-longitude coordinate tuples.
        Args:
            encoded_polyline (str): The encoded polyline string representing a series of geographic coordinates.

        Returns:
            List[Tuple[float, float]]: A list of (latitude, longitude) tuples representing the decoded path.
        """
        return polyline.decode(encoded_polyline)

    def calculate_points_along_route(
        self,
        geometry: List[Tuple[float, float]],
        target_distances: List[float],
        label: str,
    ) -> List[dict]:
        """
        Calculate coordinates for points along route at specified distances
        Returns list of {coordinates, distance_from_start, label, [day]}
        """
        points = []
        if len(geometry) < 2 or not target_distances:
            return points

        current_distance = 0.0
        target_index = 0
        current_target = target_distances[target_index]

        for i in range(len(geometry) - 1):
            coord1 = geometry[i]
            coord2 = geometry[i + 1]
            segment_dist = self.distance_covered(coord1, coord2)
            segment_remaining = segment_dist

            while (
                current_distance + segment_remaining >= current_target
                and target_index < len(target_distances)
            ):
                # Calculate position along the segment
                needed = current_target - current_distance
                fraction = needed / segment_dist
                lat = coord1[0] + fraction * (coord2[0] - coord1[0])
                lng = coord1[1] + fraction * (coord2[1] - coord1[1])

                point = {
                    "coordinates": (round(lat, 6), round(lng, 6)),
                    "distance_from_start": round(current_target, 2),
                    "type": label,
                }

                # Add day number for rest stops
                if label == "rest":
                    point["day"] = target_index + 1

                points.append(point)

                target_index += 1
                if target_index >= len(target_distances):
                    break
                current_target = target_distances[target_index]

            current_distance += segment_dist
            if target_index >= len(target_distances):
                break

        return points

    def calculate_eld_data(
        self,
        current_cycle: float,
        total_on_duty: float,
        duration_hr: float,
        distance_mi: float,
    ) -> Tuple[List[dict], List[float], str]:
        """
        Calculate ELD (Electronic Logging Device) compliance data, including
        daily logs, rest stop distances, and duty status for a given driving
        session.
        Args:
            current_cycle (float): The driver's current accumulated cycle
            hours.Total_on_duty (float): The total on-duty hours before the
            trip.
            Duration_hr (float): The total duration of the trip in hours.
            distance_mi (float): The total distance covered in miles.

        Returns:
            Tuple[List[dict], List[float], str]:
                - A list of dictionaries containing daily driving details,
                    on-duty, and off-duty hours.
                - A list of cumulative distances at rest stops.
                - A string message if the trip exceeds the 70-hour compliance
                    limit, otherwise None.
        """
        if current_cycle + total_on_duty > 70:
            return [], [], "Exceeds 70-hour limit"

        days = []
        remaining_drive = duration_hr
        avg_speed = distance_mi / duration_hr if duration_hr > 0 else 0
        cumulative_dist = 0.0
        rest_distances = []

        while remaining_drive > 0:
            drive = min(remaining_drive, DRIVING_LIMIT_HRS)
            dist = drive * avg_speed
            cumulative_dist += dist

            days.append({"driving": round(drive, 2), "distance": round(dist, 2)})
            remaining_drive -= drive

            # Record rest stop distance (except last day)
            if remaining_drive > 0:
                rest_distances.append(round(cumulative_dist, 2))

        # Add duty calculations
        for i, day in enumerate(days):
            pickup = 1 if i == 0 else 0
            dropoff = 1 if i == len(days) - 1 else 0
            on_duty = day["driving"] + pickup + dropoff
            break_hr = 0.5 if day["driving"] >= 8 else 0
            day["on_duty"] = round(on_duty, 2)
            day["off_duty"] = round(break_hr + 10, 2)
            day["day_number"] = i + 1

        return days, rest_distances, None

    def aggregator(self):
        """
        Aggregates route, fuel stops, and ELD data.

        Retrieves route data from OpenRouteService, calculates fuel stops,
        estimates ELD compliance, and returns a structured response.

        Returns:
            dict: Route details, fuel/rest stops, and ELD data.
        """

        try:
            # Get route data from OpenRouteService
            url = "https://api.openrouteservice.org/v2/directions/driving-car"
            headers = {
                "Authorization": API_KEY,
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "POST",
            }
            coordinates = [
                self.current_location,
                self.pickup_location,
                self.dropoff_location,
            ]
            body = {"coordinates": coordinates, "instructions": "false"}
            response = requests.post(url, json=body, headers=headers)

            if response.status_code != 200:
                raise ValidationError("Route calculation failed")

            route_data = response.json()
            route = route_data["routes"][0]

            geometry = self.get_decoded_geometry(route["geometry"])

            # Convert units
            distance_m = route["summary"]["distance"]
            duration_s = route["summary"]["duration"]
            distance_mi = distance_m * 0.000621371
            duration_hr = duration_s / 3600

            # Calculate fuel stops
            fuel_stops_count = int(distance_mi // FUELING_MILEAGE)
            fuel_distances = [
                FUELING_MILEAGE * (i + 1) for i in range(fuel_stops_count)
            ]

            fuel_stops = self.calculate_points_along_route(
                geometry, fuel_distances, "fuel"
            )

            # Calculate ELD data and rest stops
            total_on_duty = duration_hr + 2  # +2 for pickup/dropoff
            daily_logs, rest_distances, error = self.calculate_eld_data(
                self.current_cycle, total_on_duty, duration_hr, distance_mi
            )

            if error:
                raise ValidationError(error)

            rest_stops = self.calculate_points_along_route(
                geometry, rest_distances, "rest"
            )

            # Build response
            response_data = {
                "route": {
                    "geometry": [
                        [round(lat, 6), round(lon, 6)] for lat, lon in geometry
                    ],
                    "waypoints": [
                        {"type": "current", "coordinates": self.current_location},
                        {"type": "pickup", "coordinates": self.pickup_location},
                        {"type": "dropoff", "coordinates": self.dropoff_location},
                    ],
                    "stops": {"fuel": fuel_stops, "rest": rest_stops},
                    "summary": {
                        "total_distance": round(distance_mi, 2),
                        "total_duration": round(duration_hr, 2),
                        "fuel_stops": fuel_stops_count,
                        "rest_stops": len(rest_stops),
                    },
                },
                "eld_data": {
                    "daily_logs": daily_logs,
                    "remaining_hours": round(
                        70 - (self.current_cycle + total_on_duty), 2
                    ),
                    "total_on_duty": round(total_on_duty, 2),
                },
            }

            return response_data
        except Exception as e:
            str(e)
