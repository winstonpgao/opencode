# Complete Guide: Claude Code, OpenCode, and How Coding Agents Work

**Purpose**: This document provides a beginner-friendly, comprehensive guide to understanding how AI coding agents work, using Claude Code and OpenCode as examples.

**For**: Sonnet 3.5 agents, developers learning about agentic systems, anyone building coding assistants

---

# TABLE OF CONTENTS

1. [What is a Coding Agent?](#part-1-what-is-a-coding-agent)
2. [Claude Code: Complete Reference](#part-2-claude-code-complete-reference)
3. [OpenCode: Anatomy of a Coding Agent](#part-3-opencode-anatomy-of-a-coding-agent)
4. [Side-by-Side Comparison](#part-4-side-by-side-comparison)
5. [The Agent Loop Explained](#part-5-the-agent-loop-explained)
6. [Tools Deep Dive](#part-6-tools-deep-dive)
7. [Building Your Own Coding Agent](#part-7-building-your-own-coding-agent)

---

# PART 1: WHAT IS A CODING AGENT?

## 1.1 Definition

A **coding agent** is an AI system that can:
1. Understand programming tasks in natural language
2. Read and analyze code files
3. Execute shell commands
4. Write and modify code
5. **Loop** until the task is complete

## 1.2 Key Difference from ChatGPT

| Aspect | ChatGPT / Claude.ai | Coding Agent (Claude Code, OpenCode) |
|--------|---------------------|--------------------------------------|
| **File Access** | Upload only | Full read/write to your filesystem |
| **Shell Access** | None | Yes, can run commands |
| **Loop** | Single turn (ask → answer) | Multi-turn (ask → act → observe → act...) |
| **Persistence** | Optional | Full session history |
| **Tool Approval** | Automatic | User approval for dangerous operations |

## 1.3 The "Agentic Loop" Pattern

This is the core of every coding agent:

```
┌─────────────────────────────────────────────┐
│                 AGENT LOOP                   │
├─────────────────────────────────────────────┤
│                                             │
│   User: "Fix the bug in auth.py"           │
│         ↓                                  │
│   ┌──────────────┐                         │
│   │    LLM       │ ← System Prompt         │
│   │   (Claude)   │ ← Message History       │
│   │              │ ← Tool Definitions      │
│   └──────┬───────┘                         │
│          ↓                                  │
│   Response: "I'll read the file first"     │
│   Tool Call: view("auth.py")               │
│          ↓                                  │
│   ┌──────────────┐                         │
│   │  TOOL        │                         │
│   │  Execution   │ → Returns file contents │
│   └──────┬───────┘                         │
│          ↓                                  │
│   Append result to message history          │
│          ↓                                  │
│   ┌──────────────┐                         │
│   │    LLM       │ ← Now sees file contents│
│   │   (Claude)   │                         │
│   └──────┬───────┘                         │
│          ↓                                  │
│   Response: "Found the bug, fixing..."     │
│   Tool Call: edit("auth.py", old, new)     │
│          ↓                                  │
│   ┌──────────────┐                         │
│   │  Permission  │ → "Allow edit?" [Y/N]   │
│   │  Dialog      │                         │
│   └──────┬───────┘                         │
│          ↓                                  │
│   Tool executes, file modified              │
│          ↓                                  │
│   Loop continues until LLM says "done"      │
│                                             │
└─────────────────────────────────────────────┘
```

---

# PART 2: CLAUDE CODE COMPLETE REFERENCE

## 2.1 What is Claude Code?

Claude Code is Anthropic's official CLI tool for AI-assisted coding. It runs in your terminal and provides:
- Direct filesystem access
- Shell command execution
- Multi-model support
- Session persistence
- Extensibility through Skills, MCP, and Hooks

## 2.2 Claude Code Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   USER INTERFACE                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │    CLI      │  │  VS Code    │  │  JetBrains  │  │   │
│  │  │  Terminal   │  │  Extension  │  │  Extension  │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └─────────────────────────┬───────────────────────────┘   │
│                            ↓                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  CORE ENGINE                         │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │               Agent Loop                     │    │   │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │    │   │
│  │  │  │ Message │→ │ LLM API │→ │ Tool Execute│  │    │   │
│  │  │  │ History │  │ (Claude)│  │ (if needed) │  │    │   │
│  │  │  └─────────┘  └─────────┘  └──────┬──────┘  │    │   │
│  │  │       ↑                           │         │    │   │
│  │  │       └───────────────────────────┘         │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  └─────────────────────────┬───────────────────────────┘   │
│                            ↓                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    TOOLS LAYER                       │   │
│  │  ┌─────┐ ┌─────┐ ┌────┐ ┌─────┐ ┌────┐ ┌─────────┐  │   │
│  │  │Read │ │Write│ │Edit│ │Bash │ │Glob│ │WebSearch│  │   │
│  │  └─────┘ └─────┘ └────┘ └─────┘ └────┘ └─────────┘  │   │
│  │  ┌─────┐ ┌──────────┐ ┌────┐ ┌─────────────────┐    │   │
│  │  │Grep │ │WebFetch  │ │Task│ │NotebookEdit     │    │   │
│  │  └─────┘ └──────────┘ └────┘ └─────────────────┘    │   │
│  └─────────────────────────┬───────────────────────────┘   │
│                            ↓                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  EXTENSIONS                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │   Skills    │  │    MCP      │  │    Hooks    │  │   │
│  │  │ (SKILL.md)  │  │  Servers    │  │  (Scripts)  │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 2.3 Claude Code Tools - Complete List

### Built-in Tools (20 total)

| Tool | Tokens | Purpose | Example Usage |
|------|--------|---------|---------------|
| **Read** | 439 | Read file contents | `Read file_path="/path/file.py"` |
| **Write** | 159 | Create/overwrite files | `Write file_path="/path/file.py" content="..."` |
| **Edit** | 278 | Replace text in files | `Edit file_path="/path/file.py" old_string="..." new_string="..."` |
| **Bash** | 1,047 | Execute shell commands | `Bash command="npm test"` |
| **Glob** | 122 | Find files by pattern | `Glob pattern="**/*.py"` |
| **Grep** | 300 | Search file contents | `Grep pattern="def main" type="py"` |
| **Task** | 1,264 | Spawn sub-agents | `Task prompt="Search for auth code" subagent_type="Explore"` |
| **WebSearch** | 329 | Search the web | `WebSearch query="React hooks 2026"` |
| **WebFetch** | 265 | Fetch web page content | `WebFetch url="https://..." prompt="..."` |
| **TodoWrite** | 2,167 | Track task progress | `TodoWrite todos=[{content: "...", status: "in_progress"}]` |
| **AskUserQuestion** | 194 | Get user input | `AskUserQuestion questions=[{question: "...", options: [...]}]` |
| **NotebookEdit** | 121 | Edit Jupyter notebooks | `NotebookEdit notebook_path="..." new_source="..."` |
| **EnterPlanMode** | 970 | Start planning mode | `EnterPlanMode` |
| **ExitPlanMode** | 738 | Present plan to user | `ExitPlanMode` |
| **Skill** | 444 | Execute a skill | `Skill skill="commit"` |
| **MCPSearch** | 477 | Search MCP tools | `MCPSearch query="database"` |
| **LSP** | 255 | Language Server access | `LSP action="diagnostics"` |
| **Computer** | 161 | Browser automation | `Computer action="click"` |
| **KillShell** | N/A | Kill background task | `KillShell shell_id="..."` |
| **TaskOutput** | N/A | Get task output | `TaskOutput task_id="..."` |

### Tool Details

#### Read Tool
```yaml
Purpose: Read file contents
Parameters:
  - file_path (required): Absolute path to file
  - offset (optional): Line number to start from
  - limit (optional): Number of lines to read (default 2000)
Features:
  - Reads images (PNG, JPG) - multimodal
  - Reads PDFs (page by page)
  - Reads Jupyter notebooks (.ipynb)
  - Returns line numbers: "   42→content here"
Limits:
  - Lines truncated at 2000 characters
  - Max file size varies by type
```

#### Write Tool
```yaml
Purpose: Create or overwrite files
Parameters:
  - file_path (required): Absolute path
  - content (required): Full file content
Requirements:
  - Must Read file first if it exists
  - Creates parent directories automatically
```

#### Edit Tool
```yaml
Purpose: Replace text in existing files
Parameters:
  - file_path (required): Absolute path
  - old_string (required): Exact text to replace
  - new_string (required): Replacement text
  - replace_all (optional): Replace all occurrences (default false)
Requirements:
  - Must Read file first
  - old_string must be unique in file (or use replace_all)
  - Preserve exact indentation
```

#### Bash Tool
```yaml
Purpose: Execute shell commands
Parameters:
  - command (required): Command to execute
  - description (optional): What command does
  - timeout (optional): Max milliseconds (default 120000, max 600000)
  - run_in_background (optional): Run async
Features:
  - Persistent shell session
  - Output truncated at 30000 characters
Safety:
  - Sandboxed execution
  - Requires permission for destructive operations
```

#### Task Tool (Sub-agents)
```yaml
Purpose: Spawn specialized agents
Parameters:
  - prompt (required): Task description
  - subagent_type (required): Agent type
  - description (required): Short summary
  - model (optional): sonnet, opus, or haiku
  - run_in_background (optional): Run async
  - resume (optional): Continue previous agent

Available Agent Types:
  - Bash: Command execution specialist
  - Explore: Fast codebase exploration
  - Plan: Software architecture planning
  - general-purpose: Multi-step tasks
  - claude-code-guide: Help with Claude Code itself
```

## 2.4 Claude Code Skills

### What are Skills?

Skills are **instruction packages** (NOT tools) that teach Claude how to do something specific. They inject knowledge into the conversation.

### Skill File Structure

```
~/.claude/skills/
└── my-skill/
    ├── SKILL.md          # Required - metadata + instructions
    ├── reference.md      # Optional - detailed docs
    └── scripts/
        └── helper.py     # Optional - executable scripts
```

### SKILL.md Format

```yaml
---
name: my-skill-name
description: When to use this skill (used for auto-discovery)
allowed-tools: Read, Grep, Glob  # Optional: restrict tools
model: claude-sonnet-4           # Optional: specific model
context: fork                    # Optional: run in sub-agent
user-invocable: true             # Optional: show in /skill menu
---

# Skill Instructions

These instructions are injected into the conversation when the skill is invoked.

## What to do
1. Step one
2. Step two

## Examples
...
```

### Skills vs Tools vs MCP

| Aspect | Skills | Tools | MCP |
|--------|--------|-------|-----|
| **What it is** | Instructions (markdown) | Functions (code) | External servers |
| **Purpose** | Teach Claude HOW | Give Claude ABILITY | Connect Claude to services |
| **Invocation** | Auto or /skill | Claude calls directly | Claude calls as tool |
| **Example** | "Follow PR review checklist" | "Read this file" | "Query this database" |

### Example Skill: PR Review

```yaml
---
name: pr-review
description: Review pull requests following team standards. Use when reviewing PRs or code changes.
---

# PR Review Checklist

When reviewing code changes:

## 1. Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented

## 2. Performance
- [ ] No N+1 queries
- [ ] Appropriate caching

## 3. Code Quality
- [ ] Functions under 50 lines
- [ ] Clear naming
- [ ] Tests included

Always provide specific line numbers with feedback.
```

## 2.5 Claude Code Slash Commands

### Built-in Commands (40+)

| Command | Purpose |
|---------|---------|
| `/help` | Show all commands |
| `/clear` | Clear conversation |
| `/compact` | Summarize conversation |
| `/config` | Open settings |
| `/context` | Show context usage |
| `/cost` | Show token usage |
| `/model` | Change AI model |
| `/mcp` | Manage MCP servers |
| `/plan` | Enter plan mode |
| `/resume` | Resume previous session |
| `/todos` | Show task list |
| `/export` | Export conversation |

### Custom Slash Commands

Create `.claude/commands/my-command.md`:

```markdown
---
description: What this command does
allowed-tools: Bash(git:*)
argument-hint: [message]
---

Create a git commit with message: $ARGUMENTS

Use conventional commits format.
```

Usage: `/my-command fix auth bug`

### Command Variables

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed |
| `$1`, `$2` | Individual arguments |
| `@file.txt` | Include file contents |
| `!git status` | Execute bash and include output |

## 2.6 Claude Code Hooks

### What are Hooks?

Hooks are scripts that run at specific points in Claude's workflow.

### Hook Events

| Event | When it Fires | Use Case |
|-------|---------------|----------|
| **PreToolUse** | Before tool executes | Validate, allow/deny |
| **PostToolUse** | After tool completes | Format, log |
| **Stop** | When agent finishes | Check if complete |
| **SessionStart** | On startup/resume | Load context |
| **UserPromptSubmit** | On user input | Add context |
| **PermissionRequest** | On permission dialog | Auto-approve |

### Hook Configuration

In `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Input/Output

**Input (JSON via stdin):**
```json
{
  "session_id": "abc123",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/test"
  }
}
```

**Output (JSON to stdout):**
```json
{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow"
  }
}
```

## 2.7 Claude Code MCP Integration

### What is MCP?

MCP (Model Context Protocol) is an open standard for connecting AI to external tools and data sources.

### Adding MCP Servers

```bash
# HTTP server (recommended)
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Stdio server (local process)
claude mcp add --transport stdio db -- npx -y @some/db-server
```

### .mcp.json Format

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "local-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@some/db-server"],
      "env": {
        "DB_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### MCP Scopes

| Scope | Location | Shared? |
|-------|----------|---------|
| Local | `~/.claude.json` | No |
| Project | `.mcp.json` | Yes (team) |
| User | `~/.claude.json` | No (all projects) |

---

# PART 3: OPENCODE ANATOMY OF A CODING AGENT

## 3.1 What is OpenCode?

OpenCode was a Go-based terminal AI coding assistant (now archived, continued as "Crush"). It's an excellent educational example of how to build a coding agent.

**GitHub**: https://github.com/opencode-ai/opencode

**Note**: Repository was archived September 2025. Development continues at https://github.com/charmbracelet/crush

## 3.2 OpenCode Directory Structure

```
opencode/
├── main.go                          # Entry point
├── cmd/
│   └── root.go                      # CLI & app initialization
├── internal/
│   ├── app/
│   │   └── app.go                   # Core application service
│   ├── llm/
│   │   ├── agent/
│   │   │   ├── agent.go             # THE AGENT LOOP (critical!)
│   │   │   ├── tools.go             # Tool registry
│   │   │   └── mcp-tools.go         # MCP integration
│   │   ├── provider/
│   │   │   ├── provider.go          # Provider interface
│   │   │   ├── anthropic.go         # Claude API
│   │   │   ├── openai.go            # OpenAI API
│   │   │   └── gemini.go            # Google Gemini
│   │   ├── prompt/
│   │   │   └── coder.go             # SYSTEM PROMPTS
│   │   └── tools/
│   │       ├── bash.go              # Bash tool
│   │       ├── view.go              # File read tool
│   │       ├── edit.go              # File edit tool
│   │       ├── write.go             # File write tool
│   │       ├── glob.go              # File search tool
│   │       └── grep.go              # Content search tool
│   ├── session/
│   │   └── session.go               # Session management
│   ├── message/
│   │   └── message.go               # Message storage
│   ├── db/
│   │   └── connect.go               # SQLite database
│   ├── permission/
│   │   └── permission.go            # Permission gates
│   └── tui/
│       └── tui.go                   # Terminal UI (Bubble Tea)
├── go.mod                           # Dependencies
└── README.md                        # Documentation
```

## 3.3 OpenCode Agent Loop (THE CRITICAL CODE)

**File**: `internal/llm/agent/agent.go`

```go
// This is the heart of the coding agent!
for {
    // 1. Check if user cancelled
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }

    // 2. Send messages to LLM, get response + tool calls
    agentMessage, toolResults, err := a.streamAndHandleEvents(
        ctx, sessionID, msgHistory
    )

    // 3. If LLM wants to use tools
    if agentMessage.FinishReason() == message.FinishReasonToolUse {
        // Tool results were already executed in streamAndHandleEvents
        // Append both to message history
        msgHistory = append(msgHistory, agentMessage, *toolResults)
        continue  // <-- LOOP BACK! Send updated history to LLM
    }

    // 4. If LLM is done (no more tool calls)
    return AgentEvent{
        Message: agentMessage,
        Done:    true,
    }
}
```

**Key insight**: The loop continues as long as the LLM requests tool calls!

## 3.4 OpenCode Tools

### Tool Interface

```go
type BaseTool interface {
    Info() ToolInfo           // Name, description, parameters
    Run(ctx, call) Response   // Execute the tool
}

type ToolInfo struct {
    Name        string
    Description string
    Parameters  map[string]Parameter
    Required    []string
}
```

### Bash Tool Implementation

```go
func (b *bashTool) Run(ctx context.Context, call ToolCall) (ToolResponse, error) {
    // 1. Parse parameters
    params := BashParams{}
    json.Unmarshal(call.Input, &params)

    // 2. Request permission (blocks until user approves)
    approved := b.permissions.Request(PermissionRequest{
        ToolName: "bash",
        Action:   "execute",
        Description: params.Command,
    })
    if !approved {
        return ErrorResponse("Permission denied")
    }

    // 3. Check for banned commands
    banned := []string{"curl", "wget", "nc", "telnet"}
    for _, b := range banned {
        if strings.Contains(params.Command, b) {
            return ErrorResponse("Command not allowed")
        }
    }

    // 4. Execute command
    cmd := exec.Command("bash", "-c", params.Command)
    output, _ := cmd.CombinedOutput()

    // 5. Truncate if too long (30,000 chars)
    if len(output) > 30000 {
        output = output[:30000] + "\n... (truncated)"
    }

    return TextResponse(string(output))
}
```

### Edit Tool Implementation

```go
func (e *editTool) Run(ctx context.Context, call ToolCall) (ToolResponse, error) {
    params := EditParams{}
    json.Unmarshal(call.Input, &params)

    // 1. Request permission
    approved := e.permissions.Request(...)
    if !approved { return error }

    // 2. Read file
    content, _ := os.ReadFile(params.FilePath)

    // 3. Find and replace (EXACTLY ONE occurrence)
    if !strings.Contains(string(content), params.OldString) {
        return ErrorResponse("old_string not found in file")
    }

    newContent := strings.Replace(
        string(content),
        params.OldString,
        params.NewString,
        1,  // Only replace FIRST occurrence
    )

    // 4. Write file
    os.WriteFile(params.FilePath, []byte(newContent), 0644)

    // 5. Track in history
    e.history.RecordEdit(params.FilePath, newContent)

    return TextResponse("File edited successfully")
}
```

## 3.5 OpenCode System Prompt

**File**: `internal/llm/prompt/coder.go`

```
You are OpenCode, an interactive CLI tool that helps users with
software engineering tasks.

# Memory
If OpenCode.md exists, it contains:
1. Frequently used bash commands (build, test, lint)
2. Code style preferences
3. Useful codebase information

# Tone and Style
- Be concise, direct, to the point
- Minimize output tokens
- MUST answer with fewer than 4 lines (unless user asks for detail)
- One word answers are best

# Proactiveness
- Only do what the user asks
- Ask before adding commands to OpenCode.md
- Don't surprise users

# Following Conventions
- First understand code conventions
- NEVER assume libraries are available
- Check neighboring files for patterns
- Always follow security best practices

# Tool Usage Policy
- Prefer Agent tool for file searching (reduces context)
- Use View/Glob for specific file reads
- Make parallel tool calls when no dependencies
```

## 3.6 OpenCode Permission System

```go
func (s *permissionService) Request(req PermissionRequest) bool {
    // 1. Check if already approved this session
    for _, p := range s.sessionPermissions {
        if matches(p, req) {
            return true
        }
    }

    // 2. Publish event to TUI
    s.Publish(pubsub.CreatedEvent, req)

    // 3. Create response channel
    respCh := make(chan bool, 1)
    s.pendingRequests.Store(req.ID, respCh)

    // 4. BLOCK until user responds in TUI
    return <-respCh
}

func (s *permissionService) Grant(req PermissionRequest) {
    respCh, _ := s.pendingRequests.Load(req.ID)
    respCh.(chan bool) <- true  // Unblock the tool
}
```

**The flow**:
1. Tool calls `permissions.Request()`
2. TUI shows dialog to user
3. Tool execution **blocks** on channel
4. User approves/denies
5. Response sent through channel
6. Tool continues

## 3.7 OpenCode LLM Provider Pattern

```go
type Provider interface {
    SendMessages(ctx, messages, tools) (*Response, error)
    StreamResponse(ctx, messages, tools) <-chan Event
    Model() Model
}

func NewProvider(name ModelProvider) Provider {
    switch name {
    case ProviderAnthropic:
        return &anthropicProvider{client: anthropic.NewClient()}
    case ProviderOpenAI:
        return &openaiProvider{client: openai.NewClient()}
    case ProviderGemini:
        return &geminiProvider{client: genai.NewClient()}
    // ... 10+ providers supported
    }
}
```

---

# PART 4: SIDE-BY-SIDE COMPARISON

## 4.1 Architecture Comparison

```
┌─────────────────────────────────────┐    ┌─────────────────────────────────────┐
│           CLAUDE CODE               │    │            OPENCODE                 │
├─────────────────────────────────────┤    ├─────────────────────────────────────┤
│                                     │    │                                     │
│  Language: TypeScript/JavaScript    │    │  Language: Go                       │
│  UI: CLI + VS Code Extension        │    │  UI: Bubble Tea TUI                 │
│  Provider: Claude only              │    │  Provider: 10+ (Claude, GPT, etc.)  │
│                                     │    │                                     │
│  ┌───────────────────────────────┐  │    │  ┌───────────────────────────────┐  │
│  │          Agent Loop           │  │    │  │          Agent Loop           │  │
│  │  (managed by Anthropic)       │  │    │  │  (in agent.go - you see it)   │  │
│  └───────────────────────────────┘  │    │  └───────────────────────────────┘  │
│                                     │    │                                     │
│  ┌───────────────────────────────┐  │    │  ┌───────────────────────────────┐  │
│  │  20+ Built-in Tools           │  │    │  │  12+ Built-in Tools           │  │
│  │  + MCP Tools (dynamic)        │  │    │  │  + MCP Tools (dynamic)        │  │
│  │  + Skills (instructions)      │  │    │  │  + Project context (.md)      │  │
│  └───────────────────────────────┘  │    │  └───────────────────────────────┘  │
│                                     │    │                                     │
│  ┌───────────────────────────────┐  │    │  ┌───────────────────────────────┐  │
│  │  Extensibility:               │  │    │  │  Extensibility:               │  │
│  │  - Skills (SKILL.md)          │  │    │  │  - MCP servers                │  │
│  │  - Slash commands             │  │    │  │  - opencode.md context        │  │
│  │  - Hooks (scripts)            │  │    │  │  - Config (.opencode.json)    │  │
│  │  - MCP servers                │  │    │  │                               │  │
│  │  - Plugins                    │  │    │  │                               │  │
│  └───────────────────────────────┘  │    │  └───────────────────────────────┘  │
│                                     │    │                                     │
└─────────────────────────────────────┘    └─────────────────────────────────────┘
```

## 4.2 Tool Comparison

| Tool | Claude Code | OpenCode |
|------|-------------|----------|
| **Read File** | `Read` | `view` |
| **Write File** | `Write` | `write` |
| **Edit File** | `Edit` | `edit` |
| **Shell** | `Bash` | `bash` |
| **Find Files** | `Glob` | `glob` |
| **Search Content** | `Grep` | `grep` |
| **Web Search** | `WebSearch` | ❌ |
| **Web Fetch** | `WebFetch` | `fetch` |
| **Sub-agents** | `Task` | `agent` |
| **Patch** | ❌ | `patch` |
| **LSP** | `LSP` | `diagnostics` |
| **Code Search** | ❌ | `sourcegraph` |
| **Todo Tracking** | `TodoWrite` | ❌ |
| **Plan Mode** | `EnterPlanMode` | ❌ |
| **Notebook Edit** | `NotebookEdit` | ❌ |

## 4.3 Permission Model Comparison

| Aspect | Claude Code | OpenCode |
|--------|-------------|----------|
| **Default** | Ask for dangerous ops | Ask for dangerous ops |
| **Safe Commands** | Pre-approved list | Pre-approved list |
| **Session Approval** | Remember this session | Remember this session |
| **Always Approve** | Via hooks | Via config |
| **Banned Commands** | Configurable | Hardcoded (curl, wget, etc.) |

## 4.4 Extension Comparison

| Extension Type | Claude Code | OpenCode |
|----------------|-------------|----------|
| **Instructions** | Skills (SKILL.md) | opencode.md, .cursorrules |
| **Custom Commands** | Slash commands | ❌ |
| **Event Hooks** | Hooks (PreToolUse, etc.) | ❌ |
| **External Tools** | MCP servers | MCP servers |
| **Plugins** | Full plugin system | ❌ |

---

# PART 5: THE AGENT LOOP EXPLAINED

## 5.1 Pseudocode

```python
def agent_loop(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    while True:
        # 1. Call LLM with message history and available tools
        response = llm.call(
            messages=messages,
            tools=ALL_TOOLS
        )

        # 2. Add assistant response to history
        messages.append(response)

        # 3. Check if LLM wants to use tools
        if response.has_tool_calls:
            tool_results = []

            for tool_call in response.tool_calls:
                # 4. Find the tool
                tool = find_tool(tool_call.name)

                # 5. Execute tool (may require permission)
                result = tool.run(tool_call.parameters)

                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # 6. Add tool results to history
            messages.append({"role": "tool", "content": tool_results})

            # 7. CONTINUE LOOP - LLM will see results
            continue

        # 8. No tool calls = agent is done
        return response.content
```

## 5.2 Real Execution Example

```
User: "Fix the TypeScript errors in src/auth.ts"

┌─ Turn 1 ─────────────────────────────────────────────────────┐
│ Messages: [system_prompt, user_message]                      │
│ LLM Response:                                                │
│   "I'll read the file to see the errors."                   │
│   Tool Call: view(file_path="src/auth.ts")                  │
└──────────────────────────────────────────────────────────────┘
           ↓
           Execute view tool → Returns file contents
           ↓
┌─ Turn 2 ─────────────────────────────────────────────────────┐
│ Messages: [system, user, assistant+tool_call, tool_result]   │
│ LLM Response:                                                │
│   "I see 2 errors. Let me fix the first one."               │
│   Tool Call: edit(                                           │
│     file_path="src/auth.ts",                                │
│     old_string="const user: any = ...",                     │
│     new_string="const user: User = ..."                     │
│   )                                                          │
└──────────────────────────────────────────────────────────────┘
           ↓
           Permission: "Allow edit to src/auth.ts?" [Y]
           Execute edit tool → File modified
           ↓
┌─ Turn 3 ─────────────────────────────────────────────────────┐
│ Messages: [...all previous, assistant+tool_call, tool_result]│
│ LLM Response:                                                │
│   "Fixed the first error. Now fixing the second..."         │
│   Tool Call: edit(...)                                       │
└──────────────────────────────────────────────────────────────┘
           ↓
           Execute edit tool → File modified
           ↓
┌─ Turn 4 ─────────────────────────────────────────────────────┐
│ Messages: [...all previous messages]                         │
│ LLM Response:                                                │
│   "Both TypeScript errors have been fixed."                 │
│   (No tool calls - DONE)                                    │
└──────────────────────────────────────────────────────────────┘
           ↓
           Return final response to user
```

## 5.3 Key Loop Characteristics

### What makes it "agentic"?

1. **Autonomous Decision Making**: LLM decides what tool to use
2. **Iterative**: Keeps going until task is complete
3. **Context-Aware**: Sees results of previous actions
4. **Goal-Oriented**: Focuses on completing user's request

### Why the loop is critical

Without the loop:
```
User: "Fix bug"
LLM: "I would need to read the file first, then edit it."
(No action taken)
```

With the loop:
```
User: "Fix bug"
LLM: reads file → analyzes → edits → verifies → "Fixed!"
(Actions completed automatically)
```

---

# PART 6: TOOLS DEEP DIVE

## 6.1 Tool Definition Format

### Claude Code (JSON Schema)

```json
{
  "name": "edit",
  "description": "Performs exact string replacements in files",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": {
        "type": "string",
        "description": "The absolute path to the file to modify"
      },
      "old_string": {
        "type": "string",
        "description": "The text to replace"
      },
      "new_string": {
        "type": "string",
        "description": "The text to replace it with"
      }
    },
    "required": ["file_path", "old_string", "new_string"]
  }
}
```

### OpenCode (Go struct)

```go
type EditParams struct {
    FilePath  string `json:"file_path" jsonschema:"description=Absolute path to file"`
    OldString string `json:"old_string" jsonschema:"description=Text to replace"`
    NewString string `json:"new_string" jsonschema:"description=Replacement text"`
}

func (e *editTool) Info() ToolInfo {
    return ToolInfo{
        Name: "edit",
        Description: "Replaces text in a file",
        Parameters: schemaOf(EditParams{}),
        Required: []string{"file_path", "old_string", "new_string"},
    }
}
```

## 6.2 Tool Categories

### File Operations

| Tool | Input | Output | Safety |
|------|-------|--------|--------|
| **Read/View** | file_path | File contents with line numbers | Safe |
| **Write** | file_path, content | "File written" | Requires permission |
| **Edit** | file_path, old, new | Diff of changes | Requires permission |
| **Glob** | pattern | List of matching files | Safe |
| **Grep** | pattern, path | Matching lines with line numbers | Safe |

### Shell Operations

| Tool | Input | Output | Safety |
|------|-------|--------|--------|
| **Bash** | command | Command output | Dangerous - needs permission |

### Network Operations

| Tool | Input | Output | Safety |
|------|-------|--------|--------|
| **WebFetch** | url, prompt | Processed page content | Moderate |
| **WebSearch** | query | Search results | Safe |

### Meta Operations

| Tool | Input | Output | Safety |
|------|-------|--------|--------|
| **Task/Agent** | prompt | Sub-agent result | Safe (has own permissions) |
| **TodoWrite** | todos list | Updated task list | Safe |

## 6.3 Tool Execution Best Practices

### Do's

1. **Always read before editing**
   ```
   ✓ Read file → Understand structure → Edit specific part
   ```

2. **Use specific patterns in Edit**
   ```
   ✓ Include 3-5 lines of context to ensure unique match
   ```

3. **Verify after changes**
   ```
   ✓ Edit file → Run tests → Report results
   ```

### Don'ts

1. **Don't guess file contents**
   ```
   ✗ Edit without reading first
   ```

2. **Don't use vague old_string**
   ```
   ✗ old_string: "function("  (too generic)
   ✓ old_string: "function handleAuth(user: User) {"
   ```

3. **Don't batch unrelated edits**
   ```
   ✗ Make 10 changes in one giant edit
   ✓ Make focused, logical changes one at a time
   ```

---

# PART 7: BUILDING YOUR OWN CODING AGENT

## 7.1 Minimal Agent in Python

```python
import anthropic
import json

client = anthropic.Anthropic()

# Define tools
TOOLS = [
    {
        "name": "read_file",
        "description": "Read contents of a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"}
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    }
]

def execute_tool(name: str, params: dict) -> str:
    if name == "read_file":
        with open(params["path"]) as f:
            return f.read()
    elif name == "write_file":
        with open(params["path"], "w") as f:
            f.write(params["content"])
        return "File written successfully"
    return "Unknown tool"

def agent_loop(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        # Call Claude with tools
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system="You are a helpful coding assistant.",
            tools=TOOLS,
            messages=messages
        )

        # Add response to history
        messages.append({"role": "assistant", "content": response.content})

        # Check for tool use
        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})
            continue

        # No tool use = done
        return response.content[0].text

# Run the agent
result = agent_loop("Read main.py and add a docstring to the main function")
print(result)
```

## 7.2 Adding Permission System

```python
def request_permission(tool_name: str, params: dict) -> bool:
    print(f"\n⚠️  Tool: {tool_name}")
    print(f"   Params: {params}")
    response = input("   Allow? [y/N]: ")
    return response.lower() == 'y'

def execute_tool_with_permission(name: str, params: dict) -> str:
    # Safe tools don't need permission
    safe_tools = ["read_file"]

    if name not in safe_tools:
        if not request_permission(name, params):
            return "Permission denied"

    return execute_tool(name, params)
```

## 7.3 Adding Session Persistence

```python
import sqlite3

def init_db():
    conn = sqlite3.connect("agent.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn

def save_message(conn, session_id: str, role: str, content: str):
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, json.dumps(content))
    )
    conn.commit()

def load_session(conn, session_id: str) -> list:
    cursor = conn.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id",
        (session_id,)
    )
    return [{"role": row[0], "content": json.loads(row[1])} for row in cursor]
```

## 7.4 Key Lessons from Claude Code & OpenCode

### 1. Tool Design Principles

- **Atomic operations**: Each tool does ONE thing well
- **Clear descriptions**: Help LLM know WHEN to use each tool
- **Structured output**: Return consistent, parseable responses
- **Error handling**: Return errors as tool results, not exceptions

### 2. Safety Patterns

- **Permission gates**: Block dangerous operations
- **Banned commands**: Prevent network access, data exfiltration
- **Output limits**: Truncate huge outputs to save context
- **Timeouts**: Kill runaway commands

### 3. UX Patterns

- **Streaming**: Show responses in real-time
- **Progress indicators**: Show what agent is doing
- **Resumable sessions**: Don't lose work on crash
- **Cost tracking**: Show token usage

### 4. Architecture Patterns

- **Pub/Sub events**: Decouple components
- **Context cancellation**: Clean shutdown
- **Provider abstraction**: Support multiple LLMs
- **Plugin system**: Allow extensions

---

# SUMMARY

## What You've Learned

1. **Coding agents** are AI systems that loop: ask LLM → execute tools → repeat
2. **Claude Code** is Anthropic's official tool with Skills, MCP, Hooks, and 20+ tools
3. **OpenCode** is an open-source example showing exactly how agents work internally
4. **Tools** are the key capability - they give the LLM ability to act
5. **Permissions** keep the user in control of dangerous operations
6. **The loop** is what makes it "agentic" - autonomous action toward a goal

## Key Takeaways

| Concept | Definition |
|---------|------------|
| **Agent Loop** | while(has_tool_calls) { execute → send_results → continue } |
| **Tool** | Function the LLM can call (read, write, bash, etc.) |
| **Skill** | Instructions that teach Claude HOW to do something |
| **MCP** | Protocol for connecting to external tool servers |
| **Hook** | Script that runs at specific points (PreToolUse, etc.) |
| **Permission** | Gate that blocks dangerous operations until user approves |

## Resources

- **Claude Code Docs**: https://code.claude.com/docs
- **Claude Code GitHub**: https://github.com/anthropics/claude-code
- **OpenCode GitHub**: https://github.com/opencode-ai/opencode (archived)
- **Crush (OpenCode successor)**: https://github.com/charmbracelet/crush
- **MCP Specification**: https://modelcontextprotocol.io
- **Claude Code System Prompts**: https://github.com/Piebald-AI/claude-code-system-prompts

---

# PART 8: SKILLS VS MULTI-AGENT SYSTEMS (Research Findings)

**Source**: "When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail" (Li, 2026) - arXiv:2601.04748v2

## 8.0 What Exactly IS a Skill? (Clarification)

### Formal Definition (from Paper, p.4)

```
Skill = (δ, π, ξ)

δ = Skill Descriptor  → Name + description (for selection)
π = Execution Policy  → Instructions on HOW to perform
ξ = Execution Backend → Tool/code (externalized) OR empty (internalized)
```

### Skill vs Tool vs Agent

| Component | Contains | Example |
|-----------|----------|---------|
| **Tool** | Code only | `read_file(path)` returns file content |
| **Skill** | Instructions + optional tool | "To review code: 1) check security 2) check style..." may call `lint_tool()` |
| **Agent** | LLM + tools + system prompt | Complete worker that can think and act |

### Two Types of Skills

| Type | Backend (ξ) | What It Does |
|------|-------------|--------------|
| **Internalized** | ∅ (empty) | Pure instructions - LLM follows steps mentally |
| **Externalized** | Tool/API | Instructions + calls external tool/code |

### Visual Example

```
┌─────────────────────────────────────────────────────────────┐
│  SKILL: "Insurance Document Extraction"                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Descriptor (δ):                                            │
│    Name: "extract_insurance_doc"                            │
│    Description: "Use when processing insurance claim forms" │
│                                                             │
│  Policy (π) - The Instructions:                             │
│    1. Identify document type (claim form, medical, receipt) │
│    2. If scanned PDF, apply OCR first                       │
│    3. Extract all form fields into structured format        │
│    4. Validate required fields: claim_id, date, amount      │
│    5. Flag any missing or suspicious values                 │
│    6. Return as JSON with confidence scores                 │
│                                                             │
│  Backend (ξ) - Optional Tools:                              │
│    - ocr_tool()      ← Called in step 2                     │
│    - validate_tool() ← Called in step 4                     │
│    OR ∅ if LLM does all steps internally                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Insight: Skill ≠ Tool ≠ Action Group

```
WRONG understanding:
  Skill = Group of tools bundled together

CORRECT understanding:
  Skill = Instructions (policy) that MAY use tools

Think of it like:
  Tool   = A hammer
  Skill  = Instructions: "To hang a picture: 1) measure 2) mark 3) hammer nail"
  Agent  = A worker who reads instructions and uses tools
```

### How Claude Code Implements Skills

Claude Code's SKILL.md files follow this pattern:

```yaml
---
name: pr-review                          # δ - Descriptor
description: Review pull requests        # δ - When to use
---

# Instructions                           # π - Policy

When reviewing a PR:
1. Check for security issues first
2. Look for code style violations
3. Verify test coverage
4. Use the Bash tool to run: npm test   # ξ - May reference tools
```

## 8.1 Key Research Findings

### Single-Agent with Skills (SAS) Benefits

| Metric | Improvement | Source |
|--------|-------------|--------|
| Token Usage | **-54%** | Table 3, p.8 |
| Latency | **-50%** | Table 3, p.8 |
| API Calls | **3-4 → 1** | Table 2, p.7 |
| Accuracy | Same (+0.7% avg) | Table 3, p.8 |

### The Scaling Problem (Tool/Skill Limits)

| # of Skills | Accuracy | Status |
|-------------|----------|--------|
| 5-20 | 95%+ | ✅ Safe |
| 30-50 | 80-90% | ⚠️ Degrading |
| 50-100 | 50-70% | ❌ Phase transition |
| 100-200 | 20-45% | ❌ Failure |

**Key finding**: LLMs have a "cognitive capacity" (κ ≈ 50-100) for skill selection. Beyond this, accuracy drops sharply. (Figure 2, p.12)

### Confusability Matters More Than Count

| Condition | Accuracy at 20 skills |
|-----------|----------------------|
| Unique descriptions | **100%** |
| 1 similar competitor | 70-93% |
| 2 similar competitors | 37-70% |

**Key finding**: Similar tool descriptions cause interference, not just tool count. (Figure 3, p.13)

## 8.2 What "Private Information" ACTUALLY Means

### Common Misconception
❌ "Private info" = Security/encryption/AWS compliance

### Paper's Actual Meaning
✅ "Private info" = **Game theory design** where agents intentionally hide data from each other

### Examples of Private Information (Paper's Definition)

| Scenario | Why Needs Multi-Agent |
|----------|----------------------|
| Negotiation | Buyer hides max price, seller hides min price |
| Poker/Games | Players hide cards from opponents |
| Red vs Blue team | Attacker hides strategy from defender |
| Multi-company | Company A secrets hidden from Company B |

### Why Single-Agent Can't Handle This

```
Multi-Agent:
┌──────────────┐    ┌──────────────┐
│   Agent A    │    │   Agent B    │
│  SECRET_A    │←──→│  SECRET_B    │
│ (hidden)     │    │ (hidden)     │
└──────────────┘    └──────────────┘
     ↓ Pass messages, NOT secrets

Single-Agent:
┌─────────────────────────────────┐
│        One LLM Context          │
│  [SECRET_A, SECRET_B, ...]      │
│  Everything visible!            │
└─────────────────────────────────┘
     ↓ Cannot hide from itself
```

### For Most Use Cases (Including Insurance Claims)

**Private information is NOT a concern** because:
- All data is shared in the pipeline
- No adversarial/competitive scenarios
- AWS security is a SEPARATE concern (encryption, IAM, etc.)

## 8.3 Compilability Rules

### What CAN Be Converted to Single-Agent + Skills

| Architecture | Structure | Compilable |
|--------------|-----------|------------|
| Pipeline | A → B → C | ✅ Yes |
| Router-Workers | Router → Workers → Aggregator | ✅ Yes |
| Iterative Refinement | Writer ↔ Critic (loop) | ✅ Yes |

### What CANNOT Be Converted

| Architecture | Structure | Compilable | Reason |
|--------------|-----------|------------|--------|
| Debate/Adversarial | Proponent ↔ Opponent | ❌ No | Needs opposing views |
| Parallel Sampling | Independent agents, best-of-n | ❌ No | Needs independent votes |
| Private Information | Agents with hidden state | ❌ No | Single context sees all |
| Heterogeneous Models | Different LLMs | ❌ No | One model only |

(Table 1, p.7)

## 8.4 Solutions for Scaling

### 1. Hierarchical Routing (Main Solution)

```
BAD (flat):
LLM → pick 1 from 120 tools → 45% accuracy

GOOD (hierarchy):
LLM → pick 1 from 10 categories → 95%
    → pick 1 from 3 tools       → 95%
    = ~85% overall accuracy
```

(Figure 5, p.15)

### 2. Better Skill Descriptions

```
BAD (confusable):
- "Calculate Sum"
- "Compute Total"      ← Too similar!
- "Sum Numbers"

GOOD (distinct):
- "Add numbers and return total"
- "Compute arithmetic mean (average)"
- "Find maximum value in list"
```

### 3. Design Guidelines (from Paper, p.15)

1. **Monitor library size** - Keep below κ ≈ 50-100
2. **Minimize confusability** - Use distinct descriptions
3. **Adopt hierarchy at scale** - Each stage < κ options
4. **Invest in descriptors** - Clear, unique skill names
5. **Match model to task** - Stronger models have higher κ
6. **Consider multi-agent** - When skills exceed threshold

## 8.5 Hybrid Architecture: Multi-Agent with Skills

**Yes, you can combine both!** Each sub-agent can have its own skill library.

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                        │
│                    (routes to sub-agents)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ↓                ↓                ↓
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  DOCUMENT AGENT │ │   POLICY AGENT  │ │  DECISION AGENT │
│                 │ │                 │ │                 │
│  Skills:        │ │  Skills:        │ │  Skills:        │
│  - extract_form │ │  - search_policy│ │  - calc_payout  │
│  - ocr_pdf      │ │  - check_limit  │ │  - gen_approval │
│  - parse_table  │ │  - verify_elig  │ │  - gen_denial   │
│  (5-10 skills)  │ │  (5-10 skills)  │ │  (5-10 skills)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Benefits of This Hybrid

| Aspect | Benefit |
|--------|---------|
| **Each agent** | Has <20 skills = high accuracy |
| **Specialization** | Each agent expert in domain |
| **Scalability** | Add more agents, not more skills |
| **Isolation** | Agent failures don't cascade |
| **Parallel** | Agents can run concurrently |

### When to Use Hybrid vs Pure Approaches

| Situation | Best Approach |
|-----------|---------------|
| <30 total tools | Single-agent + skills |
| 30-100 tools | Single-agent + hierarchy |
| >100 tools | Multi-agent, each with skills |
| Need debate/verification | Multi-agent |
| Need parallel voting | Multi-agent |
| Different models needed | Multi-agent |

## 8.6 Quick Reference: Skills vs Multi-Agent

| | **Single-Agent + Skills** | **Multi-Agent** |
|---|---|---|
| **Speed** | ✅ 50% faster | ❌ Slow |
| **Cost** | ✅ 54% less tokens | ❌ Expensive |
| **API Calls** | ✅ 1 | ❌ 3-4+ |
| **Max Tools (flat)** | ❌ ~50-100 | ✅ Unlimited |
| **Similar Tools** | ❌ Gets confused | ✅ Better |
| **Debate/Voting** | ❌ Cannot | ✅ Can |
| **Private Info** | ❌ Cannot | ✅ Can |
| **Different Models** | ❌ Cannot | ✅ Can |

---

**Document Version**: 1.1
**Last Updated**: January 2026
**Purpose**: Educational guide for understanding AI coding agents
