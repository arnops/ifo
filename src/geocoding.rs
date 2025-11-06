//! Geocoding module for converting place names to coordinates.
//!
//! Uses Nominatim (OpenStreetMap) geocoding service which is free
//! and doesn't require an API key.

use governor::{Jitter, Quota, RateLimiter};
use nonzero::nonzero;
use reqwest::Client;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::Mutex;

use crate::error::{IfoError, Result};
use crate::models::{Location, NominatimResult};

const MAX_PLACE_LENGTH: usize = 200;

/// Geocoder using Nominatim API with rate limiting.
pub struct Geocoder {
    client: Client,
    base_url: String,
    rate_limiter: Arc<
        Mutex<
            RateLimiter<
                governor::state::NotKeyed,
                governor::state::InMemoryState,
                governor::clock::DefaultClock,
            >,
        >,
    >,
}

impl Geocoder {
    /// Create a new geocoder with rate limiting.
    pub fn new(timeout_secs: u64) -> Result<Self> {
        let client = Client::builder()
            .user_agent("IFO-CLI/2.0 (Aircraft tracking tool)")
            .timeout(Duration::from_secs(timeout_secs))
            .build()
            .map_err(IfoError::NetworkError)?;

        // Create rate limiter: 1 request per second (Nominatim policy)
        let quota = Quota::per_second(nonzero!(1u32));
        let rate_limiter = RateLimiter::direct(quota);

        Ok(Self {
            client,
            base_url: "https://nominatim.openstreetmap.org".to_string(),
            rate_limiter: Arc::new(Mutex::new(rate_limiter)),
        })
    }

    /// Convert a place name to coordinates.
    pub async fn geocode(&self, place: &str) -> Result<Option<Location>> {
        // Validate input
        let place = place.trim();
        if place.is_empty() {
            return Err(IfoError::EmptyPlaceName);
        }
        if place.len() > MAX_PLACE_LENGTH {
            return Err(IfoError::PlaceNameTooLong {
                max: MAX_PLACE_LENGTH,
            });
        }

        // Rate limiting: wait for permission
        {
            let limiter = self.rate_limiter.lock().await;
            // Add jitter to avoid thundering herd
            limiter
                .until_ready_with_jitter(Jitter::up_to(Duration::from_millis(100)))
                .await;
        }

        // Make request
        let url = format!("{}/search", self.base_url);
        let response = self
            .client
            .get(&url)
            .query(&[("q", place), ("format", "json"), ("limit", "1")])
            .send()
            .await?;

        if !response.status().is_success() {
            let status = response.status();
            let text = response.text().await.unwrap_or_default();
            return Err(IfoError::ApiError {
                status: status.as_u16(),
                message: format!("Geocoding failed: {}", text),
            });
        }

        let results: Vec<NominatimResult> = response.json().await?;

        if results.is_empty() {
            return Ok(None);
        }

        let result = &results[0];

        // Parse and validate response
        let lat = result
            .lat
            .parse::<f64>()
            .map_err(|_| IfoError::UnexpectedResponse {
                service: "Nominatim".to_string(),
            })?;
        let lon = result
            .lon
            .parse::<f64>()
            .map_err(|_| IfoError::UnexpectedResponse {
                service: "Nominatim".to_string(),
            })?;

        Ok(Some(Location {
            lat,
            lon,
            display_name: result.display_name.clone(),
        }))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_place_validation() {
        // Test would require async runtime
        // These tests would normally be in tests/geocoding_tests.rs
    }

    #[test]
    fn test_max_place_length() {
        let _long_name = "a".repeat(MAX_PLACE_LENGTH + 1);
        // Would test that this returns an error
    }
}
