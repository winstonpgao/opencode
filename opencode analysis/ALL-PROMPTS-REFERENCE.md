# All Prompts Quick Reference

## Complete List of System Prompts

This file provides **quick access** to all system prompts used in OpenCode.

---

## Session Prompts (Main Behavior)

### 1. anthropic.txt (106 lines)
**Used by:** Claude Sonnet, Opus, Haiku
**Location:** `packages/opencode/src/session/prompt/anthropic.txt`

**Key Features:**
- Professional, concise tone
- No emojis unless requested
- MUST read before editing
- Prefer editing over creating files
- Use TodoWrite for complex tasks
- Delegate searches to Task tool
- Parallel tool calls for efficiency

**Highlights:**
```
"ALWAYS prefer editing an existing file to creating a new one"
"Use the Task tool instead of running search commands directly"
"Mark todos as completed as soon as you are done with a task"
```

[Full documentation →](01-anthropic-prompt.md)

---

### 2. beast.txt (148 lines)
**Used by:** GPT-4, GPT-4 Turbo, o1, o3, other OpenAI models
**Location:** `packages/opencode/src/session/prompt/beast.txt`

**Key Features:**
- Autonomous iteration (keep going until fully solved)
- **Mandatory** internet research for every task
- 10-step structured workflow
- Casual, friendly communication style
- Memory system (`.github/instructions/memory.instruction.md`)
- Doom loop protection (3-iteration max)

**Highlights:**
```
"THE PROBLEM CAN NOT BE SOLVED WITHOUT EXTENSIVE INTERNET RESEARCH"
"You MUST iterate and keep going until the problem is solved"
"Your knowledge is out of date - use webfetch to verify everything"
```

[Full documentation →](02-beast-prompt.md)

---

### 3. gemini.txt (156 lines)
**Used by:** Google Gemini Pro, Gemini Ultra
**Location:** `packages/opencode/src/session/prompt/gemini.txt`

**Key Features:**
- Extreme focus on following project conventions
- Minimal output (< 3 lines when possible)
- NEVER assume libraries are available
- Verify everything in existing codebase first
- Safety-first approach
- Sparse comments (only "why", not "what")

**Highlights:**
```
"NEVER assume a library/framework is available - verify its established usage"
"Mimic the style, structure, framework choices of existing code"
"Aim for fewer than 3 lines of text output per response"
```

[Full documentation →](03-gemini-prompt.md)

---

## Agent Prompts (Specialized Modes)

### 4. explore.txt (19 lines)
**Used by:** EXPLORE subagent
**Location:** `packages/opencode/src/agent/prompt/explore.txt`

**Key Features:**
- File search specialist
- Fast and thorough
- Read-only (cannot modify files)
- No TodoWrite (focused on search)
- Adapts thoroughness based on request

**Highlights:**
```
"You are a file search specialist"
"Use Glob for broad file pattern matching"
"Use Grep for searching file contents with regex"
"Do not create any files or modify system state"
```

[Full documentation →](04-explore-agent-prompt.md)

---

### 5. plan.txt (27 lines)
**Used by:** PLAN agent (plan mode)
**Location:** `packages/opencode/src/session/prompt/plan.txt`

**Key Features:**
- **ABSOLUTE READ-ONLY** mode
- Cannot edit files (even if user asks!)
- Explores and plans only
- Asks clarifying questions
- Presents plan for user approval
- Overrides all other edit permissions

**Highlights:**
```
"CRITICAL: Plan mode ACTIVE - you are in READ-ONLY phase"
"STRICTLY FORBIDDEN: ANY file edits, modifications, or system changes"
"This ABSOLUTE CONSTRAINT overrides ALL other instructions"
"Any modification attempt is a critical violation. ZERO exceptions"
```

[Full documentation →](05-plan-mode-prompt.md)

---

### 6. compaction.txt (13 lines)
**Used by:** COMPACTION agent (context compression)
**Location:** `packages/opencode/src/agent/prompt/compaction.txt`

**Key Features:**
- Summarizes long conversations
- Preserves important context
- Identifies what needs to be retained
- Enables unlimited conversation length

**Purpose:**
```
"You are a helpful AI assistant tasked with summarizing conversations"
Focus on:
- What was done
- What is currently being worked on
- Which files are being modified
- What needs to be done next
- Key user requests and preferences
- Important technical decisions
```

[Full documentation →](06-compaction-prompt.md)

---

### 7. title.txt (44 lines)
**Used by:** TITLE agent (session naming)
**Location:** `packages/opencode/src/agent/prompt/title.txt`

**Key Features:**
- Generates brief, descriptive session titles
- ≤50 characters
- Focuses on main topic
- No tool names in titles
- Natural, grammatically correct

**Rules:**
```
"You output ONLY a thread title. Nothing else"
"Never include tool names (e.g. 'read tool', 'bash tool')"
"Focus on WHAT the user wants to do WITH the file"
"Always output something meaningful, even if input is minimal"
```

**Examples:**
```
"debug 500 errors in production" → "Debugging production 500 errors"
"implement rate limiting" → "Rate limiting implementation"
"@auth.ts add refresh token support" → "Auth refresh token support"
```

[Full documentation →](07-title-generator-prompt.md)

---

## Special Prompts

### 8. generate.txt (76 lines)
**Used by:** Agent generation system
**Location:** `packages/opencode/src/agent/generate.txt`

**Purpose:** Creates custom agents based on user requirements

**Key Features:**
- Elite AI agent architect persona
- Extracts core intent from user descriptions
- Designs expert personas
- Creates comprehensive system prompts
- Optimizes for performance

**Output Format:**
```json
{
  "identifier": "code-reviewer",
  "whenToUse": "Use this agent when...",
  "systemPrompt": "You are..."
}
```

**Principles:**
```
"Be specific rather than generic"
"Include concrete examples when they clarify behavior"
"Balance comprehensiveness with clarity"
"Build in quality assurance and self-correction mechanisms"
```

[Full documentation →](08-agent-generator-prompt.md)

---

## Prompt Comparison Table

| Feature | Anthropic | Beast (GPT) | Gemini | Explore | Plan |
|---------|-----------|-------------|--------|---------|------|
| **Length** | 106 lines | 148 lines | 156 lines | 19 lines | 27 lines |
| **Tone** | Professional | Casual/Friendly | Minimal | Focused | Planning |
| **Web Research** | Optional | **MANDATORY** | Optional | Allowed | Allowed |
| **Can Edit Files** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ **NEVER** |
| **TodoWrite** | ✅ Emphasized | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Iteration** | Moderate | **Aggressive** | Moderate | Fast | Planning only |
| **File Creation** | Discouraged | Allowed | Discouraged | ❌ No | ❌ No |
| **Verbosity** | Concise | Casual | **< 3 lines** | Results only | Planning docs |
| **Key Strength** | Balanced | Autonomous | Convention-aware | Fast search | Safe planning |

---

## Prompt Stacking Order

When AI runs, prompts are combined in this order:

```
┌─────────────────────────────────────┐
│ 1. Base Prompt (provider-specific) │
│    - anthropic.txt OR               │
│    - beast.txt OR                   │
│    - gemini.txt                     │
├─────────────────────────────────────┤
│ 2. Agent Prompt (if applicable)    │
│    - explore.txt (if EXPLORE mode)  │
│    - plan.txt (if PLAN mode)        │
├─────────────────────────────────────┤
│ 3. User Instructions (optional)    │
│    - .claude/CLAUDE.md              │
│    - .claude/AGENTS.md              │
│    - ~/.opencode/CLAUDE.md          │
├─────────────────────────────────────┤
│ 4. Tool Descriptions (generated)   │
│    - Read tool: reads files...      │
│    - Glob tool: finds files...      │
│    - [all available tools]          │
├─────────────────────────────────────┤
│ 5. Environment Context (generated) │
│    - Working directory: /project    │
│    - Platform: Windows              │
│    - Date: 2026-01-26              │
└─────────────────────────────────────┘
```

**Important:** Later prompts can override earlier ones!
- Example: plan.txt makes mode READ-ONLY even though anthropic.txt allows editing

---

## Customization Layers

### Global Customization
**File:** `~/.opencode/CLAUDE.md`
**Applies to:** All projects

```markdown
# My Global Preferences

## Communication
- Use emojis for progress

## Code Style
- Always use TypeScript
- 2 spaces for indentation
```

### Project-Specific Customization
**File:** `.claude/CLAUDE.md` (in project root)
**Applies to:** Current project only

```markdown
# Project Rules

## Framework
- This is a Next.js project
- Use App Router, not Pages Router

## Testing
- Always run tests after changes
```

---

## When Each Prompt is Used

### anthropic.txt
```
✓ Default for Claude models
✓ User runs: opencode run "task"
✓ Model: claude-sonnet, claude-opus, claude-haiku
✓ No special mode specified
```

### beast.txt
```
✓ Using OpenAI models
✓ Model: gpt-4, gpt-4-turbo, o1, o3
✓ User runs: opencode run --model openai/gpt-4 "task"
```

### gemini.txt
```
✓ Using Google models
✓ Model: gemini-pro, gemini-ultra
✓ User runs: opencode run --model google/gemini-pro "task"
```

### explore.txt
```
✓ BUILD agent launches EXPLORE subagent
✓ User asks: "How does auth work?"
✓ Automatic when complex search needed
```

### plan.txt
```
✓ User enters plan mode
✓ Command: opencode run --agent plan "task"
✓ Or: EnterPlanMode tool called
```

### compaction.txt
```
✓ Conversation gets too long (context full)
✓ Automatic trigger by system
✓ User sees: "Summarizing conversation..."
```

### title.txt
```
✓ New session created
✓ Automatic title generation
✓ Creates: "Debugging auth errors"
```

### generate.txt
```
✓ User creates custom agent
✓ System generates agent config
✓ Command: opencode agent generate "description"
```

---

## Prompt File Locations

```
opencode/packages/opencode/src/

session/prompt/                    ← Main behavior prompts
├── anthropic.txt                  ← Claude (default)
├── anthropic-20250930.txt         ← Version-specific
├── anthropic_spoof.txt            ← Minimal header
├── beast.txt                      ← GPT/OpenAI
├── gemini.txt                     ← Google Gemini
├── qwen.txt                       ← Qwen models
├── copilot-gpt-5.txt             ← GitHub Copilot variant
├── plan.txt                       ← Plan mode overlay
├── plan-reminder-anthropic.txt    ← Plan mode reminder
├── build-switch.txt               ← Build mode switching
├── max-steps.txt                  ← Iteration limit
└── codex_header.txt               ← Provider header

agent/prompt/                      ← Agent-specific prompts
├── explore.txt                    ← EXPLORE agent
├── compaction.txt                 ← Context compression
├── summary.txt                    ← Session summary
└── title.txt                      ← Title generation

agent/
└── generate.txt                   ← Agent generator
```

---

## Loading Code Reference

**File:** `packages/opencode/src/session/system.ts`

```typescript
export async function buildSystemPrompt(
  session: Session.Info,
  agent: Agent.Info,
  model: Provider.Model
): Promise<string[]> {
  const parts: string[] = []

  // 1. Provider-specific base prompt
  if (model.providerID === 'anthropic') {
    parts.push(await readFile('session/prompt/anthropic.txt'))
  } else if (model.providerID === 'openai') {
    parts.push(await readFile('session/prompt/beast.txt'))
  } else if (model.providerID === 'google') {
    parts.push(await readFile('session/prompt/gemini.txt'))
  }

  // 2. Agent-specific prompt
  if (agent.prompt) {
    parts.push(agent.prompt)
  }

  // 3. User instructions
  const userInstructions = await loadInstructions([
    '.claude/CLAUDE.md',
    '.claude/AGENTS.md',
    '~/.opencode/CLAUDE.md'
  ])
  parts.push(...userInstructions)

  // 4. Tool descriptions (auto-generated)
  const toolDescriptions = await generateToolDescriptions()
  parts.push(toolDescriptions)

  // 5. Environment context
  parts.push(`Working directory: ${session.directory}`)
  parts.push(`Platform: ${process.platform}`)
  parts.push(`Date: ${new Date().toISOString()}`)

  return parts
}
```

---

## Quick Links

- [01-anthropic-prompt.md](01-anthropic-prompt.md) - Claude prompt details
- [02-beast-prompt.md](02-beast-prompt.md) - GPT prompt details
- [03-gemini-prompt.md](03-gemini-prompt.md) - Gemini prompt details
- [04-explore-agent-prompt.md](04-explore-agent-prompt.md) - EXPLORE agent
- [05-plan-mode-prompt.md](05-plan-mode-prompt.md) - PLAN mode
- [MASTER-INDEX.md](../MASTER-INDEX.md) - Complete documentation index

---

**Total Prompts:** 8 main prompts + variations
**Customizable:** Yes (via CLAUDE.md)
**Location:** `packages/opencode/src/session/prompt/` and `agent/prompt/`
