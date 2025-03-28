SAMPLE_TRIP_DATA = {
    "route": {
        "geometry": [[-1.27571, 36.81289], [-1.27566, 36.81285]],
        "waypoints": [
            {
                "type": "current",
                "coordinates": [36.812374486076045, -1.2760919692021566],
            },
            {"type": "pickup", "coordinates": [36.07746376202207, -0.3017346273660451]},
            {
                "type": "dropoff",
                "coordinates": [39.664199789049384, -4.043061393609565],
            },
        ],
        "stops": {
            "fuel": [
                {
                    "coordinates": [-0.284003, 36.101607],
                    "distance_from_start": 100,
                    "type": "fuel",
                },
                {
                    "coordinates": [-1.328826, 36.878912],
                    "distance_from_start": 200,
                    "type": "fuel",
                },
                {
                    "coordinates": [-2.287568, 37.82668],
                    "distance_from_start": 300,
                    "type": "fuel",
                },
                {
                    "coordinates": [-3.404432, 38.578556],
                    "distance_from_start": 400,
                    "type": "fuel",
                },
            ],
            "rest": [],
        },
        "summary": {
            "total_distance": 493.87,
            "total_duration": 9.36,
            "fuel_stops": 4,
            "rest_stops": 0,
        },
    },
    "eld_data": {
        "daily_logs": [
            {
                "driving": 9.36,
                "distance": 493.87,
                "on_duty": 11.36,
                "off_duty": 10.5,
                "day_number": 1,
            }
        ],
        "remaining_hours": 43.64,
        "total_on_duty": 11.36,
    },
}
