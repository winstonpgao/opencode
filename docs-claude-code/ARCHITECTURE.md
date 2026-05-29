# Architecture Overview: How AI Coding Assistants Work

This document explains the architecture of OpenCode and Claude Code.

---

## The Three Layers

```
+------------------------------------------------------------------+
|                         LAYER 1: USER INTERFACE                   |
|                                                                   |
|   +----------+    +----------+    +----------+    +----------+   |
|   |   TUI    |    |   CLI    |    |   Web    |    |   IDE    |   |
|   | Terminal |    | Commands |    | Browser  |    | VS Code  |   |
|   +----------+    +----------+    +----------+    +----------+   |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                         LAYER 2: CORE ENGINE                      |
|                                                                   |
|   +----------+    +----------+    +----------+    +----------+   |
|   |  Agent   |    |  Tools   |    | Session  |    | Provider |   |
|   | Manager  |    | Registry |    | Manager  |    | Bridge   |   |
|   +----------+    +----------+    +----------+    +----------+   |
|                                                                   |
|   +----------+    +----------+    +----------+    +----------+   |
|   |Permission|    |  Config  |    |   MCP    |    |   LSP    |   |
|   |  System  |    |  Loader  |    | Servers  |    | Servers  |   |
|   +----------+    +----------+    +----------+    +----------+   |
+------------------------------------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
|                         LAYER 3: AI PROVIDERS                     |
|                                                                   |
|   +----------+    +----------+    +----------+    +----------+   |
|   |  Claude  |    |  OpenAI  |    |  Gemini  |    |  Local   |   |
|   | Anthropic|    |   GPT    |    |  Google  |    |  Models  |   |
|   +----------+    +----------+    +----------+    +----------+   |
+------------------------------------------------------------------+
```

---

## Component Details

### Layer 1: User Interface

**What it does:** How you interact with the AI

| Component | Description |
|-----------|-------------|
| TUI | Terminal User Interface - colorful terminal app |
| CLI | Command Line Interface - simple text commands |
| Web | Browser-based interface |
| IDE | Editor integrations (VS Code, etc.) |

---

### Layer 2: Core Engine

**What it does:** The brain that coordinates everything

#### Agent Manager
```
Purpose: Controls which "personality" the AI uses

Agents:
  - build: Full access, can edit files
  - plan: Read-only, for exploration
  - general: Subagent for complex tasks

Each agent has:
  - Name
  - Permissions (what tools it can use)
  - Prompt (personality instructions)
```

#### Tools Registry
```
Purpose: Manages all available tools

Tools are registered with:
  - Name (read, write, bash, etc.)
  - Parameters (what inputs it needs)
  - Execute function (what it does)
  - Prompt (instructions for AI)
```

#### Session Manager
```
Purpose: Manages the conversation

Tracks:
  - Message history
  - Context window
  - Token usage
  - Current state
```

#### Provider Bridge
```
Purpose: Connects to AI providers

Handles:
  - API authentication
  - Request formatting
  - Response parsing
  - Streaming
```

#### Permission System
```
Purpose: Controls what AI can do

Rules:
  - allow: Always permit
  - deny: Always block
  - ask: Prompt user first

Applied to:
  - Each tool
  - File patterns
  - Commands
```

#### Config Loader
```
Purpose: Loads settings

From:
  - opencode.json (project config)
  - ~/.opencode/config.json (user config)
  - Environment variables
```

#### MCP Servers
```
Purpose: Model Context Protocol - external tools

Allows:
  - Third-party tools
  - Database connections
  - API integrations
```

#### LSP Servers
```
Purpose: Language Server Protocol

Provides:
  - Code completion
  - Error detection
  - Go to definition
  - Refactoring
```

---

## Message Flow

### Step-by-Step: User Request to Response

```
1. USER INPUT
   +------------------+
   | "Add login form" |
   +------------------+
           |
           v
2. SESSION RECEIVES
   +------------------+
   | Create message   |
   | Add to history   |
   +------------------+
           |
           v
3. CONTEXT BUILDING
   +------------------+
   | System prompt    |
   | + Message history|
   | + Current state  |
   +------------------+
           |
           v
4. PROVIDER CALL
   +------------------+
   | Send to Claude   |
   | or OpenAI, etc.  |
   +------------------+
           |
           v
5. AI RESPONSE
   +------------------+
   | "I'll read the   |
   |  existing files" |
   | Tool: Read       |
   +------------------+
           |
           v
6. TOOL EXECUTION
   +------------------+
   | Check permission |
   | Execute Read     |
   | Return content   |
   +------------------+
           |
           v
7. BACK TO AI
   +------------------+
   | "Now I see the   |
   |  structure..."   |
   | Tool: Edit       |
   +------------------+
           |
           v
8. MORE TOOLS...
   (repeat 6-7 as needed)
           |
           v
9. FINAL RESPONSE
   +------------------+
   | "Done! I added   |
   |  the login form" |
   +------------------+
           |
           v
10. USER SEES RESULT
```

---

## File Structure Mapping

### OpenCode Source Code

```
packages/opencode/src/
|
+-- agent/           # Agent definitions and management
|   +-- agent.ts     # Main agent logic
|   +-- prompt/      # Agent-specific prompts
|
+-- tool/            # All tools
|   +-- read.ts      # Read tool
|   +-- read.txt     # Read tool prompt
|   +-- write.ts     # Write tool
|   +-- write.txt    # Write tool prompt
|   +-- bash.ts      # Bash tool
|   +-- bash.txt     # Bash tool prompt
|   +-- edit.ts      # Edit tool
|   +-- edit.txt     # Edit tool prompt
|   +-- grep.ts      # Grep tool
|   +-- glob.ts      # Glob tool
|   +-- ... etc
|
+-- session/         # Conversation management
|   +-- session.ts   # Session state
|   +-- system.ts    # System prompt builder
|
+-- provider/        # AI provider connections
|   +-- provider.ts  # Provider interface
|   +-- transform.ts # Request/response transforms
|
+-- permission/      # Permission system
|   +-- next.ts      # Permission rules
|
+-- config/          # Configuration
|   +-- config.ts    # Config loading
|
+-- mcp/             # MCP server support
+-- lsp/             # LSP server support
+-- cli/             # Command line interface
+-- server/          # HTTP server for remote access
```

---

## Key Concepts

### 1. Tool Loop

The AI operates in a loop:
```
Think -> Use Tool -> See Result -> Think -> Use Tool -> ... -> Done
```

This continues until:
- Task is complete
- User interrupts
- Error occurs
- Max iterations reached

### 2. Context Window

The AI has limited "memory" (context window):
```
+----------------------------------+
|  System Prompt (instructions)    | ~2000 tokens
+----------------------------------+
|  Conversation History            | Variable
+----------------------------------+
|  Current File Contents           | Variable
+----------------------------------+
|  Tool Results                    | Variable
+----------------------------------+
         TOTAL: ~128k-200k tokens
```

When context gets full:
- Old messages are summarized
- Less important content is dropped
- Critical context is preserved

### 3. Streaming

Responses come in chunks:
```
"I" -> "I will" -> "I will read" -> "I will read the" -> "I will read the file"
```

This allows:
- Faster perceived response
- Early cancellation
- Progress indication

---

## Security Model

### What AI CAN do:
- Read files (with permission for sensitive files)
- Write files in project directory
- Run allowed commands
- Search the internet
- Use approved MCP tools

### What AI CANNOT do:
- Access files outside project (without permission)
- Run dangerous commands (without permission)
- Send data to unauthorized servers
- Modify system files
- Execute arbitrary code without sandbox

### Permission Flow:
```
AI wants to use tool
        |
        v
Check permission rules
        |
    +---+---+
    |       |
  allow   deny/ask
    |       |
    v       v
Execute   Block or
  tool    Ask user
```

---

## Summary

The architecture follows a clean separation:

1. **Interface Layer** - How you interact
2. **Core Engine** - Coordination and logic
3. **Provider Layer** - AI model communication

This design allows:
- Multiple interfaces (terminal, web, IDE)
- Multiple AI providers (Claude, GPT, etc.)
- Extensibility (MCP, plugins)
- Security (permissions, sandboxing)
