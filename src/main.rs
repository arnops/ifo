//! IFO - Identified Flying Object CLI
//!
//! Query aircraft flying over a location using coordinates or place name.

use clap::{Args, Parser};
use std::process;

use ifo::{
    api::OpenSkyClient,
    geocoding::Geocoder,
    models::{BoundingBox, Coordinate},
    Result,
};

#[derive(Parser)]
#[command(name = "ifo")]
#[command(author, version, about = "Identified Flying Object: Query aircraft flying over a location", long_about = None)]
#[command(after_help = r#"EXAMPLES:
    ifo --coords "37.7,-122.4"          # Coordinates
    ifo --place "San Francisco"          # Place name
    ifo --place "London, UK"             # Place with country
    ifo --coords "40.7,-74.0" --radius 1.0  # Custom radius"#)]
struct Cli {
    /// Location input (coordinates or place name)
    #[command(flatten)]
    location: LocationArgs,

    /// Search radius in degrees (default: 0.5, approximately 55km)
    #[arg(long, default_value = "0.5")]
    radius: f64,

    /// API request timeout in seconds (default: 10)
    #[arg(long, default_value = "10")]
    timeout: u64,
}

#[derive(Args)]
#[group(required = true, multiple = false)]
struct LocationArgs {
    /// Location coordinates in format "latitude,longitude" (e.g., "37.7,-122.4")
    #[arg(long, value_name = "LAT,LON")]
    coords: Option<String>,

    /// Place name (e.g., "San Francisco" or "London, UK")
    #[arg(long, value_name = "NAME")]
    place: Option<String>,
}

/// Parse coordinate string in format 'lat,lon'.
fn parse_coordinates(coord_str: &str) -> Result<Coordinate> {
    let parts: Vec<&str> = coord_str.split(',').collect();
    if parts.len() != 2 {
        return Err(ifo::IfoError::InvalidCoordinates(
            "Coordinates must be in format 'latitude,longitude'".to_string(),
        ));
    }

    let lat = parts[0].trim().parse::<f64>().map_err(|_| {
        ifo::IfoError::InvalidCoordinates(format!("Invalid latitude: {}", parts[0]))
    })?;

    let lon = parts[1].trim().parse::<f64>().map_err(|_| {
        ifo::IfoError::InvalidCoordinates(format!("Invalid longitude: {}", parts[1]))
    })?;

    Coordinate::new(lat, lon)
}

#[tokio::main]
async fn main() {
    if let Err(e) = run().await {
        eprintln!("Error: {}", e);
        process::exit(1);
    }
}

async fn run() -> Result<()> {
    let cli = Cli::parse();

    // Get coordinates (either from direct coords or geocoding)
    let (coord, location_name) = if let Some(coords_str) = &cli.location.coords {
        let coord = parse_coordinates(coords_str)?;
        (coord, format!("{},{}", coord.latitude, coord.longitude))
    } else if let Some(place) = &cli.location.place {
        // Geocode place name
        let geocoder = Geocoder::new(cli.timeout)?;
        match geocoder.geocode(place).await? {
            Some(location) => {
                println!(
                    "Found location: {} ({:.4}, {:.4})",
                    location.display_name, location.lat, location.lon
                );
                let coord = Coordinate::new(location.lat, location.lon)?;
                (coord, location.display_name)
            }
            None => {
                return Err(ifo::IfoError::LocationNotFound(place.clone()));
            }
        }
    } else {
        unreachable!("Clap ensures one location arg is provided");
    };

    // Create bounding box
    let bbox = BoundingBox::from_center(coord, cli.radius);

    // Query API
    let api = OpenSkyClient::new(cli.timeout)?;
    let aircraft = api.get_aircraft_in_area(bbox).await?;

    // Display results
    if aircraft.is_empty() {
        println!("No aircraft found near {}", location_name);
        return Ok(());
    }

    println!(
        "Found {} aircraft near {}:\n",
        aircraft.len(),
        location_name
    );

    for ac in aircraft {
        println!("Callsign: {}", ac.callsign.as_deref().unwrap_or("N/A"));
        println!("  ICAO24: {}", ac.icao24);
        println!("  Country: {}", ac.origin_country);

        if let (Some(lat), Some(lon)) = (ac.latitude, ac.longitude) {
            println!("  Position: {:.4}, {:.4}", lat, lon);
        }

        if let Some(alt) = ac.baro_altitude {
            println!("  Altitude: {:.0} m", alt);
        }

        if let Some(vel) = ac.velocity {
            println!("  Velocity: {:.1} m/s", vel);
        }

        if ac.on_ground {
            println!("  Status: On ground");
        }

        println!();
    }

    Ok(())
}
