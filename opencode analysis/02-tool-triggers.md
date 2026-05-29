# Tool Triggers - When Does AI Use Each Tool?

## Overview

The AI doesn't randomly pick tools. **The system prompt tells it exactly when to use each tool.** This document explains the triggers (decision points) that make the AI choose Glob, Grep, Read, Bash, Edit, etc.

## The Decision Tree

```
User makes a request
    ↓
AI reads system prompt rules
    ↓
AI matches request to tool trigger
    ↓
AI uses appropriate tool
```

## Tool Categories

### 🔍 Search Tools
- **Glob** - Find files by name pattern
- **Grep** - Search file contents
- **Codesearch** - Code-specific searching

### 📖 Read Tools
- **Read** - View file contents

### ✏️ Modification Tools
- **Edit** - Change existing files
- **Write** - Create new files
- **Multiedit** - Change multiple files at once

### ⚙️ Execution Tools
- **Bash** - Run shell commands

### 🤔 Interaction Tools
- **Question** - Ask user for input
- **WebSearch** - Search Google
- **WebFetch** - Get web page content

### 📋 Task Management
- **TodoRead** / **TodoWrite** - Track progress
- **Task** - Launch specialized agents

---

## Detailed Tool Triggers

## 1. GLOB Tool

**Purpose:** Find files by name pattern

### When AI Uses Glob

| **Trigger** | **Example User Request** | **Why Glob?** |
|-------------|-------------------------|---------------|
| Finding files by name | "Find all .tsx files" | Pattern matching |
| Finding files by extension | "Show me all JavaScript files" | `**/*.js` pattern |
| Finding files in directory | "What's in the src folder?" | `src/**/*` pattern |
| Finding specific filename | "Find package.json" | `**/package.json` |

### Prompt Instructions for Glob

From the system prompt:
```
Use Glob tool when you need to find files by name patterns:
- Supports patterns like "*.js", "**/*.tsx", "src/**/test*.ts"
- Returns up to 100 files, sorted by modification time
- Use instead of 'ls' or 'find' commands
- Fast and efficient for file discovery
```

### Real Examples

**Example 1:**
```
User: "Find all TypeScript files in the src directory"

AI thinking:
- Need to find files (trigger: Glob)
- Pattern: TypeScript files = *.ts
- Location: src directory = src/**/*.ts

AI action: Glob("src/**/*.ts")
```

**Example 2:**
```
User: "What test files do we have?"

AI thinking:
- Need to find files (trigger: Glob)
- Pattern: test files = *test*.ts or *.test.ts or test/**/*

AI action: Glob("**/*test*.ts")
```

### When NOT to use Glob

❌ **Don't use for searching file contents** (use Grep instead)
```
User: "Find where the login function is defined"
Wrong: Glob("**/login*")  # This finds files NAMED "login"
Right: Grep(pattern="function login")  # This searches INSIDE files
```

---

## 2. GREP Tool

**Purpose:** Search inside files for code/text

### When AI Uses Grep

| **Trigger** | **Example User Request** | **Why Grep?** |
|-------------|-------------------------|---------------|
| Finding where something is defined | "Where is loginUser defined?" | Searches code content |
| Finding usage of function/variable | "Where is API_KEY used?" | Full codebase search |
| Finding patterns in code | "Find all TODO comments" | Regex pattern matching |
| Finding imports | "Where do we import React?" | Content search |

### Prompt Instructions for Grep

```
Use Grep for searching file contents:
- Supports full regex patterns
- Three output modes:
  * files_with_matches: just show which files match
  * content: show the actual matching lines
  * count: show how many matches per file
- Can filter by file type or glob pattern
- Shows context lines with -A/-B/-C flags
```

### Real Examples

**Example 1: Find function definition**
```
User: "Where is the calculateTotal function defined?"

AI thinking:
- Need to search file contents (trigger: Grep)
- Looking for: function definition
- Pattern: "function calculateTotal" or "calculateTotal.*="

AI action:
Grep(
  pattern="function calculateTotal",
  output_mode="files_with_matches"
)

Result: "Found in src/utils/math.ts"
```

**Example 2: Find all TODOs**
```
User: "Show me all TODO comments"

AI thinking:
- Search inside files (trigger: Grep)
- Want to see the actual comments (not just filenames)
- Pattern: TODO:

AI action:
Grep(
  pattern="TODO:",
  output_mode="content"
)

Result shows:
src/app.ts:45: // TODO: Add error handling
src/api.ts:120: // TODO: Implement retry logic
```

**Example 3: Case-insensitive search**
```
User: "Find where we use 'api' (any case)"

AI action:
Grep(
  pattern="api",
  output_mode="content",
  -i=true  # case insensitive
)
```

### Advanced Grep Usage

**With context lines:**
```typescript
Grep(
  pattern="export.*login",
  output_mode="content",
  -A=3,  // Show 3 lines after match
  -B=2   // Show 2 lines before match
)
```

**With file filtering:**
```typescript
Grep(
  pattern="useState",
  glob="*.tsx",  // Only search .tsx files
  output_mode="content"
)
```

---

## 3. READ Tool

**Purpose:** View file contents

### When AI Uses Read

| **Trigger** | **Example User Request** | **Why Read?** |
|-------------|-------------------------|---------------|
| User asks to see a file | "Show me app.ts" | Direct file viewing |
| Before editing | AI needs to edit file | MUST read first (prompt rule) |
| Understanding code | "What does this file do?" | Read to analyze |
| Debugging | "Why is this failing?" | Read to find issues |

### Prompt Instructions for Read

```
CRITICAL RULE: ALWAYS read a file before editing it!

Read tool parameters:
- file_path: Required, absolute path
- offset: Optional, which line to start from
- limit: Optional, how many lines to read (default: 2000)

For large files:
1. Read first 2000 lines
2. If needed, read more with offset parameter
```

### Real Examples

**Example 1: Simple read**
```
User: "Show me package.json"

AI action: Read("package.json")
```

**Example 2: Must read before editing**
```
User: "Fix the bug in login.ts"

AI must do:
Step 1: Read("src/login.ts")  ✅ REQUIRED by prompt
Step 2: Analyze the code
Step 3: Edit("src/login.ts", old_string, new_string)

If AI tries to skip reading:
System ERROR: "You must read a file before editing!"
```

**Example 3: Large file handling**
```
AI reads log file (10,000 lines):

AI action 1: Read("app.log")  # Gets first 2000 lines
AI sees: "Showing lines 1-2000 of 10,000"

If AI needs more:
AI action 2: Read("app.log", offset=2000, limit=2000)  # Lines 2000-4000
```

---

## 4. EDIT Tool

**Purpose:** Modify existing files

### When AI Uses Edit

| **Trigger** | **Example User Request** | **Why Edit?** |
|-------------|-------------------------|---------------|
| Fix a bug | "Fix the error in app.ts" | Modify existing code |
| Update code | "Change the port to 3000" | Replace specific text |
| Refactor | "Rename variable to userList" | String replacement |

### Prompt Instructions for Edit

```
Edit tool rules:
1. MUST read file first (NEVER edit without reading)
2. old_string must be EXACT match
3. new_string must be different from old_string
4. If old_string appears multiple times, edit fails
5. Use replace_all=true to replace all occurrences

NEVER guess file contents - always read first!
```

### Real Examples

**Example 1: Simple edit**
```
User: "Change the port from 3000 to 8080 in server.ts"

AI workflow:
Step 1: Read("src/server.ts")
Step 2: Find the line: `const PORT = 3000`
Step 3: Edit(
  file_path="src/server.ts",
  old_string="const PORT = 3000",
  new_string="const PORT = 8080"
)
```

**Example 2: Rename variable everywhere**
```
User: "Rename 'users' to 'userList' in app.ts"

AI workflow:
Step 1: Read("app.ts")
Step 2: Edit(
  file_path="app.ts",
  old_string="users",
  new_string="userList",
  replace_all=true  # Replace ALL occurrences
)
```

**Example 3: Multi-line edit**
```
AI can edit multiple lines at once:

Edit(
  file_path="config.ts",
  old_string=`export const config = {
  port: 3000,
  host: 'localhost'
}`,
  new_string=`export const config = {
  port: 8080,
  host: '0.0.0.0',
  debug: true
}`
)
```

---

## 5. WRITE Tool

**Purpose:** Create new files

### When AI Uses Write

| **Trigger** | **Example User Request** | **Why Write?** |
|-------------|-------------------------|---------------|
| Create new file | "Create a new utils.ts file" | File doesn't exist |
| Generate code | "Generate a React component" | New file needed |
| Create config | "Create .env file" | Configuration setup |

### Prompt Instructions

```
Write tool:
- Creates new files or overwrites existing
- If file exists, you MUST read it first
- Prefer Edit over Write for existing files
- Use Write only when truly creating new files
```

### Real Example

```
User: "Create a new component Button.tsx"

AI workflow:
Step 1: Check if exists (Glob or Read)
Step 2: Write(
  file_path="src/components/Button.tsx",
  content=`import React from 'react';

export const Button = () => {
  return <button>Click me</button>
};`
)
```

---

## 6. BASH Tool

**Purpose:** Run shell commands

### When AI Uses Bash

| **Trigger** | **Example User Request** | **Why Bash?** |
|-------------|-------------------------|---------------|
| Install packages | "Install express" | `npm install express` |
| Run tests | "Run the tests" | `npm test` |
| Git operations | "Commit changes" | `git add, git commit` |
| Build project | "Build the app" | `npm run build` |
| Check status | "What's git status?" | `git status` |

### Prompt Instructions

```
Bash tool:
- Use for actual shell commands (git, npm, docker, etc.)
- DON'T use for file operations (use Read/Edit/Write instead)
- DON'T use for searching (use Glob/Grep instead)
- Requires permissions (user may need to approve)
- Can run in background with run_in_background=true
```

### Real Examples

**Example 1: Install package**
```
User: "Install axios"

AI action: Bash("npm install axios")
```

**Example 2: Git commit**
```
User: "Commit the changes"

AI workflow:
Step 1: Bash("git status")
Step 2: Bash("git add .")
Step 3: Bash('git commit -m "Update feature"')
```

**Example 3: Run tests**
```
User: "Run tests"

AI action: Bash("npm test")
```

### When NOT to use Bash

❌ **Don't use bash for file operations:**
```
Wrong: Bash("cat app.ts")
Right: Read("app.ts")

Wrong: Bash("find . -name '*.ts'")
Right: Glob("**/*.ts")

Wrong: Bash("grep 'function' *.ts")
Right: Grep(pattern="function")
```

---

## 7. TASK Tool (Launching Agents)

**Purpose:** Delegate work to specialized agents

### When AI Uses Task

| **Trigger** | **Example User Request** | **Why Task?** |
|-------------|-------------------------|---------------|
| Complex exploration | "How does auth work?" | Use explore agent |
| Multi-step research | "Find all API endpoints" | Use general agent |
| Deep investigation | "Understand the codebase" | Use explore agent |

### Prompt Instructions

```
Use Task tool for:
- Complex multi-step searches
- Deep codebase exploration
- When single Glob/Grep isn't enough
- Parallel task execution

Available agents:
- explore: Fast codebase exploration
- general: Multi-step tasks
- plan: Planning mode
```

### Real Example

```
User: "Explain how authentication works in this project"

AI thinking:
- This is complex, needs multiple searches
- Should use explore agent

AI action:
Task(
  subagent_type="explore",
  prompt="Find and explain how authentication works, including:
  - Auth middleware
  - Token handling
  - User session management",
  description="Explore authentication system"
)
```

---

## 8. TODO Tools

**Purpose:** Track progress on multi-step tasks

### When AI Uses TodoWrite

| **Trigger** | **Example User Request** | **Why TodoWrite?** |
|-------------|-------------------------|---------------|
| Complex task | "Add login feature" | Multiple steps to track |
| Multiple changes | "Refactor the API" | Keep user informed |
| Long process | "Set up the project" | Show progress |

### Prompt Instructions

```
Use TodoWrite to:
1. Plan complex tasks (3+ steps)
2. Track progress
3. Keep user informed
4. Mark tasks as: pending, in_progress, completed

Update todos in real-time:
- Mark in_progress when starting
- Mark completed immediately when done
- Only ONE task in_progress at a time
```

### Real Example

```
User: "Add a new feature for user profiles"

AI action 1: TodoWrite([
  {content: "Create User profile component", status: "pending"},
  {content: "Add profile API endpoint", status: "pending"},
  {content: "Update database schema", status: "pending"},
  {content: "Write tests", status: "pending"}
])

AI action 2: TodoWrite([
  {content: "Create User profile component", status: "in_progress"},
  {content: "Add profile API endpoint", status: "pending"},
  ...
])

# After completing first task
AI action 3: TodoWrite([
  {content: "Create User profile component", status: "completed"},
  {content: "Add profile API endpoint", status: "in_progress"},
  ...
])
```

---

## 9. QUESTION Tool

**Purpose:** Ask user for clarification

### When AI Uses Question

| **Trigger** | **Example Situation** | **Why Question?** |
|-------------|----------------------|-------------------|
| Ambiguous request | "Make it better" | Need specifics |
| Multiple options | "Add styling" | Which approach? |
| Important decision | "Refactor auth" | User should choose |

### Real Example

```
User: "Add a database to the project"

AI thinking:
- Multiple database options exist
- Should ask user to choose

AI action: Question({
  questions: [{
    question: "Which database would you like to use?",
    header: "Database",
    options: [
      {label: "PostgreSQL", description: "Production-ready SQL database"},
      {label: "MongoDB", description: "NoSQL document database"},
      {label: "SQLite", description: "Lightweight file-based database"}
    ]
  }]
})
```

---

## Decision Flow Chart

```
User Request: "Find and fix the bug in login.ts"
    ↓
┌─────────────────────────────────────┐
│ AI reads system prompt              │
│ Matches request to triggers         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 1: Need to see the file        │
│ Trigger: "Before editing, read"     │
│ Tool: Read("src/login.ts")          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 2: Found the bug               │
│ Trigger: "Fix bug" = modify file    │
│ Tool: Edit(file, old_string, new)   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ Step 3: Verify fix works            │
│ Trigger: "Run tests" = bash command │
│ Tool: Bash("npm test")              │
└─────────────────────────────────────┘
```

## Summary: Quick Reference

| **Need to...** | **Use Tool** | **Trigger Keyword** |
|----------------|--------------|---------------------|
| Find files by name | Glob | "find files", "show me files", "what .js files" |
| Search file contents | Grep | "where is defined", "find usage", "search for" |
| View a file | Read | "show me", "what's in", before editing |
| Change existing file | Edit | "fix", "update", "change", "modify" |
| Create new file | Write | "create", "generate new" |
| Run command | Bash | "install", "run", "test", "commit" |
| Complex search | Task | "how does X work", "explain", "investigate" |
| Track progress | TodoWrite | multi-step tasks |
| Ask user | Question | ambiguous requests, important choices |

## Key Principle

**The AI doesn't randomly choose tools. Every decision is based on:**
1. **Prompt instructions** (the rules)
2. **User request analysis** (matching triggers)
3. **Context** (what's been done already)

Read [03-task-breakdown.md](03-task-breakdown.md) to see how complex requests are broken into steps!
