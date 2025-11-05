"""
Geocoding support for converting place names to coordinates.

Uses Nominatim (OpenStreetMap) geocoding service which is free
and doesn't require an API key.
"""
import requests
import time
from threading import Lock
from typing import Optional, Dict, Any


class Geocoder:
    """Simple geocoder using Nominatim API."""

    BASE_URL = "https://nominatim.openstreetmap.org"
    MAX_PLACE_LENGTH = 200

    def __init__(self, timeout: int = 10):
        """
        Initialize the geocoder.

        Args:
            timeout: Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
        self.session = requests.Session()
        # Nominatim requires a User-Agent per their usage policy
        self.session.headers.update({
            'User-Agent': 'IFO-CLI/1.0 (Aircraft tracking tool)'
        })
        # Rate limiting to comply with Nominatim usage policy (max 1 req/sec)
        self._last_request_time = 0.0
        self._lock = Lock()

    def geocode(self, place: str) -> Optional[Dict[str, Any]]:
        """
        Convert a place name to coordinates.

        Args:
            place: Place name (e.g., "San Francisco", "London, UK")

        Returns:
            Dictionary with 'lat', 'lon', and 'display_name' if found,
            None if not found

        Raises:
            requests.RequestException: If the geocoding request fails
            ValueError: If place name is invalid
        """
        if not place or not place.strip():
            raise ValueError("Place name cannot be empty")

        if len(place) > self.MAX_PLACE_LENGTH:
            raise ValueError(f"Place name too long (max {self.MAX_PLACE_LENGTH} characters)")

        # Rate limiting: ensure at least 1 second between requests (Nominatim policy)
        with self._lock:
            time_since_last = time.time() - self._last_request_time
            if time_since_last < 1.0:
                time.sleep(1.0 - time_since_last)
            self._last_request_time = time.time()

        params = {
            'q': place.strip(),
            'format': 'json',
            'limit': 1
        }

        response = self.session.get(
            f"{self.BASE_URL}/search",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()

        data = response.json()

        if not data or len(data) == 0:
            return None

        result = data[0]

        # Validate response structure
        if 'lat' not in result or 'lon' not in result or 'display_name' not in result:
            raise ValueError("Unexpected response format from geocoding service")

        return {
            'lat': float(result['lat']),
            'lon': float(result['lon']),
            'display_name': result['display_name']
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
