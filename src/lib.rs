//! IFO - Identified Flying Object library.
//!
//! A blazing-fast library for querying real-time aircraft data.

pub mod api;
pub mod error;
pub mod geocoding;
pub mod models;

pub use error::{IfoError, Result};
pub use models::{Aircraft, BoundingBox, Coordinate, Location};
