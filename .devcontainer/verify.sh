#!/bin/bash
# Verification script for devcontainer setup

set -e

# Ensure PATH includes .cargo/bin and .local/bin
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

echo "🔍 Verifying devcontainer installation..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        if [ "$2" = "version" ]; then
            $1 --version 2>&1 | head -1 | sed 's/^/  /'
        fi
    else
        echo -e "${RED}✗${NC} $1 is NOT installed"
        return 1
    fi
}

echo "=== Core Tools ==="
check_command rustc version
check_command cargo version
check_command node version
check_command npm version
echo ""

echo "=== Cross-Compilation ==="
check_command cross version
check_command docker version
echo ""

echo "=== Rust Targets ==="
rustup target list --installed | while read target; do
    echo -e "${GREEN}✓${NC} $target"
done
echo ""

echo "=== Python & Code Search ==="
check_command uv version
check_command chunkhound version

# Check if chunkhound is indexed
if [ -f ".chunkhound/db" ]; then
    echo -e "${GREEN}✓${NC} chunkhound database exists"
else
    echo -e "${RED}✗${NC} chunkhound database NOT found (run: chunkhound index --no-embeddings)"
fi

# Test chunkhound search functionality
if command -v chunkhound &> /dev/null; then
    if chunkhound search --regex "use " --no-embeddings > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} chunkhound search is functional"
    else
        echo -e "${YELLOW}⚠${NC}  chunkhound search test failed (database may need indexing)"
    fi
fi
echo ""

echo "=== AI CLI Tools ==="
check_command claude version
check_command codex
echo ""

echo "=== MCP Integration ==="
# Check if ChunkHound is configured as MCP server
if command -v claude &> /dev/null; then
    if claude mcp list 2>&1 | grep -q "chunkhound\|ChunkHound"; then
        echo -e "${GREEN}✓${NC} ChunkHound MCP server is configured"
    else
        echo -e "${YELLOW}⚠${NC}  ChunkHound MCP server NOT configured"
        echo "    To add: claude mcp add ChunkHound chunkhound mcp"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Claude CLI not available, cannot check MCP configuration"
fi
echo ""

echo "=== Cargo Tools ==="
check_command cargo-add
check_command cargo-watch
echo ""

echo "=== VS Code Extensions (run 'code --list-extensions' to verify) ==="
echo -e "${YELLOW}Note:${NC} Extensions are auto-installed by VS Code when container starts"
echo "Expected extensions:"
echo "  - rust-lang.rust-analyzer"
echo "  - tamasfe.even-better-toml"
echo "  - serayuzgur.crates"
echo "  - vadimcn.vscode-lldb"
echo "  - anthropic.claude-code"
echo "  - openai.chatgpt"
echo ""

echo "=== Authentication Requirements ==="
echo -e "${YELLOW}Claude Code:${NC}"
echo "  - Requires Anthropic API key"
echo "  - Set via VS Code or environment variable ANTHROPIC_API_KEY"
echo ""
echo -e "${YELLOW}OpenAI Codex:${NC}"
echo "  - Requires ChatGPT Plus/Pro/Business/Enterprise subscription"
echo "  - Sign in via VS Code extension"
echo ""

echo "=== Summary ==="
echo -e "${GREEN}✓${NC} Devcontainer setup complete!"
echo ""
echo "Next steps:"
echo "  1. Verify VS Code extensions: Cmd+Shift+X and check installed"
echo "  2. Authenticate Claude Code with your API key"
echo "  3. Sign in to OpenAI Codex extension"
echo "  4. Start coding!"
