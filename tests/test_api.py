"""
Tests for the OpenSky API client.
"""
import pytest
from unittest.mock import Mock, patch
from api import OpenSkyAPI


class TestOpenSkyAPI:
    """Test cases for OpenSkyAPI class."""

    def test_initialization(self):
        """Test API client initialization."""
        api = OpenSkyAPI(timeout=15)
        assert api.timeout == 15
        assert api.BASE_URL == "https://opensky-network.org/api"
        assert api.session.headers['User-Agent'] == 'IFO-CLI/1.0'

    def test_context_manager(self):
        """Test API client works as context manager."""
        with OpenSkyAPI() as api:
            assert api.session is not None
        # Session should be closed after context exit

    def test_validate_bounding_box_invalid_latitude(self):
        """Test validation rejects invalid latitude values."""
        api = OpenSkyAPI()
        with pytest.raises(ValueError, match="Latitude must be between"):
            api.get_aircraft_in_area(-91, 0, 45, 10)
        with pytest.raises(ValueError, match="Latitude must be between"):
            api.get_aircraft_in_area(0, 0, 91, 10)

    def test_validate_bounding_box_invalid_longitude(self):
        """Test validation rejects invalid longitude values."""
        api = OpenSkyAPI()
        with pytest.raises(ValueError, match="Longitude must be between"):
            api.get_aircraft_in_area(0, -181, 45, 10)
        with pytest.raises(ValueError, match="Longitude must be between"):
            api.get_aircraft_in_area(0, 0, 45, 181)

    def test_validate_bounding_box_invalid_order(self):
        """Test validation rejects inverted bounding boxes."""
        api = OpenSkyAPI()
        with pytest.raises(ValueError, match="lat_min must be less than lat_max"):
            api.get_aircraft_in_area(45, 0, 40, 10)
        with pytest.raises(ValueError, match="lon_min must be less than lon_max"):
            api.get_aircraft_in_area(40, 10, 45, 5)

    @patch('api.requests.Session.get')
    def test_get_aircraft_in_area_success(self, mock_get):
        """Test successful aircraft query."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'time': 1234567890,
            'states': [
                [
                    'abc123',      # icao24
                    'UAL123  ',    # callsign
                    'United States', # origin_country
                    1234567880,    # time_position
                    1234567890,    # last_contact
                    -122.4,        # longitude
                    37.7,          # latitude
                    10000.0,       # baro_altitude
                    False,         # on_ground
                    250.0,         # velocity
                    90.0,          # true_track
                    0.0,           # vertical_rate
                    None,          # sensors
                    10050.0,       # geo_altitude
                    '1234',        # squawk
                    False,         # spi
                    0              # position_source
                ]
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenSkyAPI()
        aircraft = api.get_aircraft_in_area(37.0, -123.0, 38.0, -122.0)

        assert len(aircraft) == 1
        assert aircraft[0]['icao24'] == 'abc123'
        assert aircraft[0]['callsign'] == 'UAL123'
        assert aircraft[0]['origin_country'] == 'United States'
        assert aircraft[0]['latitude'] == 37.7
        assert aircraft[0]['longitude'] == -122.4
        assert aircraft[0]['baro_altitude'] == 10000.0
        assert aircraft[0]['velocity'] == 250.0

        # Verify API was called with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['params']['lamin'] == 37.0
        assert call_args[1]['params']['lomin'] == -123.0
        assert call_args[1]['params']['lamax'] == 38.0
        assert call_args[1]['params']['lomax'] == -122.0

    @patch('api.requests.Session.get')
    def test_get_aircraft_in_area_empty(self, mock_get):
        """Test query with no aircraft in area."""
        mock_response = Mock()
        mock_response.json.return_value = {'time': 1234567890, 'states': None}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = OpenSkyAPI()
        aircraft = api.get_aircraft_in_area(37.0, -123.0, 38.0, -122.0)

        assert aircraft == []

    def test_parse_state_vector(self):
        """Test state vector parsing."""
        api = OpenSkyAPI()
        state = [
            'abc123', 'TEST123 ', 'Germany', 1234567880, 1234567890,
            10.5, 50.2, 5000.0, False, 150.0, 45.0, 5.0,
            None, 5100.0, '7700', False, 0
        ]

        parsed = api._parse_state_vector(state)

        assert parsed['icao24'] == 'abc123'
        assert parsed['callsign'] == 'TEST123'
        assert parsed['origin_country'] == 'Germany'
        assert parsed['latitude'] == 50.2
        assert parsed['longitude'] == 10.5
        assert parsed['baro_altitude'] == 5000.0
        assert parsed['velocity'] == 150.0
        assert parsed['squawk'] == '7700'

    def test_parse_state_vector_null_callsign(self):
        """Test state vector parsing with null callsign."""
        api = OpenSkyAPI()
        state = [
            'abc123', None, 'Germany', 1234567880, 1234567890,
            10.5, 50.2, 5000.0, False, 150.0, 45.0, 5.0,
            None, 5100.0, '7700', False, 0
        ]

        parsed = api._parse_state_vector(state)
        assert parsed['callsign'] is None

    def test_parse_state_vector_invalid_length(self):
        """Test state vector parsing with insufficient data."""
        api = OpenSkyAPI()
        state = ['abc123', 'TEST', 'Germany']  # Only 3 elements instead of 17

        with pytest.raises(ValueError, match="Invalid state vector: expected 17 elements, got 3"):
            api._parse_state_vector(state)
