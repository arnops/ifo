# Installation

## Pre-built Binary (Recommended)

**Quick Install (Latest Release):**

Visit the [GitLab Releases](https://gitlab.com/arnops/ifo/-/releases) page and download the appropriate binary for your platform.

### Linux (x86_64)

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

### macOS (Intel)

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

### macOS (Apple Silicon)

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

### Windows (x86_64)

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

### Verify Checksums (Recommended)

Download `SHA256SUMS.txt` from the release and verify:

```bash
# Linux/macOS
sha256sum -c SHA256SUMS.txt

# macOS alternative
shasum -a 256 -c SHA256SUMS.txt
```

## Build from Source

```bash
# Clone the repository
git clone <repository-url>
cd ifo

# Build release binary
cargo build --release

# Binary will be at: ./target/release/ifo
```
