# IFO - Identified Flying Object

[![Pipeline Status](https://gitlab.com/arnops/ifo/badges/main/pipeline.svg)](https://gitlab.com/arnops/ifo/-/pipelines)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://gitlab.com/arnops/ifo/-/releases)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://gitlab.com/arnops/ifo/-/pipelines)
[![Signed Commits](https://img.shields.io/badge/commits-signed-green.svg)](.signing-info)
[![Changelog](https://img.shields.io/badge/changelog-Keep%20a%20Changelog-orange.svg)](CHANGELOG.md)

A blazing-fast Rust CLI application for querying real-time aircraft information flying over any location worldwide.

> **🤖 Built with AI Assistance**
>
> This project was developed with the help of [Claude Code](https://claude.com/claude-code) and enhanced with [ChunkHound](https://chunkhound.github.io) semantic code search for efficient codebase navigation and understanding.

## Features

- 🚀 **Blazing fast**: Sub-5ms startup time, efficient async I/O
- 🌍 **Query by location**: Use coordinates or place names
- ✈️ **Real-time data**: Live aircraft tracking via OpenSky Network API
- 🔍 **Flexible search**: Configurable search radius
- 🔒 **Secure**: Input validation, rate limiting, HTTPS-only
- 💾 **Lightweight**: Single 2.4MB binary, 12.5MB memory footprint

## Performance

- **Startup**: 3.5ms (sub-5ms)
- **Query time**: 133ms average
- **Memory**: 12.5MB lightweight footprint
- **Binary size**: 2.4MB single executable

## Installation

### Pre-built Binary (Recommended)

**Quick Install (Latest Release):**

Visit the [GitLab Releases](https://gitlab.com/arnops/ifo/-/releases) page and download the appropriate binary for your platform.

#### Linux (x86_64)

```bash
# Download the latest release (replace VERSION with actual version, e.g., v0.1.0)
VERSION=v0.1.0
curl -LO "https://gitlab.com/arnops/ifo/-/releases/${VERSION}/downloads/ifo-${VERSION}-linux-x86_64.tar.gz"

# Extract
tar -xzf ifo-${VERSION}-linux-x86_64.tar.gz

# Install system-wide
sudo mv ifo-linux-x86_64 /usr/local/bin/ifo
sudo chmod +x /usr/local/bin/ifo

# Verify installation
ifo --help
```

**Alternative (Manual Download):**
1. Go to https://gitlab.com/arnops/ifo/-/releases
2. Download `ifo-*-linux-x86_64.tar.gz` from the latest release
3. Extract and install as shown above

#### macOS (Intel)

```bash
# Download the latest release (replace VERSION with actual version, e.g., v0.1.0)
VERSION=v0.1.0
curl -LO "https://gitlab.com/arnops/ifo/-/releases/${VERSION}/downloads/ifo-${VERSION}-macos-x86_64.tar.gz"

# Extract
tar -xzf ifo-${VERSION}-macos-x86_64.tar.gz

# Remove quarantine flag (bypasses Gatekeeper warning)
xattr -d com.apple.quarantine ifo-macos-x86_64

# Install system-wide
sudo mv ifo-macos-x86_64 /usr/local/bin/ifo
sudo chmod +x /usr/local/bin/ifo

# Verify installation
ifo --help
```

**Note:** The binary is not code-signed with an Apple Developer certificate. If you see a security warning:
- **Option 1:** Right-click the binary in Finder → "Open" → Click "Open" in the dialog
- **Option 2:** System Preferences → Security & Privacy → Click "Open Anyway"
- **Option 3:** Run `sudo spctl --add /usr/local/bin/ifo` to whitelist it

**Alternative (Manual Download):**
1. Go to https://gitlab.com/arnops/ifo/-/releases
2. Download `ifo-*-macos-x86_64.tar.gz` from the latest release
3. Extract and install as shown above

#### macOS (Apple Silicon)

```bash
# Download the latest release (replace VERSION with actual version, e.g., v0.1.0)
VERSION=v0.1.0
curl -LO "https://gitlab.com/arnops/ifo/-/releases/${VERSION}/downloads/ifo-${VERSION}-macos-aarch64.tar.gz"

# Extract
tar -xzf ifo-${VERSION}-macos-aarch64.tar.gz

# Remove quarantine flag (bypasses Gatekeeper warning)
xattr -d com.apple.quarantine ifo-macos-aarch64

# Install system-wide
sudo mv ifo-macos-aarch64 /usr/local/bin/ifo
sudo chmod +x /usr/local/bin/ifo

# Verify installation
ifo --help
```

**Note:** The binary is not code-signed with an Apple Developer certificate. If you see a security warning:
- **Option 1:** Right-click the binary in Finder → "Open" → Click "Open" in the dialog
- **Option 2:** System Preferences → Security & Privacy → Click "Open Anyway"
- **Option 3:** Run `sudo spctl --add /usr/local/bin/ifo` to whitelist it

**Alternative (Manual Download):**
1. Go to https://gitlab.com/arnops/ifo/-/releases
2. Download `ifo-*-macos-aarch64.tar.gz` from the latest release
3. Extract and install as shown above

#### Windows (x86_64)

```powershell
# PowerShell - Download the latest release (replace VERSION with actual version, e.g., v1.0.0)
$VERSION = "v1.0.0"
Invoke-WebRequest -Uri "https://gitlab.com/arnops/ifo/-/releases/$VERSION/downloads/ifo-$VERSION-windows-x86_64.zip" -OutFile "ifo-$VERSION-windows-x86_64.zip"

# Extract to C:\Program Files\ifo
Expand-Archive -Path "ifo-$VERSION-windows-x86_64.zip" -DestinationPath "C:\Program Files\ifo"

# Rename to ifo.exe
Rename-Item "C:\Program Files\ifo\ifo-windows-x86_64.exe" "ifo.exe"

# Add to PATH (requires admin)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\ifo", [EnvironmentVariableTarget]::Machine)

# Restart terminal and verify
ifo --help
```

**Alternative (Manual Download):**
1. Go to https://gitlab.com/arnops/ifo/-/releases
2. Download `ifo-*-windows-x86_64.zip` from the latest release
3. Extract the zip file
4. Move `ifo-windows-x86_64.exe` to a directory in your PATH (or create `C:\Program Files\ifo`)
5. Rename to `ifo.exe` (optional)
6. Add directory to PATH via System Properties → Environment Variables
7. Run `ifo --help` in Command Prompt or PowerShell

#### Verify Checksums (Recommended)

Download `SHA256SUMS.txt` from the release and verify:

```bash
# Linux/macOS
sha256sum -c SHA256SUMS.txt

# macOS alternative
shasum -a 256 -c SHA256SUMS.txt
```

### Build from Source

```bash
# Clone the repository
git clone <repository-url>
cd ifo

# Build release binary
cargo build --release

# Binary will be at: ./target/release/ifo
```

## Usage

### Query by Coordinates

```bash
ifo --coords "37.7,-122.4"
```

### Query by Place Name

```bash
ifo --place "San Francisco"
ifo --place "London, UK"
ifo --place "Tokyo, Japan"
```

### Custom Search Radius

```bash
# Search radius in degrees (default: 0.5° ≈ 55km)
ifo --place "New York" --radius 1.0
```

### Custom Timeout

```bash
ifo --coords "51.5,-0.1" --timeout 15
```

## Example Output

```
Found location: San Francisco, California, USA (37.7749, -122.4194)
Found 52 aircraft near San Francisco, California, USA:

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
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_bounding_box_validation
```

### Build

```bash
# Debug build
cargo build

# Release build (optimized)
cargo build --release
```

### Project Structure

```
ifo/
├── Cargo.toml         # Package manifest and dependencies
├── src/
│   ├── main.rs        # CLI entry point
│   ├── lib.rs         # Library root
│   ├── api.rs         # OpenSky Network API client
│   ├── geocoding.rs   # Place name to coordinates converter
│   ├── models.rs      # Data structures (Aircraft, BoundingBox, etc.)
│   └── error.rs       # Error types
└── CHANGELOG.md       # Release history
```

## Architecture

The application uses a modular async architecture:

1. **CLI Layer** (`main.rs`): Handles user input and output formatting with clap
2. **Geocoding Layer** (`geocoding.rs`): Converts place names to coordinates using Nominatim/OpenStreetMap
3. **API Layer** (`api.rs`): Queries OpenSky Network for aircraft data
4. **Models Layer** (`models.rs`): Type-safe data structures with validation
5. **Error Layer** (`error.rs`): Comprehensive error handling with thiserror

### Data Sources

- **Aircraft Data**: [OpenSky Network](https://opensky-network.org/) - Community-based ADS-B/Mode S data
- **Geocoding**: [Nominatim](https://nominatim.openstreetmap.org/) - OpenStreetMap geocoding service

### Key Technologies

- **Async Runtime**: Tokio for efficient async I/O
- **HTTP Client**: reqwest with connection pooling
- **CLI Framework**: clap v4 with derive macros
- **Rate Limiting**: governor crate for precise 1 req/sec limit
- **Error Handling**: thiserror for ergonomic error types
- **Serialization**: serde/serde_json for zero-copy JSON parsing

## Security

- All API calls use HTTPS
- Type-safe input validation at compile time
- Rate limiting (1 req/sec for Nominatim API)
- No API keys or credentials required
- Memory-safe Rust implementation

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes, releases, and version notes. We follow [Keep a Changelog](https://keepachangelog.com/) format and [Semantic Versioning](https://semver.org/).

**Latest Release**: [v0.1.0](https://gitlab.com/arnops/ifo/-/releases/v0.1.0) - Initial release with cross-platform binaries and automated CI/CD.

## Branding

- GitLab project icon: `assets/gitlab-project-icon.svg` (512×512, vector, gradient background with aircraft motif)

## License

This project is licensed under the [MIT License](https://opensource.org/license/MIT) - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please ensure:
- All tests pass (`cargo test`)
- Code follows Rust best practices (`cargo clippy`)
- Format code (`cargo fmt`)
- **Sign your commits** using SSH or GPG (see [.signing-info](.signing-info) for setup instructions)

### Setting Up Commit Signing

This project requires signed commits for security and authenticity. We use SSH-based signing (Git 2.34+):

```bash
# Configure SSH signing (recommended)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

See [.signing-info](.signing-info) for detailed instructions.
