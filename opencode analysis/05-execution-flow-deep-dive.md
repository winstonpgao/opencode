# Execution Flow - Deep Technical Dive

## Complete Code Flow from User Input to Response

**⚠️ IMPORTANT:** This document contains **SIMPLIFIED** code examples for educational purposes. The actual OpenCode implementation in `processor.ts` is significantly more complex with:
- Event-driven stream processing (reasoning-start, reasoning-delta, tool-call, etc.)
- Complex state management for tool calls
- Doom loop detection (3-iteration threshold)
- Permission checking and retry logic
- Context compaction handling

For EXACT implementation details, read the actual source files referenced below.

---

## 📍 Code References

**Main Files:**
- Session processor: `packages/opencode/src/session/processor.ts`
- LLM streaming: `packages/opencode/src/session/llm.ts`
- Tool registry: `packages/opencode/src/tool/registry.ts`
- Tool execution: `packages/opencode/src/tool/tool.ts`
- Agent definitions: `packages/opencode/src/agent/agent.ts`
- Permission system: `packages/opencode/src/permission/next.ts`

---

## 🔄 Complete Execution Flow

### Level 1: High-Level Flow

```
User Input
    ↓
CLI Command Parsing (src/cli/cmd/run.ts)
    ↓
Session Creation/Resume (src/session/index.ts)
    ↓
System Prompt Building (src/session/system.ts)
    ↓
LLM Stream Request (src/session/llm.ts)
    ↓
Tool Call Detection (src/session/processor.ts)
    ↓
Tool Execution Loop (src/tool/tool.ts)
    ↓
Response to User
```

---

## Level 2: Detailed Code Flow

### Step 1: User Input → CLI Processing

**File:** `packages/opencode/src/cli/cmd/run.ts`

```typescript
// User runs: opencode run "Fix the bug in login.ts"

export async function run(args: {
  message?: string
  agent?: string
  model?: string
  session?: string
  file?: string[]
  // ... other options
}) {
  // 1. Parse command line arguments
  const message = args.message || await promptUser()
  const files = args.file || []

  // 2. Get or create session
  const session = args.session
    ? await Session.get(args.session)
    : await Session.create({
        projectID: project.id,
        directory: project.directory,
        title: generateTitle(message)
      })

  // 3. Determine which agent to use
  const agentName = args.agent || config.default_agent || "build"
  const agent = await Agent.get(agentName)

  // 4. Select model (override or default)
  const model = args.model
    ? Provider.parseModel(args.model)
    : await Provider.getDefaultModel()

  // 5. Create user message
  const userMessage: MessageV2.User = {
    role: "user",
    content: [
      { type: "text", text: message },
      ...files.map(f => ({ type: "file", path: f }))
    ]
  }

  // 6. Start processing
  await SessionProcessor.process({
    session,
    agent,
    model,
    message: userMessage
  })
}
```

**Code Location:** [packages/opencode/src/cli/cmd/run.ts](../packages/opencode/src/cli/cmd/run.ts)

---

### Step 2: System Prompt Building

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
    const prompt = await readFile('session/prompt/anthropic.txt')
    parts.push(prompt)
  } else if (model.providerID === 'openai') {
    const prompt = await readFile('session/prompt/beast.txt')
    parts.push(prompt)
  } else if (model.providerID === 'google') {
    const prompt = await readFile('session/prompt/gemini.txt')
    parts.push(prompt)
  }

  // 2. Agent-specific prompt (if exists)
  if (agent.prompt) {
    parts.push(agent.prompt)
  }

  // 3. Load user instructions (CLAUDE.md, AGENTS.md)
  const userInstructions = await loadUserInstructions([
    '.claude/CLAUDE.md',
    '.claude/AGENTS.md',
    '~/.opencode/CLAUDE.md',
    '~/.opencode/AGENTS.md'
  ])
  parts.push(...userInstructions)

  // 4. Add tool descriptions (auto-generated)
  const tools = await ToolRegistry.tools(model, agent)
  const toolDescriptions = tools.map(t => t.description).join('\n\n')
  parts.push(toolDescriptions)

  // 5. Add environment context
  parts.push(`
Working directory: ${session.directory}
Platform: ${process.platform}
Date: ${new Date().toISOString()}
`)

  return parts
}
```

**Code Location:** [packages/opencode/src/session/system.ts](../packages/opencode/src/session/system.ts)

---

### Step 3: LLM Streaming

**File:** `packages/opencode/src/session/llm.ts`

```typescript
export async function stream(input: {
  user: MessageV2.User
  sessionID: string
  model: Provider.Model
  agent: Agent.Info
  system: string[]
  messages: ModelMessage[]
  tools: Record<string, Tool>
  abort: AbortSignal
}): Promise<StreamTextResult> {
  // 1. Build final system prompt
  const systemPrompt = input.system.join('\n\n')

  // 2. Convert tools to model format
  const toolDefinitions = Object.entries(input.tools).map(([name, tool]) => ({
    name,
    description: tool.description,
    parameters: tool.parameters
  }))

  // 3. Call AI provider (via Vercel AI SDK)
  const result = await streamText({
    model: getProviderModel(input.model),
    system: systemPrompt,
    messages: input.messages,
    tools: toolDefinitions,
    maxTokens: 32000,
    temperature: input.agent.temperature || 1.0,
    topP: input.agent.topP || 1.0,
    abortSignal: input.abort
  })

  return result
}
```

**Code Location:** [packages/opencode/src/session/llm.ts](../packages/opencode/src/session/llm.ts)

---

### Step 4: Session Processor (Main Loop)

**File:** `packages/opencode/src/session/processor.ts`

This is the **heart** of the system. Here's the actual code:

```typescript
export class SessionProcessor {
  async process(input: {
    session: Session.Info
    agent: Agent.Info
    model: Provider.Model
    message: MessageV2.User
  }): Promise<void> {
    // 1. Build system prompt
    const system = await buildSystemPrompt(
      input.session,
      input.agent,
      input.model
    )

    // 2. Get conversation history
    const messages = await this.getMessages(input.session)

    // 3. Add user message
    messages.push(input.message)

    // 4. Initialize tools
    const tools = await this.initializeTools(input.agent, input.model)

    // 5. Main processing loop
    let iteration = 0
    const MAX_ITERATIONS = 100

    while (iteration < MAX_ITERATIONS) {
      iteration++

      // 6. Stream LLM response
      const stream = await llm.stream({
        user: input.message,
        sessionID: input.session.id,
        model: input.model,
        agent: input.agent,
        system,
        messages,
        tools,
        abort: this.abortSignal
      })

      // 7. Collect response parts
      const assistantMessage: MessageV2.Assistant = {
        role: "assistant",
        content: []
      }

      // 8. Process stream
      for await (const part of stream.fullStream) {
        if (part.type === 'text-delta') {
          // Text response - display to user
          this.displayText(part.textDelta)
          assistantMessage.content.push({
            type: "text",
            text: part.textDelta
          })
        }

        if (part.type === 'tool-call') {
          // Tool call detected
          assistantMessage.content.push({
            type: "tool_use",
            id: part.toolCallId,
            name: part.toolName,
            input: part.args
          })
        }

        if (part.type === 'reasoning') {
          // Extended thinking (Claude models)
          assistantMessage.content.push({
            type: "reasoning",
            content: part.reasoning
          })
        }
      }

      // 9. Save assistant message
      messages.push(assistantMessage)
      await this.saveMessage(input.session, assistantMessage)

      // 10. Check if tool calls exist
      const toolCalls = assistantMessage.content.filter(
        c => c.type === "tool_use"
      )

      if (toolCalls.length === 0) {
        // No tool calls - we're done!
        break
      }

      // 11. Execute tool calls
      const toolResults = await this.executeToolCalls(
        toolCalls,
        tools,
        input.session,
        input.agent
      )

      // 12. Check for doom loop (same tool called 3+ times)
      if (this.isDoomLoop(messages, toolCalls)) {
        console.warn('Doom loop detected - breaking')
        break
      }

      // 13. Add tool results to conversation
      const toolResultMessage: MessageV2.User = {
        role: "user",
        content: toolResults.map(result => ({
          type: "tool_result",
          tool_use_id: result.id,
          content: result.output
        }))
      }

      messages.push(toolResultMessage)
      await this.saveMessage(input.session, toolResultMessage)

      // 14. Continue loop - send results back to LLM
    }

    // 15. Check if context is full
    if (this.contextNearlyFull(messages)) {
      await this.triggerCompaction(input.session)
    }
  }

  // Doom loop detection
  private isDoomLoop(
    messages: Message[],
    currentToolCalls: ToolCall[]
  ): boolean {
    // Get last 3 tool calls
    const recentTools = messages
      .slice(-6) // Last 3 assistant messages
      .flatMap(m => m.content.filter(c => c.type === "tool_use"))
      .map(t => t.name)

    // Check if same tool called 3 times
    const counts = {}
    for (const tool of recentTools) {
      counts[tool] = (counts[tool] || 0) + 1
      if (counts[tool] >= 3) {
        return true // DOOM LOOP!
      }
    }

    return false
  }
}
```

**Code Location:** [packages/opencode/src/session/processor.ts](../packages/opencode/src/session/processor.ts)

---

### Step 5: Tool Execution

**File:** `packages/opencode/src/tool/tool.ts`

```typescript
export namespace Tool {
  export interface Context {
    sessionID: string
    messageID: string
    agent: string
    abort: AbortSignal
    callID: string

    // Request permission
    ask(request: PermissionRequest): Promise<void>

    // Update metadata (title, progress, etc.)
    metadata(data: { title?: string; metadata?: any }): void
  }

  export interface ExecuteResult {
    title: string
    output: string
    metadata?: any
    attachments?: File[]
  }

  export interface Info {
    id: string
    init(ctx?: InitContext): Promise<{
      description: string
      parameters: z.ZodType
      execute(args: any, ctx: Context): Promise<ExecuteResult>
      formatValidationError?(error: any): string
    }>
  }
}

// Example: Read tool implementation
export const ReadTool: Tool.Info = {
  id: "read",

  async init() {
    return {
      description: `Reads a file from the local filesystem.

Parameters:
- file_path: absolute path to file (required)
- offset: line number to start from (optional)
- limit: number of lines to read (default: 2000)

Usage:
- ALWAYS use absolute paths
- Default reads first 2000 lines
- Lines > 2000 chars are truncated`,

      parameters: z.object({
        file_path: z.string().describe("Absolute path to file"),
        offset: z.number().optional().describe("Start line"),
        limit: z.number().optional().describe("Max lines")
      }),

      async execute(args, ctx) {
        // 1. Check permissions
        await ctx.ask({
          permission: "read",
          patterns: [args.file_path]
        })

        // 2. Read file
        const offset = args.offset || 0
        const limit = args.limit || 2000

        const content = await fs.readFile(args.file_path, 'utf-8')
        const lines = content.split('\n')
        const selectedLines = lines.slice(offset, offset + limit)

        // 3. Format with line numbers (cat -n style)
        const output = selectedLines
          .map((line, i) => `${offset + i + 1}\t${line}`)
          .join('\n')

        // 4. Return result
        return {
          title: `Read ${path.basename(args.file_path)}`,
          output,
          metadata: {
            totalLines: lines.length,
            returnedLines: selectedLines.length,
            truncated: lines.length > (offset + limit)
          }
        }
      }
    }
  }
}
```

**Code Location:** [packages/opencode/src/tool/read.ts](../packages/opencode/src/tool/read.ts)

---

## 🔄 Visual Flow Chart

```
┌─────────────────────────────────────────────────────────────┐
│ USER INPUT                                                   │
│ "Fix the bug in login.ts"                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ CLI PARSING (run.ts)                                        │
│ - Parse arguments                                            │
│ - Determine agent (default: "build")                        │
│ - Determine model (default from config)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ SESSION (index.ts)                                          │
│ - Get or create session                                     │
│ - Load conversation history                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ SYSTEM PROMPT BUILDING (system.ts)                         │
│ 1. Base prompt (anthropic.txt / beast.txt / gemini.txt)    │
│ 2. Agent prompt (if PLAN/EXPLORE mode)                     │
│ 3. User instructions (CLAUDE.md)                           │
│ 4. Tool descriptions (auto-generated)                       │
│ 5. Environment context                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ TOOL REGISTRY (registry.ts)                                │
│ - Initialize all available tools                            │
│ - Filter by agent permissions                               │
│ - Filter by model (GPT uses ApplyPatch, Claude uses Edit)  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ LLM STREAM (llm.ts)                                         │
│ - Call AI provider (Anthropic/OpenAI/Google)               │
│ - Stream response in real-time                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ PROCESSOR LOOP (processor.ts) ◄───────────┐                │
│                                             │                │
│ ┌─────────────────────────────────────┐   │                │
│ │ Collect stream parts:                │   │                │
│ │ - Text deltas                        │   │                │
│ │ - Tool calls                         │   │                │
│ │ - Reasoning (thinking)               │   │                │
│ └─────────────────────────────────────┘   │                │
│                     │                       │                │
│                     ▼                       │                │
│ ┌─────────────────────────────────────┐   │                │
│ │ Any tool calls?                      │   │                │
│ └──────────┬──────────────────────────┘   │                │
│            │                                │                │
│     NO ────┤                                │                │
│            │ YES                            │                │
│            ▼                                │                │
│ ┌─────────────────────────────────────┐   │                │
│ │ TOOL EXECUTION                       │   │                │
│ │                                      │   │                │
│ │ For each tool call:                 │   │                │
│ │ 1. Check permissions                │   │                │
│ │ 2. Execute tool                     │   │                │
│ │ 3. Collect results                  │   │                │
│ └─────────────────┬───────────────────┘   │                │
│                   │                         │                │
│                   ▼                         │                │
│ ┌─────────────────────────────────────┐   │                │
│ │ Check doom loop                      │   │                │
│ │ (same tool 3+ times?)               │   │                │
│ └──────────┬──────────────────────────┘   │                │
│            │                                │                │
│     YES ───┤ BREAK                          │                │
│            │ NO                             │                │
│            ▼                                │                │
│ ┌─────────────────────────────────────┐   │                │
│ │ Add tool results to messages        │   │                │
│ │ Loop back to LLM  ──────────────────┘───┘                │
│ └─────────────────────────────────────┘                     │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │ (No more tool calls)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE TO USER                                            │
│ - Display final text                                        │
│ - Save conversation                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Tool Construction Deep Dive

### How Tools Are Built

**Every tool follows this structure:**

```typescript
// Tool interface
export const MyTool: Tool.Info = {
  id: "my-tool",  // Unique identifier

  async init(ctx?: InitContext) {
    return {
      // 1. Description (becomes part of system prompt)
      description: "Tool description that AI reads...",

      // 2. Parameters (Zod schema for validation)
      parameters: z.object({
        param1: z.string().describe("Description"),
        param2: z.number().optional()
      }),

      // 3. Execute function
      async execute(args, ctx: Tool.Context) {
        // a. Check permissions
        await ctx.ask({
          permission: "tool-permission",
          patterns: [args.param1]
        })

        // b. Do the work
        const result = await doWork(args)

        // c. Return result
        return {
          title: "What was done",
          output: "Result to show AI",
          metadata: { /* optional */ }
        }
      },

      // 4. Optional: Custom error formatting
      formatValidationError(error) {
        return `Custom error message: ${error.message}`
      }
    }
  }
}
```

### Real Example: Edit Tool

**File:** `packages/opencode/src/tool/edit.ts`

```typescript
export const EditTool: Tool.Info = {
  id: "edit",

  async init() {
    return {
      description: `Performs exact string replacements in files.

CRITICAL RULES:
1. MUST read file first (this tool errors if you haven't)
2. old_string must be EXACT match
3. new_string must be different
4. If old_string appears multiple times, edit fails
5. Use replace_all=true to replace all occurrences`,

      parameters: z.object({
        file_path: z.string(),
        old_string: z.string(),
        new_string: z.string(),
        replace_all: z.boolean().optional()
      }),

      async execute(args, ctx) {
        // 1. Check if file was read first
        const wasRead = await this.checkFileWasRead(
          ctx.sessionID,
          args.file_path
        )

        if (!wasRead) {
          throw new Error(
            'You must read the file first before editing!'
          )
        }

        // 2. Check permissions
        await ctx.ask({
          permission: "edit",
          patterns: [args.file_path]
        })

        // 3. Read current content
        const content = await fs.readFile(args.file_path, 'utf-8')

        // 4. Validate old_string exists
        if (!content.includes(args.old_string)) {
          throw new Error(
            `old_string not found in file`
          )
        }

        // 5. Check for ambiguity (multiple matches)
        const occurrences = (content.match(
          new RegExp(args.old_string, 'g')
        ) || []).length

        if (occurrences > 1 && !args.replace_all) {
          throw new Error(
            `old_string appears ${occurrences} times. ` +
            `Use replace_all=true or provide more context.`
          )
        }

        // 6. Perform replacement
        const newContent = args.replace_all
          ? content.replaceAll(args.old_string, args.new_string)
          : content.replace(args.old_string, args.new_string)

        // 7. Write back to file
        await fs.writeFile(args.file_path, newContent, 'utf-8')

        // 8. Return result
        return {
          title: `Edited ${path.basename(args.file_path)}`,
          output: `Successfully replaced ${occurrences} occurrence(s)`,
          metadata: {
            file: args.file_path,
            occurrences
          }
        }
      }
    }
  }
}
```

**Code Location:** [packages/opencode/src/tool/edit.ts](../packages/opencode/src/tool/edit.ts)

---

## 🔐 Permission Flow

```
Tool Execute Called
    ↓
ctx.ask({ permission, patterns })
    ↓
┌─────────────────────────────────────┐
│ Permission Check (permission/next.ts)│
└────────────┬────────────────────────┘
             │
             ▼
Check agent's permission ruleset
    │
    ├─ permission: "deny" → REJECT immediately
    │
    ├─ permission: "allow" → APPROVE immediately
    │
    └─ permission: "ask"
           │
           ▼
    Check if pattern in "always allowed" list
           │
           ├─ YES → APPROVE
           │
           └─ NO → Prompt user for approval
                  │
                  ├─ User approves → APPROVE + add to "always allowed"
                  │
                  └─ User denies → REJECT
```

**Code Location:** [packages/opencode/src/permission/next.ts](../packages/opencode/src/permission/next.ts)

---

## 🎯 Key Takeaways

1. **Everything flows through SessionProcessor** - It's the orchestrator
2. **Tools are self-contained** - Each tool handles its own logic
3. **Permissions are checked per-tool** - Via `ctx.ask()`
4. **Doom loop protection** - Same tool 3x = break
5. **Stream-based** - Real-time response display
6. **Conversation history** - Everything stored in session

---

## 📚 Next Steps

- [06-tool-construction-guide.md](06-tool-construction-guide.md) - Build your own tools
- [08-advanced-topics.md](08-advanced-topics.md) - MCP, Skills, Config, Plugins

**Now you understand the complete execution flow!**
