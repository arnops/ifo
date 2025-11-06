# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Identified Flying Object (IFO)** - A blazing-fast Rust CLI application for querying real-time aircraft data flying over a specified location using coordinates or place names.

**Performance**: Sub-5ms startup time, 12.5MB memory footprint, 2.4MB binary size

## Commands

### Build
```bash
# Debug build
cargo build

# Release build (optimized)
cargo build --release

# Check code without building
cargo check
```

### Running the Application
```bash
# Query by coordinates
cargo run --release -- --coords "37.7,-122.4"
# or if using the binary:
./target/release/ifo --coords "37.7,-122.4"

# Query by place name
./target/release/ifo --place "San Francisco"

# With custom search radius (in degrees)
./target/release/ifo --place "London, UK" --radius 1.0

# With custom timeout
./target/release/ifo --coords "40.7,-74.0" --timeout 15
```

### Testing
```bash
# Run all tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Run specific test
cargo test test_bounding_box_validation

# Run specific module tests
cargo test --test api
```

### Code Quality
```bash
# Format code
cargo fmt

# Run linter
cargo clippy

# Run clippy with pedantic lints
cargo clippy -- -W clippy::pedantic
```

## Development Environment

### Devcontainer (Recommended)

The project includes a devcontainer for consistent cross-platform development:

```bash
# Open in VS Code
code .

# Reopen in Container
# Cmd+Shift+P -> "Dev Containers: Reopen in Container"
```

The devcontainer includes:
- Rust toolchain with all cross-compilation targets
- `cross` tool for Docker-based cross-compilation
- Node.js LTS (for AI extensions and tooling)
- ChunkHound for semantic code search
- VS Code extensions (rust-analyzer, Better TOML, crates, CodeLLDB)
- AI assistants (Claude Code, ChatGPT)
- Cargo tools (cargo-edit, cargo-watch)

See [.devcontainer/README.md](.devcontainer/README.md) for details.

### Cross-Platform Builds

```bash
# Inside devcontainer, build for all platforms:

# macOS Intel
cargo build --release --target x86_64-apple-darwin

# macOS ARM
cargo build --release --target aarch64-apple-darwin

# Linux x86_64
cross build --release --target x86_64-unknown-linux-gnu

# Windows x86_64
cross build --release --target x86_64-pc-windows-gnu
```

## Architecture

The application follows a modular async architecture with type-safe validation:

### Core Modules

1. **src/error.rs** - Custom error types
   - `IfoError` enum: Comprehensive error types using `thiserror`
   - Automatic conversion from `reqwest::Error`, `serde_json::Error`, `std::io::Error`
   - Type alias `Result<T>` for consistent error handling

2. **src/models.rs** - Data structures with validation
   - `Coordinate`: Type-safe coordinate with validation at construction
   - `BoundingBox`: Geographic bounding box with clamping to valid lat/lon ranges
   - `Aircraft`: Parsed aircraft data from OpenSky state vectors
   - `Location`: Geocoding result with display name
   - All types implement validation in their constructors

3. **src/api.rs** - OpenSky Network API client
   - `OpenSkyClient`: Async HTTP client using `reqwest`
   - `get_aircraft_in_area()`: Queries real-time aircraft data within bounding boxes
   - Connection pooling and timeout handling
   - Parses state vectors into typed `Aircraft` structs

4. **src/geocoding.rs** - Nominatim/OpenStreetMap geocoding client
   - `Geocoder`: Async geocoding with rate limiting
   - Implements precise 1 req/sec rate limiting using `governor` crate
   - Adds jitter to avoid thundering herd
   - Input validation with max length checks

5. **src/main.rs** - CLI interface
   - Command-line argument parsing with `clap` v4 derive macros
   - Mutually exclusive location arguments (coords OR place)
   - Async runtime with `tokio`
   - Integration of all modules

6. **src/lib.rs** - Library root
   - Public exports of modules
   - Convenience re-exports of key types

### Data Flow

1. User provides location (coordinates OR place name) via CLI
2. `clap` validates argument structure
3. If place name: `Geocoder::geocode()` converts to coordinates
4. `Coordinate::new()` validates lat/lon ranges
5. `BoundingBox::from_center()` creates search area (default ±0.5°)
6. `OpenSkyClient::get_aircraft_in_area()` queries API
7. Results parsed into typed `Aircraft` structs
8. Output formatted and displayed

### Key Technologies

- **Async Runtime**: Tokio for efficient concurrent I/O
- **HTTP Client**: reqwest with connection pooling and timeout
- **CLI**: clap v4 with derive macros for type-safe argument parsing
- **Rate Limiting**: governor crate for token bucket algorithm
- **Error Handling**: thiserror for ergonomic error types
- **Serialization**: serde + serde_json for JSON parsing

### Security Features

- All external API calls use HTTPS (enforced by reqwest)
- Type-safe validation at compile time (invalid coordinates can't be constructed)
- Rate limiting for third-party APIs (1 req/sec for Nominatim)
- No credentials or API keys required
- Memory safety guaranteed by Rust
- Input validation with maximum length checks
- Timeout protection on all network requests

### Performance Optimizations

Release profile configured for maximum performance:
- Link-time optimization (LTO)
- Single codegen unit for better optimization
- Maximum optimization level (opt-level = 3)
- Debug symbols stripped
- Results: 2.4MB binary, 3.5ms startup time, 12.5MB memory usage

### Testing Strategy

- Unit tests in each module using `#[cfg(test)]`
- Integration tests for API client behavior
- Tests for coordinate validation and edge cases
- Async tests using `#[tokio::test]`
- Tests cover boundary conditions (poles, date line, invalid inputs)

## Development Practices

- Type-safe design: Invalid states not representable
- Async/await for efficient I/O
- Comprehensive error handling with Result types
- Zero-cost abstractions where possible
- Security by default (HTTPS, validation, rate limiting)

## Release Information

This is a production-ready Rust implementation with comprehensive testing and CI/CD automation for cross-platform releases.
