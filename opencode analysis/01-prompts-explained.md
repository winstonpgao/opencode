# What Are Prompts? - Complete Beginner's Guide

## Simple Explanation

Think of prompts like a **job manual** for the AI. Just like you'd give a new employee a handbook that explains their job, prompts tell the AI:

- What their job is
- What tools they can use
- How to use those tools
- When to use each tool
- What NOT to do

## Real-World Analogy

Imagine you're a **chef** (the AI):

**Without a Recipe (No Prompt):**
- You have ingredients but don't know what to make
- You might make something random
- Results are unpredictable

**With a Recipe (With Prompt):**
```
Recipe: "You are an expert Italian chef. Make pasta carbonara.
Tools available: stove, pan, whisk, bowl
Steps:
1. First, boil water for pasta
2. Then, cook bacon in pan
3. Whisk eggs and cheese in bowl
4. Combine everything at the end
Don't: add cream (that's not authentic!)"
```

Now you know exactly what to do!

## How OpenCode Uses Prompts

OpenCode has **different prompts for different AI models**:

### 1. Anthropic Prompt (Claude)
**Location:** `packages/opencode/src/session/prompt/anthropic.txt`

**What it says (simplified):**
```
You are Claude Code, a coding assistant.

Your job:
- Help users with code
- Search files thoroughly
- Use the internet to research
- Always test your work
- Be professional and accurate

Tools you have:
- Read: Look at files
- Edit: Change files
- Bash: Run commands
- Glob: Find files by pattern
- Grep: Search inside files

Rules:
1. ALWAYS read a file before editing it
2. Don't make assumptions - search first
3. Test your changes
4. Be concise but thorough
```

### 2. OpenAI/GPT Prompt (Beast)
**Location:** `packages/opencode/src/session/prompt/beast.txt`

**Key difference:**
- Has "doom loop" detection (stops if AI repeats same action 3 times)
- More structured step-by-step approach
- Different workflow style

### 3. Google Gemini Prompt
**Location:** `packages/opencode/src/session/prompt/gemini.txt`

**Key difference:**
- Optimized for Google's AI
- Different tool calling format

## How Prompts Guide Tool Usage

### Example Prompt Instruction:
```
"When you need to find files:
- Use Glob for pattern matching (*.js, **/*.tsx)
- DON'T use bash 'find' command
- Glob is faster and more reliable"
```

**What this does:**
- ✅ AI will use Glob tool
- ❌ AI won't use bash 'find'
- 🎯 AI knows WHY (faster, more reliable)

### Another Example:
```
"Before editing a file:
1. MUST read it first using Read tool
2. Understand the existing code
3. Then use Edit tool with exact string matching
4. NEVER guess file contents"
```

**What happens:**
```
User: "Fix the bug in app.ts"

AI (following prompt):
Step 1: Read tool → reads app.ts
Step 2: Analyzes the code
Step 3: Edit tool → fixes the bug
Step 4: Responds to user

WITHOUT the prompt:
AI might try to edit without reading → ERROR!
```

## System Prompt Construction

When you use OpenCode, it builds a **mega-prompt** from multiple sources:

### Prompt Building Blocks

```
┌─────────────────────────────────────┐
│  FINAL PROMPT SENT TO AI            │
├─────────────────────────────────────┤
│                                     │
│  1. Provider Header                 │
│     "You are Claude Code..."        │
│                                     │
│  2. Agent Custom Prompt (optional)  │
│     "You are in plan mode..."       │
│                                     │
│  3. Provider-Model Instructions     │
│     "For Claude: use this format"   │
│                                     │
│  4. User Instructions               │
│     Your CLAUDE.md, AGENTS.md       │
│                                     │
│  5. Tool Descriptions               │
│     "Read tool: reads files..."     │
│                                     │
│  6. Environment Info                │
│     "Working dir: /home/project"    │
│     "Platform: Windows"             │
│     "Date: 2026-01-26"              │
│                                     │
└─────────────────────────────────────┘
```

### Example: Real System Prompt

Here's what gets sent to Claude for a simple request:

```markdown
You are Claude Code, Anthropic's official CLI for Claude.

## Your Role
You help users with software engineering tasks.

## Tools Available
1. Read - Read file contents
   - Parameters: file_path, offset (optional), limit (optional)
   - Example: Read("src/app.ts")

2. Glob - Find files by pattern
   - Parameters: pattern
   - Example: Glob("**/*.tsx")

3. Edit - Edit files
   - Parameters: file_path, old_string, new_string
   - MUST read file first!

## Rules
- Professional tone
- Read before editing
- Use Glob/Grep for search (not bash find/grep)
- Test your changes

## User's Custom Instructions (from CLAUDE.md)
[User's preferences loaded here]

## Environment
- Working directory: /home/user/project
- Platform: Windows
- Date: 2026-01-26
```

## How Prompts Control Behavior

### Example 1: File Reading

**Prompt says:**
```
"The Read tool:
- Default: reads first 2000 lines
- Use offset and limit for large files
- Files >50KB are truncated"
```

**AI behavior:**
```python
# Small file (100 lines)
AI uses: Read("config.json")  # Simple

# Large file (10,000 lines)
AI uses: Read("big.log", offset=0, limit=2000)  # First 2000 lines
AI uses: Read("big.log", offset=2000, limit=2000)  # Next 2000 lines
```

### Example 2: Search Strategy

**Prompt says:**
```
"Search strategy:
1. Use Glob for finding files (fast, pattern-based)
2. Use Grep for searching file contents (regex support)
3. DON'T use bash find/grep (permission issues)"
```

**AI behavior:**
```
User: "Find all TypeScript files"
AI: Uses Glob("**/*.ts")  ✅

User: "Find where 'loginUser' function is defined"
AI: Uses Grep(pattern="function loginUser", output_mode="files_with_matches")  ✅

User: "Search for TODO comments"
AI: Uses Grep(pattern="TODO:", output_mode="content")  ✅
```

## Custom Prompts: CLAUDE.md

You can add your own instructions in `.claude/CLAUDE.md`:

```markdown
# My Project Rules

## Code Style
- Use 2 spaces for indentation
- Always use TypeScript
- Prefer functional components in React

## Behavior
- Always run tests after changes
- Ask before making breaking changes
- Commit with conventional commit messages
```

**OpenCode reads this and adds it to the system prompt!**

## Prompts vs Instructions

| **Prompts** | **Instructions** |
|-------------|------------------|
| Built into OpenCode | Your custom rules (CLAUDE.md) |
| Same for all users | Specific to your project |
| Define tool usage | Define preferences |
| Technical guidance | Style/workflow guidance |

## How Prompts Are Loaded

**Code location:** `packages/opencode/src/session/system.ts`

```typescript
// Simplified version
async function buildSystemPrompt(session) {
  const parts = []

  // 1. Load provider-specific prompt
  parts.push(await loadPrompt("anthropic.txt"))

  // 2. Load agent prompt if exists
  if (agent.prompt) {
    parts.push(agent.prompt)
  }

  // 3. Load user instructions
  const userInstructions = await loadInstructions([
    ".claude/CLAUDE.md",
    ".claude/AGENTS.md",
    "~/.opencode/CLAUDE.md"
  ])
  parts.push(userInstructions)

  // 4. Add environment info
  parts.push(`Working directory: ${cwd}`)
  parts.push(`Platform: ${platform}`)
  parts.push(`Date: ${new Date()}`)

  // 5. Combine all parts
  return parts.join("\n\n")
}
```

## Key Takeaways

1. **Prompts are instructions** that guide the AI's behavior
2. **Different AI models** get different prompts (Claude vs GPT vs Gemini)
3. **Prompts control** which tools to use and when
4. **System prompts** are built from multiple sources
5. **You can customize** behavior with CLAUDE.md
6. **Prompts prevent mistakes** by setting rules (like "read before editing")

## Next Steps

Read [02-tool-triggers.md](02-tool-triggers.md) to understand exactly when the AI decides to use each tool (Glob, Grep, Read, Bash, Edit, etc.)!

---

**Remember:** The AI isn't "thinking" on its own - it's following the detailed instructions in these prompts, just like you'd follow a recipe or instruction manual!
