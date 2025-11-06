# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-06

### Added
- **Core Functionality**: Query aircraft by coordinates or place name
- **OpenSky Network Integration**: Real-time aircraft tracking with REST API client
- **Nominatim Geocoding**: Convert place names to coordinates with rate limiting
- **CLI Interface**: User-friendly command-line interface with clap v4
- **Cross-platform Binaries**: Automated CI/CD with GitLab and GitHub Actions
  - Linux x86_64
  - macOS Intel (x86_64)
  - macOS Apple Silicon (aarch64)
  - Windows x86_64
- **Security Features**:
  - SSH-based commit signing
  - Input validation and type safety
  - Rate limiting (1 req/sec for Nominatim)
  - HTTPS-only API calls
- **Performance**:
  - 3.5ms startup time
  - 12.5MB memory footprint
  - 2.4MB binary size
- **Documentation**: Complete README, CLAUDE.md, and inline code documentation
- **License**: MIT License

## Links

- **Repository**: https://gitlab.com/arnops/ifo
- **Releases**: https://gitlab.com/arnops/ifo/-/releases
- **Issues**: https://gitlab.com/arnops/ifo/-/issues
- **License**: [MIT](https://opensource.org/license/MIT)

[0.1.0]: https://gitlab.com/arnops/ifo/-/releases/v0.1.0
