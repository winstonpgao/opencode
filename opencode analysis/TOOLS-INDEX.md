# Complete Tools Index - All OpenCode Tools

## Overview

OpenCode provides **19 built-in tools** that the AI can use to interact with your codebase, run commands, search the web, and more.

**Location:** `packages/opencode/src/tool/registry.ts`

---

## All Tools Quick Reference

| Tool | Category | Purpose | When AI Uses It |
|------|----------|---------|-----------------|
| **Read** | File | View file contents | Before editing, to understand code |
| **Glob** | Search | Find files by pattern | "find all .ts files" |
| **Grep** | Search | Search file contents | "where is function X defined?" |
| **Edit** | File | Modify existing files | Fix bugs, refactor code |
| **Write** | File | Create new files | Generate new components |
| **Bash** | Execution | Run shell commands | Install packages, run tests, git |
| **Task** | Orchestration | Launch subagents | Complex searches, parallel work |
| **TodoWrite** | Task Mgmt | Update task list | Track multi-step tasks |
| **TodoRead** | Task Mgmt | Read task list | Resume work, check status |
| **Question** | Interaction | Ask user questions | Clarify requirements, get decisions |
| **WebSearch** | Web | Search Google | Find docs, research libraries |
| **WebFetch** | Web | Fetch URL content | Read documentation, API specs |
| **CodeSearch** | Search | Semantic code search | Find code by meaning (powered by Exa) |
| **Skill** | Orchestration | Invoke custom skills | Run user-defined workflows |
| **ApplyPatch** | File | Apply git patches | GPT models use this instead of Edit |
| **LSP** | Advanced | Language Server Protocol | Code intelligence (experimental) |
| **Batch** | Advanced | Batch operations | Multiple tool calls (experimental) |
| **PlanEnter** | Mode | Enter plan mode | Start planning phase |
| **PlanExit** | Mode | Exit plan mode | Finish planning, get approval |

---

## Detailed Tool Documentation

## 1. SEARCH TOOLS

### Glob Tool
**File:** `tool/glob.ts`
**Purpose:** Find files by name pattern

**Parameters:**
```typescript
{
  pattern: string  // e.g., "**/*.ts", "src/**/*.tsx"
  path?: string    // directory to search (optional)
}
```

**Usage Examples:**
```typescript
// Find all TypeScript files
Glob({ pattern: "**/*.ts" })

// Find all test files
Glob({ pattern: "**/*.test.{ts,tsx}" })

// Find package.json
Glob({ pattern: "**/package.json" })

// Find files in specific directory
Glob({ pattern: "*.ts", path: "src/components" })
```

**How It Works:**
- Uses ripgrep for fast pattern matching
- Returns up to 100 results
- Sorted by modification time (newest first)
- Supports glob patterns: `*`, `**`, `?`, `[...]`, `{...}`

**When AI Uses This:**
- User asks "find all X files"
- User asks "what's in this directory"
- Before broad code changes
- To understand project structure

**System Prompt Instruction:**
```
"Use Glob for broad file pattern matching"
```

---

### Grep Tool
**File:** `tool/grep.ts`
**Purpose:** Search file contents with regex

**Parameters:**
```typescript
{
  pattern: string            // regex pattern
  path?: string              // file/directory to search
  glob?: string              // file filter pattern
  type?: string              // file type (js, py, rust, etc.)
  output_mode?: "files_with_matches" | "content" | "count"
  -i?: boolean               // case insensitive
  -A?: number                // lines after match
  -B?: number                // lines before match
  -C?: number                // lines before and after match
  -n?: boolean               // show line numbers (default: true)
  head_limit?: number        // limit output lines
  offset?: number            // skip first N results
  multiline?: boolean        // pattern can span lines
}
```

**Usage Examples:**
```typescript
// Find where function is defined
Grep({
  pattern: "function loginUser",
  output_mode: "files_with_matches"
})

// Show all TODO comments with context
Grep({
  pattern: "TODO:",
  output_mode: "content",
  -A: 2  // show 2 lines after each match
})

// Case-insensitive search
Grep({
  pattern: "api",
  -i: true,
  output_mode: "content"
})

// Search only in TypeScript files
Grep({
  pattern: "useState",
  glob: "*.tsx"
})

// Count matches per file
Grep({
  pattern: "import.*react",
  output_mode: "count"
})
```

**How It Works:**
- Uses ripgrep under the hood
- Full regex support
- Lines truncated at 2000 chars
- Context lines with -A/-B/-C

**When AI Uses This:**
- "where is X defined?"
- "find all usages of Y"
- "show me all TODO comments"
- "search for pattern Z"

**System Prompt Instruction:**
```
"Use Grep for searching file contents with regex"
```

---

### CodeSearch Tool
**File:** `tool/codesearch.ts`
**Purpose:** Semantic code search (understands meaning, not just keywords)

**Powered By:** Exa AI
**Availability:** Only for OpenCode Zen users or with `OPENCODE_ENABLE_EXA=true`

**Parameters:**
```typescript
{
  query: string  // natural language query
}
```

**Usage Examples:**
```typescript
// Find authentication code
CodeSearch({ query: "user authentication and login logic" })

// Find error handling
CodeSearch({ query: "error handling and retry mechanisms" })
```

**How It Works:**
- Semantic search (understands intent)
- Returns relevant code snippets
- Better than keyword search for concepts

**When AI Uses This:**
- Complex conceptual searches
- When keyword search isn't enough
- Understanding architecture

---

## 2. FILE TOOLS

### Read Tool
**File:** `tool/read.ts`
**Purpose:** View file contents

**Parameters:**
```typescript
{
  file_path: string  // absolute path (required)
  offset?: number    // start line (default: 0)
  limit?: number     // max lines (default: 2000)
}
```

**Usage Examples:**
```typescript
// Read entire file (up to 2000 lines)
Read({ file_path: "/project/src/app.ts" })

// Read specific range
Read({
  file_path: "/project/package.json",
  offset: 0,
  limit: 50  // first 50 lines
})

// Read next chunk of large file
Read({
  file_path: "/project/large.log",
  offset: 2000,
  limit: 2000  // lines 2000-4000
})
```

**How It Works:**
- Default limit: 2000 lines
- Lines > 2000 chars are truncated
- Can read: text, images, PDFs, Jupyter notebooks
- Shows line numbers (cat -n format)

**CRITICAL RULE:**
```
"ALWAYS read a file before editing it!"
```

**When AI Uses This:**
- User asks "show me X file"
- Before any edit operation (required!)
- Understanding code structure
- Debugging issues

**System Prompt Instruction:**
```
"CRITICAL RULE: ALWAYS read a file before editing it!
You must NEVER edit without reading first."
```

---

### Edit Tool
**File:** `tool/edit.ts`
**Purpose:** Modify existing files

**Parameters:**
```typescript
{
  file_path: string      // absolute path
  old_string: string     // exact text to replace
  new_string: string     // replacement text
  replace_all?: boolean  // replace all occurrences (default: false)
}
```

**Usage Examples:**
```typescript
// Simple replacement
Edit({
  file_path: "/project/config.ts",
  old_string: "const PORT = 3000",
  new_string: "const PORT = 8080"
})

// Multi-line edit
Edit({
  file_path: "/project/App.tsx",
  old_string: `export default function App() {
  return <div>Hello</div>
}`,
  new_string: `export default function App() {
  return <div>Hello World</div>
}`
})

// Replace all occurrences
Edit({
  file_path: "/project/app.ts",
  old_string: "users",
  new_string: "userList",
  replace_all: true  // rename variable everywhere
})
```

**How It Works:**
- Exact string matching (must be EXACT!)
- If old_string appears multiple times, edit fails (unless replace_all=true)
- LSP integration for smart edits
- Validates file was read first

**CRITICAL RULES:**
```
1. MUST read file first
2. old_string must be EXACT match
3. If ambiguous, edit fails
4. Use replace_all for global changes
```

**When AI Uses This:**
- Fix bugs
- Update code
- Refactor
- Rename variables

**System Prompt Instruction:**
```
"Edit tool rules:
1. MUST read file first (NEVER edit without reading)
2. old_string must be EXACT match
3. new_string must be different from old_string
4. If old_string appears multiple times, edit fails
5. Use replace_all=true to replace all occurrences"
```

---

### Write Tool
**File:** `tool/write.ts`
**Purpose:** Create new files (or overwrite existing)

**Parameters:**
```typescript
{
  file_path: string  // absolute path
  content: string    // file contents
}
```

**Usage Examples:**
```typescript
// Create new component
Write({
  file_path: "/project/src/Button.tsx",
  content: `import React from 'react';

export const Button = () => {
  return <button>Click me</button>;
};`
})

// Create config file
Write({
  file_path: "/project/.env",
  content: `API_KEY=placeholder
DATABASE_URL=postgresql://localhost`
})
```

**How It Works:**
- Creates new file
- If file exists, OVERWRITES completely
- Must read first if file already exists

**CRITICAL RULE:**
```
"If file exists, you MUST read it first before writing"
```

**When AI Uses This:**
- Create new files
- Generate code
- Setup configuration

**System Prompt Instruction:**
```
"Write tool:
- Creates new files or overwrites existing
- If file exists, you MUST read it first
- Prefer Edit over Write for existing files
- Use Write only when truly creating new files"
```

---

### ApplyPatch Tool
**File:** `tool/apply_patch.ts`
**Purpose:** Apply git-style patches (used by GPT models instead of Edit)

**Parameters:**
```typescript
{
  file_path: string  // absolute path
  patch: string      // unified diff format
}
```

**Usage Example:**
```typescript
ApplyPatch({
  file_path: "/project/app.ts",
  patch: `--- a/app.ts
+++ b/app.ts
@@ -1,3 +1,3 @@
-const PORT = 3000
+const PORT = 8080`
})
```

**How It Works:**
- Uses git patch format
- Better for GPT models (they're trained on diffs)
- Anthropic models use Edit instead

**When Used:**
- GPT-4, GPT-4 Turbo models
- Not used by Claude models

---

## 3. EXECUTION TOOLS

### Bash Tool
**File:** `tool/bash.ts`
**Purpose:** Run shell commands

**Parameters:**
```typescript
{
  command: string       // shell command
  description?: string  // what this command does
  timeout?: number      // milliseconds (max: 600000 = 10 min)
  run_in_background?: boolean  // async execution
}
```

**Usage Examples:**
```typescript
// Install package
Bash({
  command: "npm install axios",
  description: "Install axios package"
})

// Run tests
Bash({
  command: "npm test",
  description: "Run test suite",
  timeout: 300000  // 5 minutes
})

// Git operations
Bash({
  command: "git add . && git commit -m 'Fix bug'",
  description: "Stage and commit changes"
})

// Start server (background)
Bash({
  command: "node server.js",
  run_in_background: true,
  description: "Start development server"
})
```

**How It Works:**
- Runs in user's shell environment
- Working directory persists
- Shell state does NOT persist
- Output captured and returned

**CRITICAL RULES:**
```
"Use specialized tools instead of bash when possible:
- Read files: Use Read (NOT cat/head/tail)
- Search files: Use Glob/Grep (NOT find/grep commands)
- Edit files: Use Edit (NOT sed/awk)
- Create files: Use Write (NOT echo >/cat <<EOF)

Reserve Bash for:
- git commands
- npm/package manager
- running tests/builds
- system operations"
```

**Git Safety Rules:**
```
"Git Safety Protocol:
- NEVER update git config
- NEVER run destructive commands unless user explicitly requests
  (push --force, reset --hard, clean -f)
- NEVER skip hooks (--no-verify)
- NEVER force push to main/master
- Create NEW commits (don't amend unless requested)
- Prefer specific file adds over 'git add -A'"
```

**When AI Uses This:**
- Install dependencies
- Run tests
- Build project
- Git operations
- System commands

**System Prompt Instruction:**
```
"Use Bash for shell commands (git, npm, docker, etc.)
DON'T use for file operations (use Read/Edit/Write)
DON'T use for searching (use Glob/Grep)"
```

---

### Task Tool
**File:** `tool/task.ts`
**Purpose:** Launch specialized subagents

**Parameters:**
```typescript
{
  subagent_type: string  // "explore", "general", "plan", or custom
  prompt: string         // task description
  description: string    // short summary (3-5 words)
  model?: "sonnet" | "opus" | "haiku"  // override model
  run_in_background?: boolean
  resume?: string        // resume previous agent by ID
}
```

**Available Subagents:**
- **explore** - Fast codebase exploration (read-only)
- **general** - Multi-step task execution
- **plan** - Planning mode (read-only)
- Custom agents from `opencode.jsonc`

**Usage Examples:**
```typescript
// Launch explore agent
Task({
  subagent_type: "explore",
  description: "Explore auth system",
  prompt: "Find and explain how authentication works in this codebase"
})

// Launch general agent for complex task
Task({
  subagent_type: "general",
  description: "Refactor user module",
  prompt: "Rename 'User' to 'Account' across all files"
})

// Use faster model for simple task
Task({
  subagent_type: "explore",
  description: "Find config files",
  prompt: "List all configuration files",
  model: "haiku"  // faster, cheaper
})

// Run in background
Task({
  subagent_type: "general",
  description: "Run comprehensive tests",
  prompt: "Run all tests and report failures",
  run_in_background: true
})
```

**How It Works:**
- Spawns new agent process
- Agent has its own context
- Returns result to parent agent
- Can run in background

**When AI Uses This:**
- Complex searches (delegates to EXPLORE)
- Multi-step operations (delegates to GENERAL)
- Parallel work
- Planning phase

**System Prompt Instruction:**
```
"When exploring the codebase to gather context or answer a question
that is not a needle query for a specific file/class/function, it is
CRITICAL that you use the Task tool instead of running search commands
directly."
```

---

## 4. TASK MANAGEMENT TOOLS

### TodoWrite Tool
**File:** `tool/todo.ts`
**Purpose:** Create and update task lists

**Parameters:**
```typescript
{
  todos: Array<{
    content: string      // task description (imperative: "Fix bug")
    activeForm: string   // present continuous: "Fixing bug"
    status: "pending" | "in_progress" | "completed"
  }>
}
```

**Usage Example:**
```typescript
TodoWrite({
  todos: [
    {
      content: "Read authentication code",
      activeForm: "Reading authentication code",
      status: "in_progress"
    },
    {
      content: "Fix login bug",
      activeForm: "Fixing login bug",
      status: "pending"
    },
    {
      content: "Run tests",
      activeForm: "Running tests",
      status: "pending"
    }
  ]
})
```

**CRITICAL RULES:**
```
"Task States and Management:
1. Use these states: pending, in_progress, completed
2. Task descriptions must have TWO forms:
   - content: imperative (\"Run tests\")
   - activeForm: present continuous (\"Running tests\")
3. Update task status in real-time
4. Mark completed IMMEDIATELY after finishing
5. Exactly ONE task must be in_progress at any time
6. Complete current tasks before starting new ones
7. Only mark completed when FULLY accomplished"
```

**When AI Uses This:**
- Complex tasks (3+ steps)
- User provides list of tasks
- Multi-step features
- To track progress

**System Prompt Instruction:**
```
"Use TodoWrite for:
- Complex tasks with 3+ steps
- Non-trivial tasks requiring planning
- When user provides multiple tasks

Task tracking:
1. Create task list BEFORE starting work
2. Mark ONE task as in_progress
3. Complete the task
4. Mark it completed IMMEDIATELY
5. Move to next task"
```

---

### TodoRead Tool
**File:** `tool/todo.ts`
**Purpose:** Read current task list

**Parameters:** None

**Usage Example:**
```typescript
TodoRead()
```

**How It Works:**
- Returns current task list from storage
- Shows status of all tasks
- Used to resume work or check status

**When AI Uses This:**
- Resume previous session
- Check what's pending
- Verify progress

---

## 5. INTERACTION TOOLS

### Question Tool
**File:** `tool/question.ts`
**Purpose:** Ask user for input/decisions

**Availability:** Only in app/cli/desktop (not in headless mode)

**Parameters:**
```typescript
{
  questions: Array<{
    question: string     // the question to ask
    header: string       // short label (max 12 chars)
    multiSelect: boolean // allow multiple answers
    options: Array<{
      label: string      // option display text (1-5 words)
      description: string // explanation of option
    }>
  }>
}
```

**Usage Example:**
```typescript
Question({
  questions: [{
    question: "Which database would you like to use?",
    header: "Database",
    multiSelect: false,
    options: [
      {
        label: "PostgreSQL",
        description: "Production-ready SQL database"
      },
      {
        label: "MongoDB",
        description: "NoSQL document database"
      },
      {
        label: "SQLite",
        description: "Lightweight file-based database"
      }
    ]
  }]
})
```

**How It Works:**
- Presents options to user
- User selects answer(s)
- AI continues with user's choice
- User can also provide custom "Other" answer

**When AI Uses This:**
- Ambiguous requests
- Multiple valid approaches
- Important decisions
- Need user preferences

**System Prompt Instruction:**
```
"Use AskUserQuestion tool to ask questions when you need clarification,
want to validate assumptions, or need to make a decision you're unsure
about."
```

---

### WebSearch Tool
**File:** `tool/websearch.ts`
**Purpose:** Search Google

**Availability:** OpenCode Zen users or US region

**Parameters:**
```typescript
{
  query: string              // search query
  allowed_domains?: string[] // whitelist domains
  blocked_domains?: string[] // blacklist domains
}
```

**Usage Examples:**
```typescript
// General search
WebSearch({ query: "React hooks best practices 2026" })

// Search specific sites
WebSearch({
  query: "authentication tutorial",
  allowed_domains: ["reactjs.org", "auth0.com"]
})

// Exclude sites
WebSearch({
  query: "typescript guide",
  blocked_domains: ["w3schools.com"]
})
```

**How It Works:**
- Uses Google search
- Returns search result blocks
- Includes links as markdown
- AI must cite sources in response

**CRITICAL RULE:**
```
"After answering with web search results, you MUST include a
'Sources:' section at the end of your response listing all
relevant URLs as markdown hyperlinks."
```

**When AI Uses This:**
- Research libraries/frameworks
- Find documentation
- Check latest versions
- Learn new technologies

---

### WebFetch Tool
**File:** `tool/webfetch.ts`
**Purpose:** Fetch and read web page content

**Parameters:**
```typescript
{
  url: string    // URL to fetch
  prompt: string // what information to extract
}
```

**Usage Examples:**
```typescript
// Read documentation
WebFetch({
  url: "https://react.dev/reference/react/useState",
  prompt: "Explain how useState hook works with examples"
})

// Read API specs
WebFetch({
  url: "https://api.github.com/",
  prompt: "List available GitHub API endpoints"
})
```

**How It Works:**
- Fetches URL content
- Converts HTML to markdown
- Processes with AI to extract info
- Returns relevant information

**CRITICAL LIMITATION:**
```
"WebFetch WILL FAIL for authenticated or private URLs.
Before using, check if URL requires authentication
(Google Docs, Confluence, Jira, private GitHub repos).
If authenticated, use specialized MCP tool instead."
```

**When AI Uses This:**
- Read documentation
- Fetch API specs
- Research from web
- Follow links from search results

---

## 6. ADVANCED TOOLS

### Skill Tool
**File:** `tool/skill.ts`
**Purpose:** Invoke user-defined custom skills

**Parameters:**
```typescript
{
  skill: string   // skill name
  args?: string   // optional arguments
}
```

**Usage Example:**
```typescript
// Invoke commit skill
Skill({ skill: "commit", args: "-m 'Fix bug'" })

// Invoke custom skill
Skill({ skill: "review-pr", args: "123" })
```

**How Skills Work:**
- Defined in `.claude/skills/` or `.opencode/skills/`
- SKILL.md files with YAML frontmatter
- Custom workflows/automation
- Reusable agent behaviors

**Skill File Format:**
```markdown
---
name: my-skill
description: Does something useful
---

# Instructions for AI
When this skill is invoked:
1. Do X
2. Do Y
3. Do Z
```

**When AI Uses This:**
- User invokes skill by name
- Automated workflows
- Custom project commands

---

### LSP Tool (Experimental)
**File:** `tool/lsp.ts`
**Purpose:** Language Server Protocol integration

**Flag:** `OPENCODE_EXPERIMENTAL_LSP_TOOL=true`

**Purpose:**
- Code intelligence
- Go to definition
- Find references
- Rename symbols
- Code completion

**When Available:**
- Experimental feature
- Requires LSP server installed
- Provides IDE-like capabilities

---

### Batch Tool (Experimental)
**File:** `tool/batch.ts`
**Purpose:** Execute multiple tool calls in a batch

**Flag:** `experimental.batch_tool = true` in config

**Purpose:**
- Batch multiple operations
- Atomic transactions
- All-or-nothing execution

---

### PlanEnter / PlanExit Tools (Experimental)
**Files:** `tool/plan.ts`
**Purpose:** Enter and exit planning mode

**Flag:** `OPENCODE_EXPERIMENTAL_PLAN_MODE=true`

**PlanEnter:**
- Switches to PLAN agent
- Read-only mode
- Exploration and planning

**PlanExit:**
- Exits plan mode
- Returns to BUILD agent
- Requests user approval of plan

---

## Model-Specific Tool Availability

### Claude Models (Anthropic)
```
✅ All standard tools
✅ TodoWrite / TodoRead
✅ Edit / Write (not ApplyPatch)
✅ WebSearch (Zen or enabled)
```

### GPT Models (OpenAI)
```
✅ All standard tools
❌ TodoWrite / TodoRead (omitted for GPT)
✅ ApplyPatch (instead of Edit for newer GPT models)
✅ WebSearch (Zen or enabled)
```

### Gemini Models (Google)
```
✅ All standard tools
✅ TodoWrite / TodoRead
✅ Edit / Write
✅ WebSearch (Zen or enabled)
```

---

## Tool Categories Summary

**Essential (Always Available):**
- Read, Glob, Grep
- Edit (or ApplyPatch), Write
- Bash
- Task

**Task Management (Most Models):**
- TodoWrite, TodoRead
- (Not available for GPT models)

**Web (Zen/Enabled):**
- WebSearch, WebFetch
- CodeSearch

**Orchestration:**
- Task, Skill
- PlanEnter, PlanExit (experimental)

**Advanced (Experimental):**
- LSP, Batch

---

## Custom Tools via Plugins

You can add custom tools:

**Location:** `.opencode/tools/my-tool.ts`

```typescript
export default {
  description: "My custom tool",
  args: {
    input: { type: "string", description: "Input" }
  },
  async execute(args, ctx) {
    // Your tool logic
    return "Result"
  }
}
```

**Auto-registered on startup!**

---

## Next Steps

- **[02-tool-triggers.md](../02-tool-triggers.md)** - When each tool is triggered
- **[Prompts/01-anthropic-prompt.md](../Prompts/01-anthropic-prompt.md)** - How prompts guide tool usage
- **[FlowControl/tool-execution-flow.md](../FlowControl/tool-execution-flow.md)** - Tool execution lifecycle

---

**Total Built-in Tools:** 19
**Custom Tools:** Unlimited (via plugins)
**Tool Registry:** `packages/opencode/src/tool/registry.ts`
