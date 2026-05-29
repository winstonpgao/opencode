# Agent System - Different AI Personalities for Different Jobs

## What Are Agents?

Think of agents as **different personalities** or **modes** the AI can switch between, each with different skills and permissions.

**Real-world analogy:**
- **Police officer** - Can enforce laws, carry weapons, arrest people
- **Librarian** - Can read books, organize, help research (but can't arrest anyone!)
- **Construction worker** - Can build, demolish, modify structures
- **Inspector** - Can only look and report (can't modify anything)

In OpenCode, agents work the same way!

## Built-in Agents

OpenCode has **6 built-in agents**, defined in [`packages/opencode/src/agent/agent.ts`](../packages/opencode/src/agent/agent.ts):

### 1. BUILD Agent (Default)
**Role:** Main coding assistant - can do everything

**ACTUAL CODE from `packages/opencode/src/agent/agent.ts` lines 73-86:**

```typescript
build: {
  name: "build",
  options: {},
  permission: PermissionNext.merge(
    defaults,
    PermissionNext.fromConfig({
      question: "allow",
      plan_enter: "allow",
    }),
    user,
  ),
  mode: "primary",
  native: true,
},
```

**When it's used:**
- Default agent when you start OpenCode
- General coding tasks
- Full access to modify files and run commands

**Example:**
```
User: "Fix the bug in app.ts"
→ BUILD agent reads, edits, tests the file
```

---

### 2. PLAN Agent
**Role:** Read-only exploration and planning

**ACTUAL CODE from `packages/opencode/src/agent/agent.ts` lines 87-108:**

```typescript
plan: {
  name: "plan",
  options: {},
  permission: PermissionNext.merge(
    defaults,
    PermissionNext.fromConfig({
      question: "allow",
      plan_exit: "allow",
      external_directory: {
        [path.join(Global.Path.data, "plans", "*")]: "allow",
      },
      edit: {
        "*": "deny",
        [path.join(".opencode", "plans", "*.md")]: "allow",
        [path.relative(Instance.worktree, path.join(Global.Path.data, path.join("plans", "*.md")))]: "allow",
      },
    }),
    user,
  ),
  mode: "primary",
  native: true,
},
```

**When it's used:**
- When you invoke `/plan` or use `EnterPlanMode` tool
- For exploring codebase before making changes
- To create implementation plans

**Example:**
```
User: "Help me plan how to add authentication"
→ PLAN agent explores code, creates detailed plan
→ Can't actually make changes (read-only)
→ User approves plan, then BUILD agent implements it
```

**Special Plan Prompt:**
```
You are in planning mode.

Your job:
1. Thoroughly explore the codebase
2. Understand existing architecture
3. Design an implementation approach
4. Create step-by-step plan
5. Ask questions if unclear
6. Present plan for user approval

You CANNOT edit files in this mode!
Only explore and plan.
```

---

### 3. EXPLORE Agent (Subagent)
**Role:** Fast codebase exploration specialist

**ACTUAL CODE from `packages/opencode/src/agent/agent.ts` lines 124-150:**

```typescript
explore: {
  name: "explore",
  permission: PermissionNext.merge(
    defaults,
    PermissionNext.fromConfig({
      "*": "deny",
      grep: "allow",
      glob: "allow",
      list: "allow",
      bash: "allow",
      webfetch: "allow",
      websearch: "allow",
      codesearch: "allow",
      read: "allow",
      external_directory: {
        [Truncate.DIR]: "allow",
        [Truncate.GLOB]: "allow",
      },
    }),
    user,
  ),
  description: `Fast agent specialized for exploring codebases. Use this when you need to quickly find files by patterns (eg. "src/components/**/*.tsx"), search code for keywords (eg. "API endpoints"), or answer questions about the codebase (eg. "how do API endpoints work?"). When calling this agent, specify the desired thoroughness level: "quick" for basic searches, "medium" for moderate exploration, or "very thorough" for comprehensive analysis across multiple locations and naming conventions.`,
  prompt: PROMPT_EXPLORE,
  options: {},
  mode: "subagent",
  native: true,
},
```

**When it's used:**
- Automatically launched by BUILD agent for complex searches
- When user asks "How does X work?"
- For understanding codebase structure

**Special Explore Prompt:**
```
You are a codebase exploration specialist.

Your task: Quickly find and analyze code.

Strategy:
1. Use Glob to find relevant files
2. Use Grep to search code patterns
3. Read the most relevant files
4. Synthesize findings
5. Report back to parent agent

Be fast and thorough.
Don't use TodoWrite (you're focused on search).
```

**Example:**
```
User: "How does authentication work in this project?"

BUILD agent thinks: "This is complex, I should delegate to EXPLORE"

BUILD agent launches:
Task(
  subagent_type="explore",
  prompt="Find and explain authentication implementation",
  description="Explore auth system"
)

EXPLORE agent:
- Globs for auth files
- Greps for "authenticate", "login", "token"
- Reads relevant files
- Reports findings back to BUILD
```

---

### 4. GENERAL Agent (Subagent)
**Role:** Multi-step task execution

**ACTUAL CODE from `packages/opencode/src/agent/agent.ts` lines 109-123:**

```typescript
general: {
  name: "general",
  description: `General-purpose agent for researching complex questions and executing multi-step tasks. Use this agent to execute multiple units of work in parallel.`,
  permission: PermissionNext.merge(
    defaults,
    PermissionNext.fromConfig({
      todoread: "deny",
      todowrite: "deny",
    }),
    user,
  ),
  options: {},
  mode: "subagent",
  native: true,
},
```

**When it's used:**
- For complex multi-step tasks
- Parallel execution of independent tasks

**Example:**
```
BUILD agent launches GENERAL for complex refactoring:

Task(
  subagent_type="general",
  prompt="Rename 'User' to 'Account' across entire codebase:
  1. Find all files with 'User'
  2. Update imports
  3. Update type definitions
  4. Update component names
  5. Update tests"
)
```

---

### 5. COMPACTION Agent (Hidden)
**Role:** Compress long conversations

**ACTUAL CODE from `packages/opencode/src/agent/agent.ts` lines 151-165:**

```typescript
compaction: {
  name: "compaction",
  mode: "primary",
  native: true,
  hidden: true,
  prompt: PROMPT_COMPACTION,
  permission: PermissionNext.merge(
    defaults,
    PermissionNext.fromConfig({
      "*": "deny",
    }),
    user,
  ),
  options: {},
},
```

**When it's used:**
- Automatically when conversation gets too long
- Summarizes previous messages to save context
- Has "*": "deny" for all permissions - only reads conversation history

---

### 6. TITLE Agent (Hidden)
**Role:** Generate session titles

**ACTUAL CODE from `packages/opencode/src/agent/agent.ts` lines 166-181:**

```typescript
title: {
  name: "title",
  mode: "primary",
  options: {},
  native: true,
  hidden: true,
  temperature: 0.5,
  permission: PermissionNext.merge(
    defaults,
    PermissionNext.fromConfig({
      "*": "deny",
    }),
    user,
  ),
  prompt: PROMPT_TITLE,
},
```

**When it's used:**
- Automatically creates titles like "Fix authentication bug in login.ts"
- Lower temperature (0.5) for consistent, predictable titles

---

## How Agents Are Invoked

### Primary Agents (Direct Use)
```bash
# Use BUILD agent (default)
opencode run "Fix the bug"

# Use PLAN agent
opencode run --agent plan "Plan the new feature"
```

### Subagents (Launched by Other Agents)

BUILD agent can launch subagents using the `Task` tool:

```typescript
// BUILD agent code (simplified)
if (userAsks("How does routing work?")) {
  // Launch EXPLORE subagent
  await Task({
    subagent_type: "explore",
    description: "Explore routing system",
    prompt: "Find and explain how routing works in this codebase"
  })
}
```

---

## Agent Prompts

Each agent can have a **custom system prompt**. Here's how they differ:

### BUILD Agent Prompt (from `anthropic.txt`)
```markdown
You are Claude Code, a coding assistant.

## Your Capabilities
- Read and modify code
- Run commands
- Search files
- Install packages
- Commit changes

## Tools
[Detailed tool descriptions...]

## Rules
1. Read files before editing
2. Use specialized tools (Glob/Grep) over bash
3. Track complex tasks with TodoWrite
4. Test your changes
5. Be professional and accurate

## Workflow
1. Understand the request
2. Explore if needed
3. Plan approach
4. Implement changes
5. Test
6. Report to user
```

### PLAN Agent Prompt
```markdown
You are in PLANNING mode.

Your job: Create implementation plans WITHOUT modifying code.

Process:
1. Explore codebase thoroughly
   - Use Glob to find relevant files
   - Use Grep to understand patterns
   - Read key files

2. Understand architecture
   - What frameworks?
   - What patterns are used?
   - What's the file structure?

3. Design approach
   - Multiple options if applicable
   - Consider trade-offs
   - List dependencies

4. Create plan
   - Step-by-step implementation
   - Files to modify
   - New files to create
   - Potential risks

5. Present to user
   - Use ExitPlanMode when ready
   - User approves or requests changes

CRITICAL: You CANNOT edit files. Read-only mode.
```

### EXPLORE Agent Prompt
```markdown
You are a codebase EXPLORATION specialist.

Mission: Find and analyze code quickly.

Strategy:
1. Start broad
   - Glob for file patterns
   - Get overview of structure

2. Narrow down
   - Grep for specific patterns
   - Find relevant code sections

3. Deep dive
   - Read important files
   - Understand implementation

4. Synthesize
   - Connect the dots
   - Explain how it works

Speed is important:
- Don't read every file
- Focus on most relevant
- Use Grep to confirm hunches

Report findings clearly:
- What you found
- Where it's located (file:line)
- How it works
```

---

## Permission System

Agents have different permission levels:

| Permission | BUILD | PLAN | EXPLORE | GENERAL |
|------------|-------|------|---------|---------|
| read | ✅ Allow | ✅ Allow | ✅ Allow | ✅ Allow |
| edit | ✅ Allow | ❌ Deny | ❌ Deny | ✅ Allow |
| write | ✅ Allow | ❌ Deny | ❌ Deny | ✅ Allow |
| bash | ✅ Allow | ⚠️ Ask | ✅ Allow | ✅ Allow |
| glob | ✅ Allow | ✅ Allow | ✅ Allow | ✅ Allow |
| grep | ✅ Allow | ✅ Allow | ✅ Allow | ✅ Allow |
| question | ✅ Allow | ✅ Allow | ❌ Deny | ❌ Deny |
| todowrite | ✅ Allow | ✅ Allow | ❌ Deny | ❌ Deny |

**Why different permissions?**

- **PLAN**: Can't edit because it's planning mode (prevent accidents)
- **EXPLORE**: No TodoWrite because it's focused on searching
- **GENERAL**: No TodoWrite to avoid confusion (parent agent tracks tasks)

---

## Creating Custom Agents

You can create your own agents in `opencode.jsonc`:

### Example: Code Review Agent

```jsonc
{
  "agent": {
    "code-reviewer": {
      "mode": "subagent",
      "description": "Reviews code for issues and suggests improvements",
      "prompt": "You are a code review expert.\n\nAnalyze code for:\n- Bugs\n- Security issues\n- Performance problems\n- Best practices\n- Code style\n\nProvide specific, actionable feedback.",
      "permission": {
        "read": "allow",
        "glob": "allow",
        "grep": "allow",
        "edit": "deny",  // Can't modify, only review
        "write": "deny"
      },
      "temperature": 0.3,  // Lower temperature for consistent reviews
      "color": "blue"
    }
  }
}
```

**Usage:**
```typescript
// BUILD agent launches custom reviewer
Task({
  subagent_type: "code-reviewer",
  description: "Review authentication code",
  prompt: "Review the auth module for security issues"
})
```

### Example: Documentation Agent

```jsonc
{
  "agent": {
    "doc-writer": {
      "mode": "subagent",
      "description": "Generates documentation",
      "prompt": "You are a documentation specialist.\n\nCreate clear, comprehensive documentation.\n\nInclude:\n- Overview\n- API references\n- Examples\n- Common pitfalls",
      "permission": {
        "read": "allow",
        "write": "allow",  // Can create .md files
        "edit": "allow",
        "glob": "allow"
      },
      "model": {
        "modelID": "claude-opus-4",  // Use Opus for better writing
        "providerID": "anthropic"
      }
    }
  }
}
```

---

## Agent Orchestration

### Example: Complex Task Using Multiple Agents

```
User: "Refactor the user authentication system"

BUILD agent workflow:

Step 1: Launch EXPLORE to understand current system
  Task(explore, "Understand auth system")
  → EXPLORE finds all auth-related files and explains

Step 2: BUILD agent creates plan
  TodoWrite([
    "Update auth middleware",
    "Refactor token handling",
    "Improve error handling",
    "Update tests"
  ])

Step 3: BUILD agent implements changes
  - Reads files
  - Makes edits
  - Runs tests

Step 4: If complex search needed during implementation
  Task(general, "Find all usages of old auth pattern")
  → GENERAL agent searches across codebase

Step 5: BUILD completes and reports
```

---

## Summary

**Key Concepts:**

1. **Agents are specialized modes** - Each has different capabilities
2. **Primary vs Subagent** - Primary can be used directly, subagents are launched
3. **Permissions control access** - What each agent can/can't do
4. **Custom prompts guide behavior** - Each agent has specific instructions
5. **Orchestration** - Agents can launch other agents for specialized tasks

**Default flow:**
```
User → BUILD agent (main)
        ↓
        Launches EXPLORE (for complex searches)
        Launches GENERAL (for multi-step tasks)
        Enters PLAN mode (for planning)
```

**Why this matters:**
- **Safety**: PLAN can't accidentally edit files
- **Efficiency**: EXPLORE is optimized for searching
- **Organization**: Each agent has clear responsibilities

Next: Read [05-system-architecture.md](05-system-architecture.md) to see how all the pieces fit together!
