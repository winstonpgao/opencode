# Tool Construction Guide - Build Your Own Tools

## Complete Guide with Real Code Examples

**⚠️ IMPORTANT:** This document contains **SIMPLIFIED** code examples for educational clarity. The actual OpenCode tool implementations are more complex with:
- Generic type parameters for metadata
- Advanced error handling and retries
- File type detection (images, PDFs, binaries)
- Truncation limits and memory management
- Provider-specific transformations

For EXACT implementation details, read the actual tool files in `packages/opencode/src/tool/*.ts`.

---

## 📍 Code References

**Tool System:**
- Tool interface: `packages/opencode/src/tool/tool.ts`
- Tool registry: `packages/opencode/src/tool/registry.ts`
- All built-in tools: `packages/opencode/src/tool/*.ts`

**Example Tools:**
- Read: `packages/opencode/src/tool/read.ts`
- Glob: `packages/opencode/src/tool/glob.ts`
- Grep: `packages/opencode/src/tool/grep.ts`
- Edit: `packages/opencode/src/tool/edit.ts`
- Bash: `packages/opencode/src/tool/bash.ts`

---

## 🏗️ Tool Architecture

### Core Tool Interface

**File:** `packages/opencode/src/tool/tool.ts`

```typescript
export namespace Tool {
  // Context provided to every tool execution
  export interface Context {
    sessionID: string      // Current session
    messageID: string      // Current message
    agent: string          // Agent name (build, plan, etc.)
    callID: string         // Unique call ID
    abort: AbortSignal     // For cancellation

    // Request permission from user
    ask(request: PermissionRequest): Promise<void>

    // Update tool execution metadata
    metadata(input: {
      title?: string
      metadata?: Record<string, any>
    }): void
  }

  // Tool execution result
  export interface ExecuteResult {
    title: string                    // Short description
    output: string                   // Result content (shown to AI)
    metadata?: Record<string, any>   // Additional info
    attachments?: File[]             // Optional files
  }

  // Tool definition
  export interface Info {
    id: string  // Unique identifier

    // Initialize tool (can be async)
    init(ctx?: InitContext): Promise<{
      description: string           // Shown to AI in system prompt
      parameters: z.ZodType         // Zod schema for validation
      execute(                      // Main execution function
        args: any,
        ctx: Context
      ): Promise<ExecuteResult>
      formatValidationError?(       // Optional custom error formatting
        error: z.ZodError
      ): string
    }>
  }
}
```

---

## 🔨 Building Tools: Complete Examples

### Example 1: Simple Tool (Read)

**File:** `packages/opencode/src/tool/read.ts`

```typescript
import { Tool } from "./tool"
import { z } from "zod"
import fs from "fs/promises"
import path from "path"

export const ReadTool: Tool.Info = {
  id: "read",

  async init() {
    return {
      // 1. DESCRIPTION
      // This becomes part of the system prompt that the AI reads
      description: `Reads a file from the local filesystem.

Usage:
- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to 2000 lines starting from the beginning
- You can optionally specify a line offset and limit for large files
- Lines longer than 2000 characters will be truncated
- Results are returned using cat -n format, with line numbers starting at 1
- Can read images (PNG, JPG), PDFs, Jupyter notebooks

IMPORTANT:
- ALWAYS use absolute paths
- You can call multiple Read tools in parallel if reading independent files
- Will receive a warning if file exists but is empty

Example:
Read({ file_path: "/project/src/app.ts" })
Read({ file_path: "/project/large.log", offset: 2000, limit: 1000 })`,

      // 2. PARAMETERS
      // Zod schema for validation
      parameters: z.object({
        file_path: z.string().describe("The absolute path to the file to read"),
        offset: z.number().optional().describe("The line number to start reading from"),
        limit: z.number().optional().describe("The number of lines to read (default: 2000)")
      }),

      // 3. EXECUTE FUNCTION
      async execute(args, ctx) {
        // Step 1: Check permissions
        await ctx.ask({
          permission: "read",
          patterns: [args.file_path]
        })

        // Step 2: Validate file exists
        try {
          await fs.access(args.file_path)
        } catch {
          throw new Error(`File not found: ${args.file_path}`)
        }

        // Step 3: Read file content
        const content = await fs.readFile(args.file_path, 'utf-8')

        // Step 4: Split into lines
        const lines = content.split('\n')

        // Step 5: Apply offset and limit
        const offset = args.offset || 0
        const limit = args.limit || 2000
        const selectedLines = lines.slice(offset, offset + limit)

        // Step 6: Format with line numbers (cat -n style)
        const output = selectedLines
          .map((line, index) => {
            const lineNumber = offset + index + 1
            // Truncate long lines
            const truncated = line.length > 2000
              ? line.substring(0, 2000) + '...'
              : line
            return `${lineNumber}\t${truncated}`
          })
          .join('\n')

        // Step 7: Add warning if file is empty
        if (lines.length === 0) {
          ctx.metadata({
            metadata: { warning: 'File exists but is empty' }
          })
        }

        // Step 8: Return result
        return {
          title: `Read ${path.basename(args.file_path)}`,
          output,
          metadata: {
            file: args.file_path,
            totalLines: lines.length,
            returnedLines: selectedLines.length,
            truncated: lines.length > (offset + limit)
          }
        }
      },

      // 4. OPTIONAL: Custom error formatting
      formatValidationError(error) {
        if (error.issues[0]?.path[0] === 'file_path') {
          return 'Error: file_path is required and must be an absolute path'
        }
        return error.message
      }
    }
  }
}
```

**Code Location:** [packages/opencode/src/tool/read.ts](../packages/opencode/src/tool/read.ts)

---

### Example 2: Complex Tool (Grep)

**File:** `packages/opencode/src/tool/grep.ts`

```typescript
import { Tool } from "./tool"
import { z } from "zod"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export const GrepTool: Tool.Info = {
  id: "grep",

  async init() {
    return {
      description: `Powerful search tool built on ripgrep.

Parameters:
- pattern: regex pattern to search for (required)
- path: file or directory to search (optional, defaults to cwd)
- glob: filter files with pattern like "*.js" (optional)
- type: file type to search like "js", "py", "rust" (optional)
- output_mode: "files_with_matches" (default), "content", or "count"
- -i: case insensitive search (optional)
- -A: lines after match (optional, requires output_mode: "content")
- -B: lines before match (optional, requires output_mode: "content")
- -C: lines before and after (optional, requires output_mode: "content")
- -n: show line numbers (default: true, requires output_mode: "content")
- head_limit: limit output lines (optional)
- offset: skip first N results (optional)
- multiline: enable multiline mode where . matches newlines (optional)

Usage:
- Supports full regex syntax
- Use Grep for searching file contents
- Use Glob for finding files by name pattern
- Lines longer than 2000 chars are truncated

Examples:
Grep({ pattern: "function loginUser", output_mode: "files_with_matches" })
Grep({ pattern: "TODO:", output_mode: "content", -A: 2 })
Grep({ pattern: "useState", glob: "*.tsx" })`,

      parameters: z.object({
        pattern: z.string(),
        path: z.string().optional(),
        glob: z.string().optional(),
        type: z.string().optional(),
        output_mode: z.enum(["files_with_matches", "content", "count"]).optional(),
        "-i": z.boolean().optional(),
        "-A": z.number().optional(),
        "-B": z.number().optional(),
        "-C": z.number().optional(),
        "-n": z.boolean().optional(),
        head_limit: z.number().optional(),
        offset: z.number().optional(),
        multiline: z.boolean().optional()
      }),

      async execute(args, ctx) {
        // Step 1: Build ripgrep command
        const rgArgs = ['rg']

        // Add pattern
        rgArgs.push(args.pattern)

        // Add path if specified
        if (args.path) {
          rgArgs.push(args.path)
        }

        // Output mode
        const outputMode = args.output_mode || "files_with_matches"
        if (outputMode === "files_with_matches") {
          rgArgs.push('-l')  // Only filenames
        } else if (outputMode === "count") {
          rgArgs.push('-c')  // Count per file
        }

        // Case insensitive
        if (args["-i"]) {
          rgArgs.push('-i')
        }

        // Context lines (only for content mode)
        if (outputMode === "content") {
          if (args["-A"]) rgArgs.push(`-A${args["-A"]}`)
          if (args["-B"]) rgArgs.push(`-B${args["-B"]}`)
          if (args["-C"]) rgArgs.push(`-C${args["-C"]}`)

          // Line numbers (default true)
          if (args["-n"] !== false) {
            rgArgs.push('-n')
          }
        }

        // File filtering
        if (args.glob) {
          rgArgs.push('--glob', args.glob)
        }
        if (args.type) {
          rgArgs.push('--type', args.type)
        }

        // Multiline mode
        if (args.multiline) {
          rgArgs.push('-U', '--multiline-dotall')
        }

        // Max line length (prevent huge outputs)
        rgArgs.push('--max-columns', '2000')

        // Step 2: Check permissions
        const searchPath = args.path || process.cwd()
        await ctx.ask({
          permission: "grep",
          patterns: [searchPath]
        })

        // Step 3: Execute ripgrep
        try {
          const { stdout } = await execAsync(rgArgs.join(' '), {
            maxBuffer: 10 * 1024 * 1024  // 10MB max output
          })

          // Step 4: Process output
          let lines = stdout.trim().split('\n')

          // Apply offset and limit
          if (args.offset) {
            lines = lines.slice(args.offset)
          }
          if (args.head_limit) {
            lines = lines.slice(0, args.head_limit)
          }

          const output = lines.join('\n')

          // Step 5: Return result
          return {
            title: `Grep: ${args.pattern}`,
            output: output || 'No matches found',
            metadata: {
              pattern: args.pattern,
              matches: lines.length,
              truncated: args.head_limit && lines.length >= args.head_limit
            }
          }

        } catch (error) {
          // ripgrep returns exit code 1 when no matches found
          if (error.code === 1) {
            return {
              title: `Grep: ${args.pattern}`,
              output: 'No matches found',
              metadata: { pattern: args.pattern, matches: 0 }
            }
          }
          throw error
        }
      }
    }
  }
}
```

**Code Location:** [packages/opencode/src/tool/grep.ts](../packages/opencode/src/tool/grep.ts)

---

### Example 3: Interactive Tool (Question)

**File:** `packages/opencode/src/tool/question.ts`

```typescript
import { Tool } from "./tool"
import { z } from "zod"

export const QuestionTool: Tool.Info = {
  id: "question",

  async init() {
    return {
      description: `Ask the user questions during execution.

Use this to:
- Gather user preferences or requirements
- Clarify ambiguous instructions
- Get decisions on implementation choices
- Offer choices about direction

Parameters:
- questions: array of question objects (1-4 questions)
  - question: the question text
  - header: short label (max 12 chars)
  - multiSelect: allow multiple answers (default: false)
  - options: array of choices (2-4 options)
    - label: option text (1-5 words)
    - description: explanation of what this option means

Usage:
- Users can always select "Other" to provide custom text
- Use multiSelect: true to allow multiple selections
- Put recommended option first and add "(Recommended)" to label

Example:
Question({
  questions: [{
    question: "Which database would you like to use?",
    header: "Database",
    multiSelect: false,
    options: [
      { label: "PostgreSQL", description: "Production-ready SQL" },
      { label: "MongoDB", description: "NoSQL document store" },
      { label: "SQLite", description: "Lightweight file-based" }
    ]
  }]
})`,

      parameters: z.object({
        questions: z.array(z.object({
          question: z.string(),
          header: z.string().max(12),
          multiSelect: z.boolean(),
          options: z.array(z.object({
            label: z.string(),
            description: z.string()
          })).min(2).max(4)
        })).min(1).max(4)
      }),

      async execute(args, ctx) {
        // Step 1: Check if interactive mode available
        // (Question tool only works in app/cli/desktop, not headless)
        if (!this.isInteractive()) {
          throw new Error(
            'Question tool is not available in headless mode'
          )
        }

        // Step 2: Request permission (user must approve showing UI)
        await ctx.ask({
          permission: "question",
          patterns: []
        })

        // Step 3: Show question UI to user
        const answers = await this.showQuestionUI(args.questions)

        // Step 4: Format answers
        const formattedAnswers = args.questions.map((q, i) => {
          const answer = answers[i]
          return `${q.header}: ${answer.join(', ')}`
        }).join('\n')

        // Step 5: Return result
        return {
          title: 'User answered questions',
          output: formattedAnswers,
          metadata: { answers }
        }
      }
    }
  }

  private isInteractive(): boolean {
    // Check if running in interactive environment
    return ['app', 'cli', 'desktop'].includes(
      process.env.OPENCODE_CLIENT
    )
  }

  private async showQuestionUI(questions): Promise<string[][]> {
    // Implementation of UI prompt
    // Returns array of arrays (for multiSelect)
    // This connects to the CLI/desktop app UI
  }
}
```

**Code Location:** [packages/opencode/src/tool/question.ts](../packages/opencode/src/tool/question.ts)

---

## 🔧 Tool Registration

### How Tools Are Registered

**File:** `packages/opencode/src/tool/registry.ts`

```typescript
export namespace ToolRegistry {
  async function all(): Promise<Tool.Info[]> {
    const custom = await loadCustomTools()  // From user plugins
    const config = await Config.get()

    return [
      // Core tools (always available)
      InvalidTool,
      QuestionTool,  // Only in app/cli/desktop
      BashTool,
      ReadTool,
      GlobTool,
      GrepTool,
      EditTool,
      WriteTool,
      TaskTool,
      WebFetchTool,
      TodoWriteTool,
      TodoReadTool,
      WebSearchTool,
      CodeSearchTool,
      SkillTool,
      ApplyPatchTool,

      // Experimental tools (gated by flags)
      ...(Flag.OPENCODE_EXPERIMENTAL_LSP_TOOL ? [LspTool] : []),
      ...(config.experimental?.batch_tool ? [BatchTool] : []),
      ...(Flag.OPENCODE_EXPERIMENTAL_PLAN_MODE ? [PlanExitTool, PlanEnterTool] : []),

      // Custom tools from plugins
      ...custom
    ]
  }

  // Filter tools based on model and agent
  export async function tools(
    model: Provider.Model,
    agent?: Agent.Info
  ): Promise<Record<string, Tool>> {
    const allTools = await all()

    const filtered = allTools.filter(tool => {
      // Filter by model
      if (tool.id === "apply_patch") {
        // Only for GPT models
        return model.modelID.includes('gpt-')
      }
      if (tool.id === "edit" || tool.id === "write") {
        // Not for newer GPT models (they use apply_patch)
        return !model.modelID.includes('gpt-4')
      }

      // Filter by provider
      if (tool.id === "websearch" || tool.id === "codesearch") {
        return model.providerID === "opencode" || Flag.OPENCODE_ENABLE_EXA
      }

      // Filter by agent permissions
      if (agent) {
        const permission = agent.permission[tool.id]
        if (permission === "deny") return false
      }

      return true
    })

    // Initialize all tools
    const initialized = await Promise.all(
      filtered.map(async tool => ({
        id: tool.id,
        ...await tool.init()
      }))
    )

    // Return as record
    return Object.fromEntries(
      initialized.map(tool => [tool.id, tool])
    )
  }
}
```

**Code Location:** [packages/opencode/src/tool/registry.ts](../packages/opencode/src/tool/registry.ts)

---

## 🎯 Creating Your Own Tool

### Custom Tool Template

Create: `.opencode/tools/my-tool.ts`

```typescript
import { z } from "zod"

export default {
  description: `Your tool description here.

This text becomes part of the system prompt that the AI reads.
Explain:
- What the tool does
- When to use it
- What parameters are needed
- Any important rules or constraints`,

  args: {
    // Define parameters using Zod-style objects
    param1: {
      type: "string",
      description: "Description of param1"
    },
    param2: {
      type: "number",
      description: "Description of param2",
      optional: true
    }
  },

  async execute(args, ctx) {
    // 1. Check permissions (optional)
    await ctx.ask({
      permission: "my-tool",
      patterns: [args.param1]
    })

    // 2. Do your work
    const result = await doSomething(args.param1, args.param2)

    // 3. Return result
    return {
      title: "What was accomplished",
      output: "Result shown to AI",
      metadata: { /* optional extra info */ }
    }
  }
}
```

**Auto-registered on startup!**

---

## 📊 Tool Execution Flow

```
AI Calls Tool
    ↓
┌─────────────────────────────────────┐
│ Processor detects tool call         │
│ (processor.ts)                       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Validate parameters                  │
│ (using Zod schema)                   │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Call tool.execute(args, ctx)        │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Tool checks permissions              │
│ ctx.ask({ permission, patterns })    │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Permission system checks             │
│ (permission/next.ts)                 │
│ - Check agent rules                  │
│ - Check if "always allowed"          │
│ - Prompt user if needed              │
└────────────────┬────────────────────┘
                 │
          APPROVED│
                 ▼
┌─────────────────────────────────────┐
│ Tool performs work                   │
│ (file operations, commands, etc.)    │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Tool returns ExecuteResult           │
│ { title, output, metadata }          │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ Processor sends result back to AI    │
│ (as tool_result message)             │
└────────────────┬────────────────────┘
                 │
                 ▼
AI reads result, decides next action
```

---

## 🔑 Key Concepts

### 1. Tools Are Self-Contained
Each tool:
- Defines its own description
- Validates its own parameters
- Handles its own errors
- Manages its own permissions

### 2. Description Becomes System Prompt
The `description` field is added to the system prompt that the AI reads. Make it:
- Clear and specific
- Include usage rules
- Show examples
- Explain when to use it

### 3. Context Provides Utilities
The `ctx` parameter gives tools access to:
- Permission system: `ctx.ask()`
- Metadata updates: `ctx.metadata()`
- Session info: `ctx.sessionID`
- Abort signal: `ctx.abort`

### 4. Validation Is Automatic
Zod schemas automatically:
- Validate parameter types
- Check required fields
- Format error messages
- Convert types

### 5. Permissions Are Per-Call
Every tool execution can request permissions for specific files/patterns.

---

## 📚 Next Steps

- [05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md) - Full system flow
- [08-advanced-topics.md](08-advanced-topics.md) - MCP, Skills, Config
- Try building your own tool in `.opencode/tools/`!

**Now you can build custom tools!**
