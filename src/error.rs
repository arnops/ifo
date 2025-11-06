//! Error types for the IFO application.

use thiserror::Error;

#[derive(Error, Debug)]
pub enum IfoError {
    #[error("Invalid coordinates: {0}")]
    InvalidCoordinates(String),

    #[error("Invalid latitude: {0} (must be between -90 and 90)")]
    InvalidLatitude(f64),

    #[error("Invalid longitude: {0} (must be between -180 and 180)")]
    InvalidLongitude(f64),

    #[error("Invalid bounding box: {0}")]
    InvalidBoundingBox(String),

    #[error("Place name cannot be empty")]
    EmptyPlaceName,

    #[error("Place name too long (max {max} characters)")]
    PlaceNameTooLong { max: usize },

    #[error("Could not find location: {0}")]
    LocationNotFound(String),

    #[error("Network request failed: {0}")]
    NetworkError(#[from] reqwest::Error),

    #[error("API request failed with status {status}: {message}")]
    ApiError { status: u16, message: String },

    #[error("JSON parsing error: {0}")]
    JsonError(#[from] serde_json::Error),

    #[error("Unexpected response format from {service}")]
    UnexpectedResponse { service: String },

    #[error("Invalid state vector: expected {expected} elements, got {got}")]
    InvalidStateVector { expected: usize, got: usize },

    #[error("Rate limit exceeded")]
    RateLimitExceeded,

    #[error("Timeout after {seconds} seconds")]
    Timeout { seconds: u64 },

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, IfoError>;
