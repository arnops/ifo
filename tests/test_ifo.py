"""
Tests for the IFO CLI.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import ifo


class TestParseCoordinates:
    """Test cases for parse_coordinates function."""

    def test_valid_coordinates(self):
        """Test parsing valid coordinate strings."""
        lat, lon = ifo.parse_coordinates("37.7,-122.4")
        assert lat == 37.7
        assert lon == -122.4

    def test_valid_coordinates_with_spaces(self):
        """Test parsing coordinates with whitespace."""
        lat, lon = ifo.parse_coordinates("51.5, -0.1")
        assert lat == 51.5
        assert lon == -0.1

    def test_invalid_format_missing_comma(self):
        """Test error on invalid format."""
        with pytest.raises(ValueError, match="must be in format"):
            ifo.parse_coordinates("37.7")

    def test_invalid_format_too_many_parts(self):
        """Test error on too many coordinate parts."""
        with pytest.raises(ValueError, match="must be in format"):
            ifo.parse_coordinates("37.7,-122.4,100")

    def test_invalid_latitude_out_of_range(self):
        """Test error on latitude out of range."""
        with pytest.raises(ValueError, match="out of range"):
            ifo.parse_coordinates("91.0,-122.4")
        with pytest.raises(ValueError, match="out of range"):
            ifo.parse_coordinates("-91.0,-122.4")

    def test_invalid_longitude_out_of_range(self):
        """Test error on longitude out of range."""
        with pytest.raises(ValueError, match="out of range"):
            ifo.parse_coordinates("37.7,181.0")
        with pytest.raises(ValueError, match="out of range"):
            ifo.parse_coordinates("37.7,-181.0")

    def test_non_numeric_values(self):
        """Test error on non-numeric input."""
        with pytest.raises(ValueError, match="Invalid coordinates"):
            ifo.parse_coordinates("abc,def")


class TestCreateBoundingBox:
    """Test cases for create_bounding_box function."""

    def test_default_radius(self):
        """Test bounding box with default radius."""
        lat_min, lon_min, lat_max, lon_max = ifo.create_bounding_box(37.7, -122.4)
        assert lat_min == pytest.approx(37.2)
        assert lat_max == pytest.approx(38.2)
        assert lon_min == pytest.approx(-122.9)
        assert lon_max == pytest.approx(-121.9)

    def test_custom_radius(self):
        """Test bounding box with custom radius."""
        lat_min, lon_min, lat_max, lon_max = ifo.create_bounding_box(40.0, -74.0, 1.0)
        assert lat_min == pytest.approx(39.0)
        assert lat_max == pytest.approx(41.0)
        assert lon_min == pytest.approx(-75.0)
        assert lon_max == pytest.approx(-73.0)

    def test_boundary_at_north_pole(self):
        """Test bounding box clamped at 90 degrees."""
        lat_min, lon_min, lat_max, lon_max = ifo.create_bounding_box(89.7, 0, 0.5)
        assert lat_min == pytest.approx(89.2)
        assert lat_max == 90.0  # Clamped

    def test_boundary_at_south_pole(self):
        """Test bounding box clamped at -90 degrees."""
        lat_min, lon_min, lat_max, lon_max = ifo.create_bounding_box(-89.7, 0, 0.5)
        assert lat_min == -90.0  # Clamped
        assert lat_max == pytest.approx(-89.2)

    def test_boundary_at_international_date_line(self):
        """Test bounding box clamped at +/-180 degrees."""
        lat_min, lon_min, lat_max, lon_max = ifo.create_bounding_box(0, 179.7, 0.5)
        assert lon_min == pytest.approx(179.2)
        assert lon_max == 180.0  # Clamped

        lat_min, lon_min, lat_max, lon_max = ifo.create_bounding_box(0, -179.7, 0.5)
        assert lon_min == -180.0  # Clamped
        assert lon_max == pytest.approx(-179.2)


class TestMain:
    """Test cases for main CLI function."""

    @patch('ifo.OpenSkyAPI')
    @patch('sys.argv', ['ifo.py', '--coords', '37.7,-122.4'])
    def test_main_success_with_aircraft(self, mock_api_class, capsys):
        """Test successful query with aircraft found."""
        # Setup mock
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=False)
        mock_api.get_aircraft_in_area.return_value = [
            {
                'icao24': 'abc123',
                'callsign': 'UAL123',
                'origin_country': 'United States',
                'latitude': 37.75,
                'longitude': -122.45,
                'baro_altitude': 10000.0,
                'velocity': 250.5,
                'on_ground': False,
                'true_track': 90.0,
                'vertical_rate': 0.0,
                'geo_altitude': 10050.0,
                'squawk': '1234'
            }
        ]
        mock_api_class.return_value = mock_api

        result = ifo.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Found 1 aircraft" in captured.out
        assert "UAL123" in captured.out
        assert "abc123" in captured.out
        assert "United States" in captured.out

    @patch('ifo.OpenSkyAPI')
    @patch('sys.argv', ['ifo.py', '--coords', '37.7,-122.4'])
    def test_main_no_aircraft(self, mock_api_class, capsys):
        """Test query with no aircraft found."""
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=False)
        mock_api.get_aircraft_in_area.return_value = []
        mock_api_class.return_value = mock_api

        result = ifo.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "No aircraft found" in captured.out

    @patch('sys.argv', ['ifo.py', '--coords', 'invalid'])
    def test_main_invalid_coordinates(self, capsys):
        """Test with invalid coordinates."""
        result = ifo.main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err

    @patch('ifo.OpenSkyAPI')
    @patch('sys.argv', ['ifo.py', '--coords', '37.7,-122.4', '--radius', '1.0', '--timeout', '15'])
    def test_main_with_custom_options(self, mock_api_class):
        """Test with custom radius and timeout."""
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=False)
        mock_api.get_aircraft_in_area.return_value = []
        mock_api_class.return_value = mock_api

        result = ifo.main()

        assert result == 0
        # Verify API was initialized with custom timeout
        mock_api_class.assert_called_once_with(timeout=15)
        # Verify correct bounding box was used (1.0 degree radius)
        call_args = mock_api.get_aircraft_in_area.call_args[0]
        assert call_args[0] == pytest.approx(36.7)  # lat_min
        assert call_args[1] == pytest.approx(-123.4)  # lon_min
        assert call_args[2] == pytest.approx(38.7)  # lat_max
        assert call_args[3] == pytest.approx(-121.4)  # lon_max

    @patch('ifo.Geocoder')
    @patch('ifo.OpenSkyAPI')
    @patch('sys.argv', ['ifo.py', '--place', 'San Francisco'])
    def test_main_with_place_name(self, mock_api_class, mock_geocoder_class, capsys):
        """Test with place name geocoding."""
        # Setup geocoder mock
        mock_geocoder = Mock()
        mock_geocoder.__enter__ = Mock(return_value=mock_geocoder)
        mock_geocoder.__exit__ = Mock(return_value=False)
        mock_geocoder.geocode.return_value = {
            'lat': 37.7749,
            'lon': -122.4194,
            'display_name': 'San Francisco, California, USA'
        }
        mock_geocoder_class.return_value = mock_geocoder

        # Setup API mock
        mock_api = Mock()
        mock_api.__enter__ = Mock(return_value=mock_api)
        mock_api.__exit__ = Mock(return_value=False)
        mock_api.get_aircraft_in_area.return_value = []
        mock_api_class.return_value = mock_api

        result = ifo.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "San Francisco, California, USA" in captured.out
        assert "37.7749" in captured.out
        mock_geocoder.geocode.assert_called_once_with('San Francisco')

    @patch('ifo.Geocoder')
    @patch('sys.argv', ['ifo.py', '--place', 'NonexistentPlace12345'])
    def test_main_place_not_found(self, mock_geocoder_class, capsys):
        """Test with place name that cannot be geocoded."""
        mock_geocoder = Mock()
        mock_geocoder.__enter__ = Mock(return_value=mock_geocoder)
        mock_geocoder.__exit__ = Mock(return_value=False)
        mock_geocoder.geocode.return_value = None
        mock_geocoder_class.return_value = mock_geocoder

        result = ifo.main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Could not find location" in captured.err
