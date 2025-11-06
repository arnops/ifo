# IFO Devcontainer

This devcontainer provides a complete Rust cross-compilation environment for building IFO binaries for multiple platforms.

## What's Included

- **Base**: Official Microsoft Rust devcontainer (Debian Bookworm)
- **Rust toolchain**: Latest stable
- **Node.js**: LTS version (for AI extensions and tooling)
- **Python tooling**: `uv` package manager
- **Code search**: `chunkhound` for semantic code search
- **Cross-compilation tool**: `cross` for Docker-based cross-compilation
- **Rust targets**:
  - `x86_64-apple-darwin` (macOS Intel)
  - `aarch64-apple-darwin` (macOS ARM)
  - `x86_64-unknown-linux-gnu` (Linux x86_64)
  - `x86_64-pc-windows-gnu` (Windows x86_64)
- **VS Code extensions**:
  - rust-analyzer (Rust language support)
  - Even Better TOML (TOML syntax)
  - crates (Cargo.toml helper)
  - CodeLLDB (Debugging)
  - Claude Code (Anthropic AI assistant)
  - ChatGPT (OpenAI assistant)
- **Cargo tools**:
  - cargo-edit (cargo add/rm/upgrade commands)
  - cargo-watch (auto-rebuild on changes)

## Usage

### Prerequisites

- Docker Desktop installed and running
- VS Code with "Dev Containers" extension

### Opening the Devcontainer

1. Open this project in VS Code
2. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
3. Select "Dev Containers: Reopen in Container"
4. Wait for the container to build (first time takes ~5-10 minutes)

### Verifying Installation

Once inside the container, run the verification script:

```bash
bash .devcontainer/verify.sh
```

This will check that all tools are installed correctly, including:
- Rust toolchain and targets
- Node.js and npm
- cross, chunkhound, cargo tools
- VS Code extensions (manual verification needed)

### Setting Up AI Assistants

**Claude Code:**
1. Open VS Code Command Palette (`Cmd+Shift+P`)
2. Search for "Claude Code: Set API Key"
3. Enter your Anthropic API key (get one at https://console.anthropic.com/)
4. Alternatively, set `ANTHROPIC_API_KEY` environment variable

**OpenAI Codex (ChatGPT):**
1. Requires ChatGPT Plus, Pro, Business, or Enterprise subscription
2. Click the OpenAI icon in the sidebar
3. Sign in with your ChatGPT account
4. Usage credits are included with your subscription

### Using AI CLI Tools

Both Claude Code and OpenAI Codex are available as CLI commands:

**Claude CLI:**
```bash
# First time: authenticate
claude

# Use in your project
claude "help me implement a function to parse JSON"

# Check version
claude --version
```

**Codex CLI:**
```bash
# First time: sign in
codex

# Use in your project
codex "add error handling to this function"

# Upgrade to latest
codex --upgrade
```

### Building Binaries

Once inside the container:

```bash
# Build for current platform (Linux)
cargo build --release

# Build for macOS Intel
cargo build --release --target x86_64-apple-darwin

# Build for macOS ARM
cargo build --release --target aarch64-apple-darwin

# Build for Windows using cross
cross build --release --target x86_64-pc-windows-gnu

# Build for Linux using cross (ensures glibc compatibility)
cross build --release --target x86_64-unknown-linux-gnu
```

### Running Tests

```bash
cargo test
```

### Code Quality

```bash
# Format code
cargo fmt

# Run linter
cargo clippy
```

### Code Search with ChunkHound

```bash
# Index the codebase (first time or after major changes)
chunkhound index

# Search for code semantically
chunkhound search "function that handles aircraft data"

# Search with filters
chunkhound search "error handling" --file-type rs
```

## Performance

- **Cargo cache**: Mounted volume for faster rebuilds
- **Docker-in-Docker**: Enabled for `cross` tool
- **Incremental compilation**: Enabled by default

## Troubleshooting

### Container won't start
- Ensure Docker Desktop is running
- Try: Dev Containers: Rebuild Container

### Cross builds fail
- Ensure Docker has enough resources (4GB+ RAM recommended)
- Check Docker daemon is accessible: `docker ps`

### Slow builds
- First build downloads toolchains and dependencies (~500MB-1GB)
- Subsequent builds use cached layers and are much faster
