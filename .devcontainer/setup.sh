#!/bin/bash
set -e

echo "🔧 Setting up development environment..."
echo ""

# Set cargo to use user directory (avoid permission issues)
export CARGO_HOME="$HOME/.cargo"
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

# Update package lists (for better dependency resolution)
echo "📦 Updating package lists..."
sudo apt-get update -qq

# Install uv (Python package manager) - idempotent
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "✓ uv already installed"
fi

# Install chunkhound (semantic code search) - idempotent
if ! command -v chunkhound &> /dev/null; then
    echo "🔍 Installing chunkhound..."
    uv tool install chunkhound
else
    echo "✓ chunkhound already installed"
fi

# Index the codebase with chunkhound - idempotent
if [ ! -f ".chunkhound/db" ]; then
    echo "📚 Indexing codebase with chunkhound..."
    chunkhound index --no-embeddings || echo "⚠️  chunkhound indexing failed (non-critical)"
else
    echo "✓ chunkhound database already exists"
fi

# Install Claude Code CLI - idempotent
if ! command -v claude &> /dev/null; then
    echo "🤖 Installing Claude Code CLI..."
    npm install -g @anthropic-ai/claude-code || echo "⚠️  Claude Code CLI installation failed (non-critical)"
else
    echo "✓ Claude Code CLI already installed"
fi

# Configure ChunkHound MCP server for Claude Code - idempotent
if command -v claude &> /dev/null && command -v chunkhound &> /dev/null; then
    if ! claude mcp list 2>&1 | grep -q "chunkhound\|ChunkHound"; then
        echo "🔗 Configuring ChunkHound MCP server for Claude Code..."
        claude mcp add ChunkHound chunkhound mcp || echo "⚠️  ChunkHound MCP configuration failed (non-critical)"
    else
        echo "✓ ChunkHound MCP server already configured"
    fi
fi

# Install OpenAI Codex CLI - idempotent
if ! command -v codex &> /dev/null; then
    echo "🤖 Installing OpenAI Codex CLI..."
    npm install -g @openai/codex || echo "⚠️  OpenAI Codex CLI installation failed (non-critical)"
else
    echo "✓ OpenAI Codex CLI already installed"
fi

# Install cross for cross-compilation - idempotent
if ! command -v cross &> /dev/null; then
    echo "📦 Installing cross tool..."
    cargo install cross --locked
else
    echo "✓ cross already installed"
fi

# Add Rust targets for cross-compilation - idempotent
echo "🎯 Adding Rust targets..."
for target in x86_64-apple-darwin aarch64-apple-darwin x86_64-unknown-linux-gnu x86_64-pc-windows-gnu; do
    if rustup target list --installed | grep -q "^$target\$"; then
        echo "✓ $target already added"
    else
        echo "Adding $target..."
        rustup target add $target
    fi
done

# Install cargo-edit - idempotent
if ! command -v cargo-add &> /dev/null; then
    echo "🛠️  Installing cargo-edit..."
    cargo install cargo-edit --locked || echo "⚠️  cargo-edit installation failed (non-critical)"
else
    echo "✓ cargo-edit already installed"
fi

# Install cargo-watch - idempotent
if ! command -v cargo-watch &> /dev/null; then
    echo "🛠️  Installing cargo-watch..."
    cargo install cargo-watch --locked || echo "⚠️  cargo-watch installation failed (non-critical)"
else
    echo "✓ cargo-watch already installed"
fi

# Verify installations
echo ""
echo "✅ Verifying core installations..."
rustc --version
cargo --version

# Verify optional tools (don't fail if missing)
command -v cross >/dev/null 2>&1 && cross --version || echo "⚠️  cross not installed"
command -v chunkhound >/dev/null 2>&1 && chunkhound --version || echo "⚠️  chunkhound not installed"
command -v chunkhound >/dev/null 2>&1 && [ -f ".chunkhound/db" ] && echo "✓ chunkhound indexed" || echo "⚠️  chunkhound not indexed"
command -v cargo-edit >/dev/null 2>&1 && echo "✓ cargo-edit installed" || echo "⚠️  cargo-edit not installed"
command -v cargo-watch >/dev/null 2>&1 && echo "✓ cargo-watch installed" || echo "⚠️  cargo-watch not installed"
command -v claude >/dev/null 2>&1 && echo "✓ claude CLI installed" || echo "⚠️  claude CLI not installed"
command -v codex >/dev/null 2>&1 && echo "✓ codex CLI installed" || echo "⚠️  codex CLI not installed"
command -v claude >/dev/null 2>&1 && claude mcp list 2>&1 | grep -q "chunkhound\|ChunkHound" && echo "✓ ChunkHound MCP configured" || echo "⚠️  ChunkHound MCP not configured"

# Add to PATH permanently - idempotent
# Add to the beginning of .bashrc (before non-interactive check) so it works in scripts
PATH_EXPORT='export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"'
if ! grep -q "$PATH_EXPORT" ~/.bashrc 2>/dev/null; then
    # Prepend to .bashrc using a temporary file
    echo "$PATH_EXPORT" | cat - ~/.bashrc > ~/.bashrc.tmp && mv ~/.bashrc.tmp ~/.bashrc
fi
if ! grep -q "$PATH_EXPORT" ~/.zshrc 2>/dev/null; then
    echo "$PATH_EXPORT" >> ~/.zshrc
fi

# Source .bashrc to ensure PATH is updated for this session
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
fi

echo "✨ Setup complete! Ready for cross-platform builds."
echo ""
echo "Available targets:"
rustup target list --installed
echo ""
echo "📝 Note: VS Code extensions (Claude Code, OpenAI Codex, etc.) will be"
echo "   automatically installed when you open VS Code in this container."
echo ""
echo "🔍 To verify installation, run: bash .devcontainer/verify.sh"
