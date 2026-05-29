# OpenCode TypeScript Codebase Walkthrough

**Purpose**: Step-by-step explanation of how the CURRENT OpenCode (TypeScript/Bun) works, with beginner-friendly explanations.

**Repository**: https://github.com/anomalyco/opencode
**Your Fork**: https://github.com/winstonpgao/opencode
**Local Copy**: D:/Github/opencode/

---

# IMPORTANT NOTE

This document covers the **NEW TypeScript/Bun version** of OpenCode.

The old document (06_OPENCODE_BEGINNER_WALKTHROUGH.md) describes an **archived Go version** which is different from what's in your repository.

---

# HOW TO READ THIS DOCUMENT

## TypeScript Syntax for Beginners

If you don't know TypeScript, here are the patterns you'll see:

### 1. Function Definition
```typescript
// Regular function
function functionName(param1: Type1, param2: Type2): ReturnType {
    return result
}

// Arrow function (shorter syntax)
const functionName = (param1: Type1) => {
    return result
}

// Async function (can "wait" for things)
async function fetchData(): Promise<Result> {
    const data = await someAsyncOperation()
    return data
}
```

### 2. Namespace (group related code)
```typescript
// Like a folder for related functions
export namespace Tool {
    export function define() { }
    export type Info = { }
}

// Usage:
Tool.define()
```

### 3. Type/Interface (describe shape of data)
```typescript
// What a "User" looks like
interface User {
    name: string
    age: number
    isAdmin?: boolean  // optional (?)
}

// Zod schema (validates data at runtime)
const UserSchema = z.object({
    name: z.string(),
    age: z.number(),
})
```

### 4. Import/Export
```typescript
// Get code from another file
import { Tool } from "./tool/tool"
import type { Agent } from "./agent/agent"  // type-only import

// Make code available to others
export function myFunction() { }
export namespace MyNamespace { }
```

### 5. Promise/Async/Await
```typescript
// Promise = something that will finish later
// async/await = wait for promise to finish

async function example() {
    const result = await fetchData()  // WAITS here
    console.log(result)               // then continues
}
```

---

# TABLE OF CONTENTS

1. [Architecture Overview](#1-architecture-overview)
2. [Entry Point & CLI](#2-entry-point--cli)
3. [The Session System](#3-the-session-system-the-brain)
4. [The Tool System](#4-the-tool-system-the-hands)
5. [The Agent System](#5-the-agent-system-the-personality)
6. [The Provider System](#6-the-provider-system-ai-connection)
7. [The Permission System](#7-the-permission-system-safety)
8. [Supporting Systems](#8-supporting-systems)
9. [Complete Execution Trace](#9-complete-execution-trace)
10. [Key Concepts Summary](#10-key-concepts-summary)

---

# 1. ARCHITECTURE OVERVIEW

## 1.1 Directory Structure

```
packages/opencode/src/
│
├── index.ts              # ENTRY POINT - where everything starts
│
├── cli/                  # Command Line Interface
│   ├── cmd/              # Commands (run, serve, auth, etc.)
│   │   ├── run.ts        # Main command: opencode run "message"
│   │   ├── serve.ts      # Server mode
│   │   └── tui/          # Terminal UI components
│   ├── ui.ts             # UI helpers (colors, formatting)
│   └── bootstrap.ts      # Startup initialization
│
├── session/              # THE BRAIN - conversation management
│   ├── index.ts          # Session state management
│   ├── processor.ts      # THE MAIN LOOP - processes messages
│   ├── llm.ts            # LLM communication
│   ├── message.ts        # Message storage
│   ├── message-v2.ts     # Message types
│   ├── system.ts         # System prompt builder
│   ├── compaction.ts     # Context compression
│   └── summary.ts        # Conversation summaries
│
├── tool/                 # THE HANDS - what AI can do
│   ├── tool.ts           # Tool definition interface
│   ├── registry.ts       # Tool registration
│   ├── read.ts           # Read files
│   ├── write.ts          # Write files
│   ├── edit.ts           # Edit files
│   ├── bash.ts           # Run commands
│   ├── glob.ts           # Find files by name
│   ├── grep.ts           # Search file contents
│   ├── websearch.ts      # Search internet
│   ├── webfetch.ts       # Fetch web pages
│   ├── task.ts           # Spawn sub-agents
│   ├── todo.ts           # Task tracking
│   └── *.txt             # Tool prompts (instructions)
│
├── agent/                # THE PERSONALITY - behavior modes
│   ├── agent.ts          # Agent definitions (build, plan)
│   └── prompt/           # Agent-specific prompts
│
├── provider/             # AI CONNECTION - talks to models
│   ├── provider.ts       # Provider interface
│   └── transform.ts      # Request/response transforms
│
├── permission/           # SAFETY - controls what AI can do
│   └── next.ts           # Permission system
│
├── config/               # Settings
│   └── config.ts         # Configuration loading
│
├── mcp/                  # External tools (Model Context Protocol)
├── lsp/                  # Language servers
├── skill/                # Skills (instruction packages)
├── plugin/               # Plugin system
│
└── (other supporting modules...)
```

## 1.2 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER TYPES COMMAND                          │
│                    $ opencode run "Fix bug"                      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  1. ENTRY POINT (index.ts)                                       │
│     - Parse command line arguments                               │
│     - Route to appropriate command                               │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. RUN COMMAND (cli/cmd/run.ts)                                 │
│     - Initialize session                                         │
│     - Send message to processor                                  │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. SESSION PROCESSOR (session/processor.ts)                     │
│     ┌──────────────────────────────────────────────────────┐    │
│     │              THE MAIN LOOP                            │    │
│     │                                                       │    │
│     │   while (true) {                                      │    │
│     │       1. Send messages to LLM                         │    │
│     │       2. Stream response back                         │    │
│     │       3. If tool call requested:                      │    │
│     │          - Execute tool                               │    │
│     │          - Add result to history                      │    │
│     │          - CONTINUE LOOP                              │    │
│     │       4. If no tool call:                             │    │
│     │          - BREAK (done!)                              │    │
│     │   }                                                   │    │
│     └──────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. TOOL EXECUTION (tool/*.ts)                                   │
│     - Read files, write files, run commands, etc.                │
│     - Results sent back to LLM                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

# 2. ENTRY POINT & CLI

## 2.1 index.ts - Where Everything Starts

**File**: `packages/opencode/src/index.ts`

```typescript
// Uses 'yargs' library for command line parsing
const cli = yargs(hideBin(process.argv))
    .scriptName("opencode")
    .command(RunCommand)      // opencode run "message"
    .command(ServeCommand)    // opencode serve
    .command(AuthCommand)     // opencode auth
    // ... more commands

await cli.parse()
```

**What happens:**
1. User types `opencode run "Fix the bug"`
2. Yargs parses the command line
3. Routes to `RunCommand` handler
4. Handler processes the request

## 2.2 RunCommand - The Main Command

**File**: `packages/opencode/src/cli/cmd/run.ts`

```typescript
export const RunCommand = cmd({
    command: "run [message..]",
    describe: "run opencode with a message",

    handler: async (args) => {
        // 1. Get the message from arguments
        let message = args.message.join(" ")

        // 2. Initialize (load config, connect to server)
        const ctx = await bootstrap({ ... })

        // 3. Create or continue a session
        const session = await Session.create({ ... })

        // 4. Send message and process response
        // This is where the magic happens!
        await Session.chat({
            sessionID: session.id,
            parts: [{ type: "text", text: message }]
        })
    }
})
```

---

# 3. THE SESSION SYSTEM (The Brain)

## 3.1 What is a Session?

A **session** is like a conversation. It tracks:
- Message history (what you said, what AI said)
- Current state (working, waiting, done)
- Tool results (what happened when AI used tools)

## 3.2 Session Processor - THE MAIN LOOP

**File**: `packages/opencode/src/session/processor.ts`

This is the **HEART** of the agent! Here's what it does:

```typescript
export namespace SessionProcessor {
    export function create(input) {
        return {
            async process(streamInput) {
                // THE LOOP
                while (true) {
                    // 1. Call LLM and stream response
                    const stream = await LLM.stream(streamInput)

                    // 2. Process each chunk of the stream
                    for await (const value of stream.fullStream) {
                        switch (value.type) {
                            case "text-delta":
                                // AI is typing text
                                break

                            case "tool-call":
                                // AI wants to use a tool!
                                // Execute it and save result
                                break

                            case "tool-result":
                                // Tool finished, save result
                                break
                        }
                    }

                    // 3. Check if we should continue
                    if (hasMoreToolCalls) {
                        continue  // LOOP AGAIN with new context
                    } else {
                        break     // DONE!
                    }
                }
            }
        }
    }
}
```

## 3.3 Key Insight: Why the Loop Matters

Without the loop:
```
User: "Fix bug in auth.py"
AI: "I would read the file, find the bug, and fix it."
(Nothing actually happens!)
```

With the loop:
```
User: "Fix bug in auth.py"
AI: Uses Read tool → sees file content
AI: Uses Edit tool → fixes the bug
AI: "I fixed the authentication bug by changing X to Y."
(Actual work gets done!)
```

---

# 4. THE TOOL SYSTEM (The Hands)

## 4.1 Tool Definition

**File**: `packages/opencode/src/tool/tool.ts`

Every tool follows this pattern:

```typescript
export namespace Tool {
    export interface Info {
        id: string              // Tool name (e.g., "read")
        init: () => Promise<{
            description: string // What the tool does
            parameters: ZodSchema // What inputs it needs
            execute: Function   // What it actually does
        }>
    }

    // Helper to create tools
    export function define(id, init) {
        return { id, init }
    }
}
```

## 4.2 Example: Read Tool

**File**: `packages/opencode/src/tool/read.ts`

```typescript
export const ReadTool = Tool.define("read", async () => {
    return {
        description: "Read file contents from the filesystem",

        parameters: z.object({
            file_path: z.string().describe("Absolute path to file"),
            offset: z.number().optional().describe("Line to start from"),
            limit: z.number().optional().describe("Number of lines"),
        }),

        async execute(args, ctx) {
            // 1. Read the file
            const content = await Bun.file(args.file_path).text()

            // 2. Apply offset/limit if specified
            const lines = content.split("\n")
            const selected = lines.slice(args.offset, args.limit)

            // 3. Return result
            return {
                title: `Read ${args.file_path}`,
                output: selected.join("\n"),
                metadata: { lines: selected.length }
            }
        }
    }
})
```

## 4.3 Tool Prompts (Instructions for AI)

Each tool has a `.txt` file with instructions for the AI:

**File**: `packages/opencode/src/tool/read.txt`

```
Reads a file from the local filesystem.

Usage:
- The file_path parameter must be an absolute path
- By default, it reads up to 2000 lines
- Results are returned with line numbers

This tool can read:
- Text files
- Images (PNG, JPG) - shown visually
- PDFs - processed page by page
- Jupyter notebooks (.ipynb)
```

## 4.4 All Tools Summary

| Tool | File | Purpose |
|------|------|---------|
| read | read.ts | Read file contents |
| write | write.ts | Create/overwrite files |
| edit | edit.ts | Find and replace in files |
| bash | bash.ts | Execute shell commands |
| glob | glob.ts | Find files by name pattern |
| grep | grep.ts | Search file contents |
| websearch | websearch.ts | Search the internet |
| webfetch | webfetch.ts | Fetch web page content |
| task | task.ts | Spawn sub-agents |
| todo | todo.ts | Track task progress |

---

# 5. THE AGENT SYSTEM (The Personality)

## 5.1 What is an Agent?

An **agent** is a "personality mode" for the AI. Different agents have:
- Different permissions (what tools they can use)
- Different prompts (how they behave)
- Different purposes (build vs explore)

## 5.2 Agent Definitions

**File**: `packages/opencode/src/agent/agent.ts`

```typescript
export namespace Agent {
    // Agent info schema
    export const Info = z.object({
        name: z.string(),
        description: z.string().optional(),
        mode: z.enum(["subagent", "primary", "all"]),
        permission: PermissionRuleset,
        model: z.object({ modelID, providerID }).optional(),
        prompt: z.string().optional(),
        temperature: z.number().optional(),
    })

    // Built-in agents
    const result = {
        build: {
            name: "build",
            permission: { "*": "allow", question: "allow" },
            mode: "primary",
        },
        plan: {
            name: "plan",
            permission: { "*": "allow", edit: "deny", write: "deny" },
            mode: "primary",
        },
        explore: {
            name: "explore",
            permission: { "*": "allow", edit: "deny" },
            mode: "subagent",
        },
    }
}
```

## 5.3 Agent Comparison

| Agent | Purpose | Can Edit? | Can Write? | Mode |
|-------|---------|-----------|------------|------|
| **build** | Full development work | Yes | Yes | Primary |
| **plan** | Planning, exploration | No | No | Primary |
| **explore** | Quick code search | No | No | Subagent |

---

# 6. THE PROVIDER SYSTEM (AI Connection)

## 6.1 What is a Provider?

A **provider** is an AI service (Anthropic, OpenAI, Google, etc.). OpenCode supports multiple providers.

## 6.2 Provider Interface

**File**: `packages/opencode/src/provider/provider.ts`

```typescript
export namespace Provider {
    export interface Model {
        id: string           // e.g., "claude-sonnet-4"
        providerID: string   // e.g., "anthropic"
        name: string         // Display name
        limit: {
            context: number  // Max input tokens
            output: number   // Max output tokens
        }
        capabilities: {
            tool: boolean    // Can use tools?
            image: boolean   // Can see images?
        }
    }

    // Get a model's language interface
    export async function getLanguage(model: Model) {
        switch (model.providerID) {
            case "anthropic":
                return createAnthropic({ apiKey })
            case "openai":
                return createOpenAI({ apiKey })
            case "google":
                return createGoogleAI({ apiKey })
            // ... more providers
        }
    }
}
```

## 6.3 Supported Providers

| Provider | ID | Example Models |
|----------|-----|----------------|
| Anthropic | anthropic | claude-sonnet-4, claude-opus-4 |
| OpenAI | openai | gpt-4, gpt-4o |
| Google | google | gemini-2.0-flash |
| Amazon Bedrock | bedrock | Various |
| Local (Ollama) | ollama | llama, codellama |

---

# 7. THE PERMISSION SYSTEM (Safety)

## 7.1 Why Permissions?

AI can do powerful things. Permissions prevent accidents:
- Don't delete important files
- Don't run dangerous commands
- Ask user before risky operations

## 7.2 Permission Rules

**File**: `packages/opencode/src/permission/next.ts`

```typescript
export namespace PermissionNext {
    // Three permission levels
    type Decision = "allow" | "deny" | "ask"

    // Permission request structure
    export interface Request {
        permission: string      // e.g., "bash", "edit"
        patterns: string[]      // What specifically (e.g., ["rm -rf"])
        sessionID: string
        metadata: any
    }

    // Check if action is allowed
    export async function ask(request: Request): Promise<void> {
        const decision = check(request)

        if (decision === "allow") return
        if (decision === "deny") throw new Error("Permission denied")

        // "ask" - prompt user
        const approved = await promptUser(request)
        if (!approved) throw new Error("User denied permission")
    }
}
```

## 7.3 Default Permissions

```typescript
const defaults = {
    "*": "allow",                    // Most things allowed
    doom_loop: "ask",                // Ask if stuck in loop
    question: "deny",                // Don't ask questions by default
    external_directory: { "*": "ask" }, // Ask for files outside project
    read: {
        "*": "allow",
        "*.env": "ask",              // Ask for .env files
    },
}
```

---

# 8. SUPPORTING SYSTEMS

## 8.1 Complete Directory Reference

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `acp/` | Agent Communication Protocol - remote agent sessions | agent.ts, session.ts, types.ts |
| `auth/` | Authentication handling | index.ts |
| `bun/` | Bun runtime utilities | index.ts |
| `bus/` | Event system (pub/sub for components) | index.ts, bus-event.ts |
| `cli/` | Command Line Interface commands | cmd/*.ts, bootstrap.ts |
| `command/` | Command definitions | - |
| `config/` | Configuration loading & management | config.ts |
| `env/` | Environment variable handling | - |
| `file/` | File operations utilities | - |
| `flag/` | Feature flags | - |
| `format/` | Output formatting utilities | - |
| `global/` | Global state and constants | - |
| `id/` | ID generation utilities | - |
| `ide/` | IDE integration support | - |
| `installation/` | Installation & setup utilities | - |
| `lsp/` | Language Server Protocol (code intelligence) | - |
| `mcp/` | Model Context Protocol (external tools) | - |
| `patch/` | File patching utilities | - |
| `permission/` | Permission system | next.ts |
| `plugin/` | Plugin system for extensions | - |
| `project/` | Project detection & management | - |
| `provider/` | AI provider connections | provider.ts, transform.ts |
| `pty/` | Pseudo-terminal support (interactive shells) | - |
| `question/` | User question/prompting system | - |
| `scheduler/` | Task scheduling and queuing | - |
| `server/` | HTTP server for remote access | - |
| `session/` | Session/conversation management | processor.ts, llm.ts |
| `share/` | Session sharing functionality | - |
| `shell/` | Shell command execution | - |
| `skill/` | Skills (instruction packages) | - |
| `snapshot/` | Save/restore session state | - |
| `storage/` | Persistent data storage (SQLite) | - |
| `tool/` | All tool implementations | read.ts, write.ts, etc. |
| `util/` | General utilities | - |
| `worktree/` | Git worktree management | - |

## 8.2 Event Bus

**File**: `packages/opencode/src/bus/index.ts`

Events allow components to communicate without direct coupling:

```typescript
// Publish an event
Bus.publish("session.created", { sessionID: "123" })

// Subscribe to events
Bus.subscribe("session.created", (data) => {
    console.log("New session:", data.sessionID)
})
```

## 8.3 MCP (Model Context Protocol)

MCP allows external tools to be added:

```typescript
// Add MCP server
opencode mcp add github https://mcp.github.com

// Now AI can use GitHub tools!
```

## 8.4 TUI (Terminal User Interface)

**Directory**: `packages/opencode/src/cli/cmd/tui/`

The TUI provides a rich terminal interface using Ink (React for terminals):

| Subdirectory | Purpose |
|--------------|---------|
| `component/` | UI components (dialogs, prompts, borders) |
| `context/` | React context providers (theme, SDK, keybinds) |
| `context/theme/` | Color themes (dracula, nord, gruvbox, etc.) |

Key components:
- **app.tsx** - Main TUI application
- **dialog-*.tsx** - Modal dialogs (agent, model, session selection)
- **prompt/** - Input prompt with autocomplete and history

## 8.5 Storage System

OpenCode uses SQLite for persistent storage:
- Session history
- Message cache
- Configuration
- Snapshots

## 8.6 Skills System

**Directory**: `packages/opencode/src/skill/`

Skills are reusable instruction packages that teach the AI specific workflows:
- Pre-defined prompts for common tasks
- Can be loaded dynamically
- Extend AI capabilities without code changes

---

# 9. COMPLETE EXECUTION TRACE

Let's trace what happens when you run:
```bash
opencode run "Read main.py and add a docstring"
```

## Step 1: Parse Command
```
index.ts:
  yargs parses "run" command
  Routes to RunCommand.handler
```

## Step 2: Initialize Session
```
cli/cmd/run.ts:
  bootstrap() - load config, connect
  Session.create() - create new session
  Session.chat() - send message
```

## Step 3: Process Message
```
session/processor.ts:
  Create processor
  Enter main loop
```

## Step 4: First LLM Call
```
session/llm.ts:
  Build system prompt
  Send to Claude: "Read main.py and add a docstring"

Claude responds:
  "I'll read the file first"
  Tool call: read(file_path="main.py")
```

## Step 5: Execute Read Tool
```
tool/read.ts:
  Check permission -> allowed
  Read file contents
  Return: "def main():\n    print('hello')\n..."
```

## Step 6: Second LLM Call
```
Claude sees file contents
Claude responds:
  "I see the main function. I'll add a docstring."
  Tool call: edit(file_path="main.py", old="def main():", new="def main():\n    \"\"\"Main entry point.\"\"\"")
```

## Step 7: Execute Edit Tool
```
tool/edit.ts:
  Check permission -> allowed (or ask user)
  Find old string
  Replace with new string
  Save file
  Return: "File edited successfully"
```

## Step 8: Third LLM Call
```
Claude sees edit succeeded
Claude responds:
  "I've added a docstring to the main function."
  (No tool calls)
```

## Step 9: Done!
```
session/processor.ts:
  No more tool calls
  Break from loop
  Return final message to user
```

---

# 10. KEY CONCEPTS SUMMARY

## 10.1 The Agent Loop (Most Important!)

```
┌─────────────────────────────────────────────────┐
│                 THE AGENT LOOP                   │
│                                                  │
│   ┌──────────────────────────────────────────┐  │
│   │  1. User sends message                    │  │
│   └──────────────┬───────────────────────────┘  │
│                  ↓                               │
│   ┌──────────────────────────────────────────┐  │
│   │  2. Send to LLM with tools available      │  │
│   └──────────────┬───────────────────────────┘  │
│                  ↓                               │
│   ┌──────────────────────────────────────────┐  │
│   │  3. LLM responds (text + maybe tool call) │  │
│   └──────────────┬───────────────────────────┘  │
│                  ↓                               │
│          ┌──────┴──────┐                        │
│          ↓             ↓                        │
│   ┌──────────┐   ┌──────────┐                   │
│   │ Tool     │   │ No Tool  │                   │
│   │ Call?    │   │ Call     │                   │
│   └────┬─────┘   └────┬─────┘                   │
│        ↓              ↓                         │
│   ┌──────────┐   ┌──────────┐                   │
│   │ Execute  │   │  DONE!   │                   │
│   │ Tool     │   │  Return  │                   │
│   └────┬─────┘   └──────────┘                   │
│        ↓                                        │
│   ┌──────────────────────────────────────────┐  │
│   │  4. Add result to message history         │  │
│   └──────────────┬───────────────────────────┘  │
│                  ↓                               │
│            LOOP BACK TO STEP 2                  │
│                                                  │
└─────────────────────────────────────────────────┘
```

## 10.2 Key Files to Study

| Priority | File | What to Learn |
|----------|------|---------------|
| 1st | `session/processor.ts` | The main loop |
| 2nd | `tool/tool.ts` | How tools are defined |
| 3rd | `tool/read.ts` | Simple tool example |
| 4th | `agent/agent.ts` | Agent configuration |
| 5th | `permission/next.ts` | Safety system |

## 10.3 Glossary

| Term | Definition |
|------|------------|
| **Session** | A conversation with history |
| **Agent** | Personality mode (build, plan, explore) |
| **Tool** | Function the AI can call |
| **Provider** | AI service (Anthropic, OpenAI, etc.) |
| **LLM** | Large Language Model (the AI brain) |
| **Stream** | Response coming in chunks |
| **Context** | All the information AI can see |
| **Token** | Piece of text (word or part of word) |
| **Permission** | Rule about what AI can do |

---

# APPENDIX: Quick Command Reference

```bash
# Run with a message
opencode run "Fix the bug in auth.py"

# Continue last session
opencode run -c "Now add tests"

# Use specific model
opencode run -m anthropic/claude-sonnet-4 "Explain this code"

# Start server mode
opencode serve --port 4096

# Authenticate
opencode auth login

# Check models
opencode models list
```

---

*Last Updated: January 2026*
*Version: For TypeScript/Bun OpenCode (not the archived Go version)*
