"""
Tests for geocoding functionality.
"""
import pytest
from unittest.mock import Mock, patch
from geocoding import Geocoder


class TestGeocoder:
    """Test cases for Geocoder class."""

    def test_initialization(self):
        """Test geocoder initialization."""
        geocoder = Geocoder(timeout=15)
        assert geocoder.timeout == 15
        assert geocoder.BASE_URL == "https://nominatim.openstreetmap.org"
        assert 'IFO-CLI' in geocoder.session.headers['User-Agent']

    def test_context_manager(self):
        """Test geocoder works as context manager."""
        with Geocoder() as geocoder:
            assert geocoder.session is not None

    def test_empty_place_name(self):
        """Test error on empty place name."""
        geocoder = Geocoder()
        with pytest.raises(ValueError, match="cannot be empty"):
            geocoder.geocode("")
        with pytest.raises(ValueError, match="cannot be empty"):
            geocoder.geocode("   ")

    @patch('geocoding.requests.Session.get')
    def test_geocode_success(self, mock_get):
        """Test successful geocoding."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'lat': '37.7749',
                'lon': '-122.4194',
                'display_name': 'San Francisco, California, USA'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode("San Francisco")

        assert result is not None
        assert result['lat'] == 37.7749
        assert result['lon'] == -122.4194
        assert result['display_name'] == 'San Francisco, California, USA'

        # Verify API was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['params']['q'] == 'San Francisco'
        assert call_args[1]['params']['format'] == 'json'
        assert call_args[1]['params']['limit'] == 1

    @patch('geocoding.requests.Session.get')
    def test_geocode_not_found(self, mock_get):
        """Test geocoding when place is not found."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode("NonexistentPlace12345")

        assert result is None

    @patch('geocoding.requests.Session.get')
    def test_geocode_strips_whitespace(self, mock_get):
        """Test that place names are stripped of whitespace."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'lat': '51.5074',
                'lon': '-0.1278',
                'display_name': 'London, UK'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode("  London  ")

        assert result is not None
        # Verify whitespace was stripped in the API call
        call_args = mock_get.call_args
        assert call_args[1]['params']['q'] == 'London'

    @patch('geocoding.requests.Session.get')
    def test_geocode_with_country(self, mock_get):
        """Test geocoding with country specification."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'lat': '51.5074',
                'lon': '-0.1278',
                'display_name': 'London, England, United Kingdom'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode("London, UK")

        assert result is not None
        assert result['lat'] == 51.5074
        assert result['lon'] == -0.1278

    @patch('geocoding.requests.Session.get')
    def test_geocode_type_conversion(self, mock_get):
        """Test that coordinates are converted to float."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'lat': '40.7128',  # String from API
                'lon': '-74.0060',  # String from API
                'display_name': 'New York, NY, USA'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        result = geocoder.geocode("New York")

        assert isinstance(result['lat'], float)
        assert isinstance(result['lon'], float)
        assert result['lat'] == 40.7128
        assert result['lon'] == -74.0060

    def test_place_name_too_long(self):
        """Test error on excessively long place names."""
        geocoder = Geocoder()
        long_name = "A" * 201  # Over MAX_PLACE_LENGTH
        with pytest.raises(ValueError, match="too long"):
            geocoder.geocode(long_name)

    @patch('geocoding.requests.Session.get')
    def test_invalid_response_structure(self, mock_get):
        """Test error on unexpected API response format."""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'lat': '40.7128',
                # Missing 'lon' and 'display_name'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        geocoder = Geocoder()
        with pytest.raises(ValueError, match="Unexpected response format"):
            geocoder.geocode("Test")
