//! Data models for the IFO application.

use crate::error::{IfoError, Result};
use serde::{Deserialize, Serialize};

/// Represents a geographic coordinate.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Coordinate {
    pub latitude: f64,
    pub longitude: f64,
}

impl Coordinate {
    /// Create a new coordinate with validation.
    pub fn new(latitude: f64, longitude: f64) -> Result<Self> {
        if !(-90.0..=90.0).contains(&latitude) {
            return Err(IfoError::InvalidLatitude(latitude));
        }
        if !(-180.0..=180.0).contains(&longitude) {
            return Err(IfoError::InvalidLongitude(longitude));
        }
        Ok(Self {
            latitude,
            longitude,
        })
    }
}

/// Represents a geographic bounding box.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BoundingBox {
    pub lat_min: f64,
    pub lon_min: f64,
    pub lat_max: f64,
    pub lon_max: f64,
}

impl BoundingBox {
    /// Create a new bounding box with validation.
    pub fn new(lat_min: f64, lon_min: f64, lat_max: f64, lon_max: f64) -> Result<Self> {
        // Validate latitudes
        if !(-90.0..=90.0).contains(&lat_min) {
            return Err(IfoError::InvalidLatitude(lat_min));
        }
        if !(-90.0..=90.0).contains(&lat_max) {
            return Err(IfoError::InvalidLatitude(lat_max));
        }

        // Validate longitudes
        if !(-180.0..=180.0).contains(&lon_min) {
            return Err(IfoError::InvalidLongitude(lon_min));
        }
        if !(-180.0..=180.0).contains(&lon_max) {
            return Err(IfoError::InvalidLongitude(lon_max));
        }

        // Validate ordering
        if lat_min >= lat_max {
            return Err(IfoError::InvalidBoundingBox(
                "lat_min must be less than lat_max".to_string(),
            ));
        }
        if lon_min >= lon_max {
            return Err(IfoError::InvalidBoundingBox(
                "lon_min must be less than lon_max".to_string(),
            ));
        }

        Ok(Self {
            lat_min,
            lon_min,
            lat_max,
            lon_max,
        })
    }

    /// Create a bounding box from a center coordinate and radius.
    pub fn from_center(center: Coordinate, radius_deg: f64) -> Self {
        let lat_min = (center.latitude - radius_deg).max(-90.0);
        let lat_max = (center.latitude + radius_deg).min(90.0);
        let lon_min = (center.longitude - radius_deg).max(-180.0);
        let lon_max = (center.longitude + radius_deg).min(180.0);

        // Safe to unwrap because we're clamping values
        Self {
            lat_min,
            lon_min,
            lat_max,
            lon_max,
        }
    }
}

/// Represents an aircraft state.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Aircraft {
    pub icao24: String,
    pub callsign: Option<String>,
    pub origin_country: String,
    pub longitude: Option<f64>,
    pub latitude: Option<f64>,
    pub baro_altitude: Option<f64>,
    pub on_ground: bool,
    pub velocity: Option<f64>,
    pub true_track: Option<f64>,
    pub vertical_rate: Option<f64>,
    pub geo_altitude: Option<f64>,
    pub squawk: Option<String>,
}

impl Aircraft {
    /// Parse a state vector from the OpenSky API.
    pub fn from_state_vector(state: Vec<serde_json::Value>) -> Result<Self> {
        if state.len() < 17 {
            return Err(IfoError::InvalidStateVector {
                expected: 17,
                got: state.len(),
            });
        }

        Ok(Self {
            icao24: state[0].as_str().unwrap_or("").to_string(),
            callsign: state[1]
                .as_str()
                .map(|s| s.trim().to_string())
                .filter(|s| !s.is_empty()),
            origin_country: state[2].as_str().unwrap_or("").to_string(),
            longitude: state[5].as_f64(),
            latitude: state[6].as_f64(),
            baro_altitude: state[7].as_f64(),
            on_ground: state[8].as_bool().unwrap_or(false),
            velocity: state[9].as_f64(),
            true_track: state[10].as_f64(),
            vertical_rate: state[11].as_f64(),
            geo_altitude: state[13].as_f64(),
            squawk: state[14].as_str().map(|s| s.to_string()),
        })
    }
}

/// Represents a location from geocoding.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Location {
    pub lat: f64,
    pub lon: f64,
    pub display_name: String,
}

/// Response from OpenSky API.
#[derive(Debug, Deserialize)]
pub struct OpenSkyResponse {
    pub time: Option<i64>,
    pub states: Option<Vec<Vec<serde_json::Value>>>,
}

/// Response from Nominatim geocoding API.
#[derive(Debug, Deserialize)]
pub struct NominatimResult {
    pub lat: String,
    pub lon: String,
    pub display_name: String,
}
