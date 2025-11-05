"""
OpenSky Network API client for querying aircraft data.
"""
import requests
from typing import Optional, Dict, List, Any


class OpenSkyAPI:
    """Client for interacting with the OpenSky Network REST API."""

    BASE_URL = "https://opensky-network.org/api"

    def __init__(self, timeout: int = 10):
        """
        Initialize the OpenSky API client.

        Args:
            timeout: Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IFO-CLI/1.0'
        })

    def get_aircraft_in_area(
        self,
        lat_min: float,
        lon_min: float,
        lat_max: float,
        lon_max: float
    ) -> List[Dict[str, Any]]:
        """
        Query aircraft within a geographic bounding box.

        Args:
            lat_min: Minimum latitude (degrees)
            lon_min: Minimum longitude (degrees)
            lat_max: Maximum latitude (degrees)
            lon_max: Maximum longitude (degrees)

        Returns:
            List of aircraft state vectors as dictionaries

        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the bounding box parameters are invalid
        """
        # Validate bounding box
        if not (-90 <= lat_min <= 90 and -90 <= lat_max <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= lon_min <= 180 and -180 <= lon_max <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")
        if lat_min >= lat_max:
            raise ValueError("lat_min must be less than lat_max")
        if lon_min >= lon_max:
            raise ValueError("lon_min must be less than lon_max")

        params = {
            'lamin': lat_min,
            'lomin': lon_min,
            'lamax': lat_max,
            'lomax': lon_max
        }

        response = self.session.get(
            f"{self.BASE_URL}/states/all",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()

        data = response.json()

        # Parse state vectors into more readable format
        if not data.get('states'):
            return []

        aircraft = []
        for state in data['states']:
            aircraft.append(self._parse_state_vector(state))

        return aircraft

    def _parse_state_vector(self, state: List) -> Dict[str, Any]:
        """
        Parse raw state vector array into a dictionary.

        State vector format from OpenSky API:
        [0] icao24, [1] callsign, [2] origin_country, [3] time_position,
        [4] last_contact, [5] longitude, [6] latitude, [7] baro_altitude,
        [8] on_ground, [9] velocity, [10] true_track, [11] vertical_rate,
        [12] sensors, [13] geo_altitude, [14] squawk, [15] spi, [16] position_source

        Args:
            state: Raw state vector array from API

        Returns:
            Dictionary with parsed aircraft information

        Raises:
            ValueError: If state vector has insufficient data
        """
        if len(state) < 17:
            raise ValueError(f"Invalid state vector: expected 17 elements, got {len(state)}")

        return {
            'icao24': state[0],
            'callsign': state[1].strip() if state[1] else None,
            'origin_country': state[2],
            'longitude': state[5],
            'latitude': state[6],
            'baro_altitude': state[7],
            'on_ground': state[8],
            'velocity': state[9],
            'true_track': state[10],
            'vertical_rate': state[11],
            'geo_altitude': state[13],
            'squawk': state[14]
        }

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
