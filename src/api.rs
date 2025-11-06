//! OpenSky Network API client.

use reqwest::Client;
use std::time::Duration;

use crate::error::{IfoError, Result};
use crate::models::{Aircraft, BoundingBox, OpenSkyResponse};

/// Client for interacting with the OpenSky Network REST API.
pub struct OpenSkyClient {
    client: Client,
    base_url: String,
}

impl OpenSkyClient {
    /// Create a new OpenSky API client.
    pub fn new(timeout_secs: u64) -> Result<Self> {
        let client = Client::builder()
            .user_agent("IFO-CLI/2.0 (Rust)")
            .timeout(Duration::from_secs(timeout_secs))
            .build()
            .map_err(IfoError::NetworkError)?;

        Ok(Self {
            client,
            base_url: "https://opensky-network.org/api".to_string(),
        })
    }

    /// Query aircraft within a geographic bounding box.
    pub async fn get_aircraft_in_area(&self, bbox: BoundingBox) -> Result<Vec<Aircraft>> {
        let url = format!("{}/states/all", self.base_url);

        let response = self
            .client
            .get(&url)
            .query(&[
                ("lamin", bbox.lat_min.to_string()),
                ("lomin", bbox.lon_min.to_string()),
                ("lamax", bbox.lat_max.to_string()),
                ("lomax", bbox.lon_max.to_string()),
            ])
            .send()
            .await?;

        if !response.status().is_success() {
            let status = response.status();
            let text = response.text().await.unwrap_or_default();
            return Err(IfoError::ApiError {
                status: status.as_u16(),
                message: text,
            });
        }

        let data: OpenSkyResponse = response.json().await?;

        // Parse state vectors into aircraft
        let aircraft = match data.states {
            Some(states) => {
                let mut result = Vec::with_capacity(states.len());
                for state in states {
                    match Aircraft::from_state_vector(state) {
                        Ok(ac) => result.push(ac),
                        Err(e) => {
                            // Log but don't fail on individual parsing errors
                            eprintln!("Warning: Failed to parse state vector: {}", e);
                        }
                    }
                }
                result
            }
            None => Vec::new(),
        };

        Ok(aircraft)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::models::Coordinate;

    #[tokio::test]
    async fn test_bounding_box_validation() {
        // Test invalid latitude
        let result = BoundingBox::new(91.0, 0.0, 45.0, 10.0);
        assert!(result.is_err());

        // Test invalid longitude
        let result = BoundingBox::new(0.0, 181.0, 45.0, 10.0);
        assert!(result.is_err());

        // Test invalid ordering
        let result = BoundingBox::new(45.0, 0.0, 40.0, 10.0);
        assert!(result.is_err());

        // Test valid bounding box
        let result = BoundingBox::new(40.0, 0.0, 45.0, 10.0);
        assert!(result.is_ok());
    }

    #[test]
    fn test_bounding_box_from_center() {
        let center = Coordinate::new(37.7, -122.4).unwrap();
        let bbox = BoundingBox::from_center(center, 0.5);

        assert_eq!(bbox.lat_min, 37.2);
        assert_eq!(bbox.lat_max, 38.2);
        assert_eq!(bbox.lon_min, -122.9);
        assert_eq!(bbox.lon_max, -121.9);
    }

    #[test]
    fn test_bounding_box_clamping() {
        // Test clamping at north pole
        let center = Coordinate::new(89.7, 0.0).unwrap();
        let bbox = BoundingBox::from_center(center, 0.5);
        assert_eq!(bbox.lat_max, 90.0);

        // Test clamping at south pole
        let center = Coordinate::new(-89.7, 0.0).unwrap();
        let bbox = BoundingBox::from_center(center, 0.5);
        assert_eq!(bbox.lat_min, -90.0);
    }
}
