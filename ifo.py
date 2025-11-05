#!/usr/bin/env python3
"""
IFO - Identified Flying Object CLI

Query aircraft flying over a location using coordinates.
"""
import argparse
import sys
from api import OpenSkyAPI


def parse_coordinates(coord_str: str) -> tuple[float, float]:
    """
    Parse coordinate string in format 'lat,lon'.

    Args:
        coord_str: Coordinate string like '37.7,-122.4'

    Returns:
        Tuple of (latitude, longitude)

    Raises:
        ValueError: If coordinate format is invalid
    """
    try:
        parts = coord_str.split(',')
        if len(parts) != 2:
            raise ValueError("Coordinates must be in format 'latitude,longitude'")

        lat = float(parts[0].strip())
        lon = float(parts[1].strip())

        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude {lat} out of range (-90 to 90)")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Longitude {lon} out of range (-180 to 180)")

        return lat, lon
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid coordinates '{coord_str}': {e}")


def create_bounding_box(lat: float, lon: float, radius_deg: float = 0.5) -> tuple[float, float, float, float]:
    """
    Create a bounding box around a point.

    Args:
        lat: Center latitude
        lon: Center longitude
        radius_deg: Radius in degrees (default: 0.5, approximately 55km)

    Returns:
        Tuple of (lat_min, lon_min, lat_max, lon_max)
    """
    lat_min = max(-90, lat - radius_deg)
    lat_max = min(90, lat + radius_deg)
    lon_min = max(-180, lon - radius_deg)
    lon_max = min(180, lon + radius_deg)

    return lat_min, lon_min, lat_max, lon_max


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Query aircraft flying over a location',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --coords "37.7,-122.4"          # San Francisco
  %(prog)s --coords "51.5,-0.1"            # London
  %(prog)s --coords "40.7,-74.0" --radius 1.0  # New York, 1 degree radius
        '''
    )

    parser.add_argument(
        '--coords',
        type=str,
        required=True,
        metavar='LAT,LON',
        help='Location coordinates in format "latitude,longitude" (e.g., "37.7,-122.4")'
    )

    parser.add_argument(
        '--radius',
        type=float,
        default=0.5,
        metavar='DEGREES',
        help='Search radius in degrees (default: 0.5, approximately 55km)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        metavar='SECONDS',
        help='API request timeout in seconds (default: 10)'
    )

    args = parser.parse_args()

    try:
        # Parse coordinates
        lat, lon = parse_coordinates(args.coords)

        # Create bounding box
        lat_min, lon_min, lat_max, lon_max = create_bounding_box(lat, lon, args.radius)

        # Query API
        with OpenSkyAPI(timeout=args.timeout) as api:
            aircraft = api.get_aircraft_in_area(lat_min, lon_min, lat_max, lon_max)

        # Display results
        if not aircraft:
            print(f"No aircraft found near {lat},{lon}")
            return 0

        print(f"Found {len(aircraft)} aircraft near {lat},{lon}:\n")
        for ac in aircraft:
            print(f"Callsign: {ac['callsign'] or 'N/A'}")
            print(f"  ICAO24: {ac['icao24']}")
            print(f"  Country: {ac['origin_country']}")
            print(f"  Position: {ac['latitude']:.4f}, {ac['longitude']:.4f}")
            if ac['baro_altitude'] is not None:
                print(f"  Altitude: {ac['baro_altitude']:.0f} m")
            if ac['velocity'] is not None:
                print(f"  Velocity: {ac['velocity']:.1f} m/s")
            if ac['on_ground']:
                print(f"  Status: On ground")
            print()

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
