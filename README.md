# IFO - Identified Flying Object

A Python CLI application for querying real-time aircraft information flying over any location worldwide.

## Features

- 🌍 **Query by location**: Use coordinates or place names
- ✈️ **Real-time data**: Live aircraft tracking via OpenSky Network API
- 🔍 **Flexible search**: Configurable search radius
- 🔒 **Secure**: Input validation, rate limiting, HTTPS-only
- ✅ **Well-tested**: 99% test coverage with 38 test cases

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ifo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Query by Coordinates

```bash
./ifo.py --coords "37.7,-122.4"
```

### Query by Place Name

```bash
./ifo.py --place "San Francisco"
./ifo.py --place "London, UK"
./ifo.py --place "Tokyo, Japan"
```

### Custom Search Radius

```bash
# Search radius in degrees (default: 0.5° ≈ 55km)
./ifo.py --place "New York" --radius 1.0
```

### Custom Timeout

```bash
./ifo.py --coords "51.5,-0.1" --timeout 15
```

## Example Output

```
Found location: San Francisco, California, USA (37.7749, -122.4194)
Found 3 aircraft near San Francisco, California, USA:

Callsign: UAL123
  ICAO24: abc123
  Country: United States
  Position: 37.7500, -122.4500
  Altitude: 10000 m
  Velocity: 250.5 m/s

Callsign: SWA456
  ICAO24: def456
  Country: United States
  Position: 37.8000, -122.3800
  Altitude: 8500 m
  Velocity: 220.0 m/s

...
```

## Development

### Run Tests

```bash
# All tests with coverage
pytest

# Specific test file
pytest tests/test_api.py

# With detailed coverage report
pytest --cov=. --cov-report=term-missing
```

### Project Structure

```
ifo/
├── ifo.py              # CLI entry point
├── api.py              # OpenSky Network API client
├── geocoding.py        # Place name to coordinates converter
├── requirements.txt    # Python dependencies
└── tests/             # Test suite
    ├── test_api.py
    ├── test_geocoding.py
    └── test_ifo.py
```

## Architecture

The application uses a modular architecture:

1. **CLI Layer** (`ifo.py`): Handles user input and output formatting
2. **Geocoding Layer** (`geocoding.py`): Converts place names to coordinates using Nominatim/OpenStreetMap
3. **API Layer** (`api.py`): Queries OpenSky Network for aircraft data

### Data Sources

- **Aircraft Data**: [OpenSky Network](https://opensky-network.org/) - Community-based ADS-B/Mode S data
- **Geocoding**: [Nominatim](https://nominatim.openstreetmap.org/) - OpenStreetMap geocoding service

## Security

- All API calls use HTTPS
- Input validation at multiple layers
- Rate limiting (1 req/sec for Nominatim API)
- No API keys or credentials required
- Comprehensive security reviews for all features

## License

[Add your license here]

## Contributing

Contributions are welcome! Please ensure:
- All tests pass (`pytest`)
- Code coverage remains high
- Security best practices are followed
