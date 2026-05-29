# OpenCode Quick Start Guide

How to install and use OpenCode - the open-source AI coding assistant.

---

## Prerequisites

Before installing OpenCode, you need:

1. **Bun** (JavaScript runtime) - OpenCode is built on Bun
2. **An AI API key** (Anthropic, OpenAI, or other provider)

---

## Installation

### Step 1: Install Bun

**Windows (PowerShell):**
```powershell
irm bun.sh/install.ps1 | iex
```

**Mac/Linux:**
```bash
curl -fsSL https://bun.sh/install | bash
```

Verify installation:
```bash
bun --version
```

### Step 2: Install OpenCode

```bash
bun install -g opencode
```

Or using npm:
```bash
npm install -g opencode
```

Verify installation:
```bash
opencode --version
```

### Step 3: Set Up API Key

**Option A: Environment Variable (Recommended)**

Add to your shell profile (~/.bashrc, ~/.zshrc, or Windows environment variables):

```bash
# For Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-..."

# For OpenAI
export OPENAI_API_KEY="sk-..."

# For Google
export GOOGLE_API_KEY="..."
```

**Option B: Interactive Login**

```bash
opencode auth login
```

This opens a browser for authentication.

---

## Basic Usage

### Run a Single Command

```bash
opencode run "Your request here"
```

**Examples:**

```bash
# Fix a bug
opencode run "Fix the type error in auth.ts"

# Add a feature
opencode run "Add a login form to the homepage"

# Explain code
opencode run "Explain what the processPayment function does"

# Refactor
opencode run "Refactor the UserService to use dependency injection"
```

### Continue a Conversation

```bash
# Start a conversation
opencode run "Create a new API endpoint for users"

# Continue the same session
opencode run -c "Now add authentication to it"

# Continue again
opencode run -c "Add unit tests"
```

### Interactive TUI Mode

```bash
opencode
```

This opens a rich terminal interface where you can:
- Type messages interactively
- See real-time responses
- Switch models/agents
- Browse session history

### Specify a Model

```bash
# Use Claude Sonnet
opencode run -m anthropic/claude-sonnet-4 "Explain this code"

# Use Claude Opus
opencode run -m anthropic/claude-opus-4 "Design the architecture"

# Use GPT-4
opencode run -m openai/gpt-4o "Review this code"
```

---

## Common Commands

| Command | Description |
|---------|-------------|
| `opencode` | Start interactive TUI |
| `opencode run "message"` | Run with a message |
| `opencode run -c "message"` | Continue last session |
| `opencode run -m MODEL` | Use specific model |
| `opencode auth login` | Authenticate |
| `opencode auth logout` | Log out |
| `opencode models list` | List available models |
| `opencode session list` | List past sessions |
| `opencode serve` | Start server mode |
| `opencode --help` | Show all commands |

---

## Configuration

### Project Configuration

Create `opencode.json` in your project root:

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4",
  "permissions": {
    "bash": "ask",
    "edit": "allow",
    "read": "allow"
  }
}
```

### User Configuration

Located at `~/.opencode/config.json`:

```json
{
  "theme": "dracula",
  "defaultProvider": "anthropic",
  "defaultModel": "claude-sonnet-4"
}
```

---

## Example Workflows

### 1. Bug Fixing

```bash
# Describe the bug
opencode run "The login button doesn't work on mobile. Fix it."

# OpenCode will:
# 1. Search for relevant files
# 2. Read the code
# 3. Identify the issue
# 4. Fix it
# 5. Explain what was changed
```

### 2. Adding Features

```bash
# Describe what you want
opencode run "Add dark mode support to the app"

# Continue to refine
opencode run -c "Make it remember the user's preference"
opencode run -c "Add a toggle button in the header"
```

### 3. Code Review

```bash
# Ask for review
opencode run "Review the changes in src/api/ for security issues"
```

### 4. Documentation

```bash
# Generate docs
opencode run "Add JSDoc comments to all functions in utils.ts"
```

### 5. Testing

```bash
# Generate tests
opencode run "Write unit tests for the UserService class"
```

---

## Tips for Better Results

### Be Specific

```bash
# Less effective
opencode run "Fix the bug"

# More effective
opencode run "Fix the null pointer error in processOrder() when cart is empty"
```

### Provide Context

```bash
# Include relevant info
opencode run "Add form validation to signup.tsx - validate email format and password must be 8+ characters"
```

### Use Continue for Complex Tasks

```bash
# Break down large tasks
opencode run "Create a REST API for user management"
opencode run -c "Add the POST /users endpoint"
opencode run -c "Add the GET /users/:id endpoint"
opencode run -c "Add authentication middleware"
opencode run -c "Write tests for all endpoints"
```

---

## Troubleshooting

### "API key not found"

Make sure your API key is set:
```bash
echo $ANTHROPIC_API_KEY  # Should show your key
```

### "Command not found: opencode"

Ensure the installation directory is in your PATH:
```bash
# For Bun global installs
export PATH="$HOME/.bun/bin:$PATH"
```

### "Permission denied"

OpenCode asks before risky operations. Type `y` to allow or `n` to deny.

### Slow responses

Try a faster model:
```bash
opencode run -m anthropic/claude-haiku "Quick question"
```

---

## Keyboard Shortcuts (TUI Mode)

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit |
| `↑/↓` | Browse history |
| `Tab` | Autocomplete |
| `Ctrl+L` | Clear screen |

---

## Next Steps

1. Read [BEGINNER_GUIDE.md](./BEGINNER_GUIDE.md) for concepts
2. Check [GLOSSARY.md](./GLOSSARY.md) for term definitions
3. Explore [07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md](./07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md) to understand how it works

---

*Last Updated: January 2026*
