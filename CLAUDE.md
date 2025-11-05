# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Identified Flying Object (IFO)** - A Python CLI application for querying real-time aircraft data flying over a specified location using coordinates or place names.

## Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Query by coordinates
./ifo.py --coords "37.7,-122.4"

# Query by place name
./ifo.py --place "San Francisco"

# With custom search radius (in degrees)
./ifo.py --place "London, UK" --radius 1.0

# With custom timeout
./ifo.py --coords "40.7,-74.0" --timeout 15
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test
pytest tests/test_api.py::TestOpenSkyAPI::test_initialization
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

### Core Modules

1. **api.py** - OpenSky Network API client
   - `OpenSkyAPI` class: Queries real-time aircraft data within geographic bounding boxes
   - Validates coordinates and bounding box parameters
   - Parses state vectors from API into structured dictionaries
   - Uses HTTPS with proper timeout handling

2. **geocoding.py** - Nominatim/OpenStreetMap geocoding client
   - `Geocoder` class: Converts place names to coordinates
   - Implements rate limiting (1 req/sec) per Nominatim usage policy
   - Input validation with max length checks
   - Response structure validation

3. **ifo.py** - CLI interface
   - Command-line argument parsing with `argparse`
   - Coordinate validation and bounding box generation
   - Integration of API and geocoding modules
   - User-friendly output formatting

### Data Flow

1. User provides location (coordinates OR place name) via CLI
2. If place name: geocoding.py converts to coordinates
3. Coordinates are used to create a bounding box (default ±0.5°)
4. api.py queries OpenSky Network for aircraft in bounding box
5. Results are formatted and displayed to user

### Security Features

- All external API calls use HTTPS
- Input validation at multiple layers (CLI, parsing, API client)
- Rate limiting for third-party APIs
- No credentials or API keys required
- Comprehensive security review for each feature

### Testing Strategy

- Unit tests for all modules with mocking for external API calls
- 99% test coverage overall
- Tests cover edge cases, boundary conditions, and error handling
- Security-focused testing for input validation

## Development Practices

- Each feature is committed incrementally with security review
- All code changes include comprehensive tests
- Security agent reviews code before commits
- Follows defensive programming principles
