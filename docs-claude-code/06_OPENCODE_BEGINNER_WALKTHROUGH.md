# OpenCode: Beginner-Friendly Complete Walkthrough

**Purpose**: Step-by-step explanation of how OpenCode works, from the lowest layer to the highest, showing exact connections between files and functions.

**Repository**: https://github.com/opencode-ai/opencode (archived, continued as Crush)

**Local Copy**: C:/Users/winst/Github/opencode/

---

# HOW TO READ THIS DOCUMENT

## Recommended Reading Order

**If you're completely new to coding agents**, follow this order:

```
START HERE
    ↓
[Part 1] Architecture Overview Diagram ← See the big picture first
    ↓
[Part 12] Complete Execution Trace ← See a real example end-to-end
    ↓
[Part 5] Layer 4: Agent Loop ← Understand THE HEART
    ↓
[Part 6] Layer 5: Tools System ← How actions are performed
    ↓
Go back to Parts 2-4 for startup details
    ↓
Read Parts 7-11 for supporting systems
```

## Key Go Syntax Explained (For Beginners)

If you don't know Go, here are the patterns you'll see:

### 1. Function Definition
```go
func functionName(param1 Type1, param2 Type2) ReturnType {
    // code here
    return result
}
```

### 2. Method on a Struct (like a class method)
```go
// This function belongs to the "agent" type
func (a *agent) Run(ctx context.Context, sessionID string) {
    // "a" is like "self" or "this" in Python/JavaScript
    a.tools  // access agent's tools
}
```

### 3. Interface (like abstract class)
```go
type BaseTool interface {
    Info() ToolInfo                    // Any tool MUST have Info()
    Run(ctx, params) (ToolResponse)    // Any tool MUST have Run()
}
```

### 4. Goroutine (run in background)
```go
go func() {
    // This runs concurrently (like a thread)
}()
```

### 5. Channel (send/receive data between goroutines)
```go
ch := make(chan Event)    // Create channel
ch <- event               // Send to channel
result := <-ch            // Receive from channel (BLOCKS until data arrives)
```

### 6. Select (wait for multiple channels)
```go
select {
case <-ctx.Done():    // If context cancelled
    return error
default:              // Otherwise continue
}
```

### 7. For Loop (also used as while loop)
```go
for {                    // Infinite loop (like while True)
    if done {
        break            // Exit loop
    }
    continue             // Go to next iteration
}
```

## Symbols Used in This Document

| Symbol | Meaning |
|--------|---------|
| `→` | Calls / leads to |
| `←` | Returns / receives from |
| `↓` | Next step |
| `├──` | One of multiple paths |
| `└──` | Last/only path |
| `✓` | Success/complete |

---

# TABLE OF CONTENTS

1. [Architecture Overview Diagram](#1-architecture-overview-diagram)
2. [Layer 1: Entry Point](#2-layer-1-entry-point-maingo)
3. [Layer 2: CLI Framework](#3-layer-2-cli-framework-cmdrootgo)
4. [Layer 3: Application Core](#4-layer-3-application-core-internalappappgo)
5. [Layer 4: Agent Loop](#5-layer-4-the-agent-loop-internalllmagent)
6. [Layer 5: Tools System](#6-layer-5-tools-system-internalllmtools)
7. [Layer 6: LLM Providers](#7-layer-6-llm-providers-internalllmprovider)
8. [Layer 7: System Prompts](#8-layer-7-system-prompts-internalllmprompt)
9. [Layer 8: Data Storage](#9-layer-8-data-storage-internaldb-session-message)
10. [Layer 9: Permission System](#10-layer-9-permission-system-internalpermission)
11. [Layer 10: Terminal UI](#11-layer-10-terminal-ui-internaltui)
12. [Complete Execution Trace](#12-complete-execution-trace)
13. [Function Call Graph](#13-function-call-graph)

---

# 1. ARCHITECTURE OVERVIEW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER TYPES COMMAND                              │
│                              $ opencode "Fix bug"                            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: ENTRY POINT                                                        │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  main.go:8-13                                                          │ │
│  │  func main() {                                                         │ │
│  │      cmd.Execute()  ─────────────────────────────────────────────────────┼─┐
│  │  }                                                                     │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │
└──────────────────────────────────────────────────────────────────────────────┘ │
                                                                                 ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│  LAYER 2: CLI FRAMEWORK (cobra)                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  cmd/root.go:284-289                                                   │ │
│  │  func Execute() {                                                      │ │
│  │      rootCmd.Execute() ───────────────────────────────────────────────────┼─┐
│  │  }                                                                     │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │
│                                                                              │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │
│  │  cmd/root.go:49-183 (rootCmd.RunE)                                     │ │ │
│  │  1. config.Load() ← Load .opencode.json                                │ │ │
│  │  2. db.Connect() ← SQLite connection                                   │ │ │
│  │  3. app.New() ← Create application ─────────────────────────────────────┼─┼─┐
│  │  4. initMCPTools() ← Load MCP servers                                  │ │ │ │
│  │  5. If prompt flag: app.RunNonInteractive() ────────────────────────────┼─┼─┼─┐
│  │  6. Else: tui.New() → program.Run() ← Start TUI                        │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │
└──────────────────────────────────────────────────────────────────────────────┘ │ │ │
                                       ↓ (from line 3)                           │ │ │
┌──────────────────────────────────────────────────────────────────────────────┐ │ │ │
│  LAYER 3: APPLICATION CORE                                                   │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │
│  │  internal/app/app.go:42-81                                             │ │ │ │ │
│  │  func New(ctx, conn) (*App, error) {                                   │ │ │ │ │
│  │      sessions := session.NewService(q)                                 │ │ │ │ │
│  │      messages := message.NewService(q)                                 │ │ │ │ │
│  │      history  := history.NewService(q, conn)                           │ │ │ │ │
│  │                                                                        │ │ │ │ │
│  │      app.CoderAgent = agent.NewAgent(                                  │ │ │ │ │
│  │          config.AgentCoder,                                            │ │ │ │ │
│  │          sessions, messages,                                           │ │ │ │ │
│  │          agent.CoderAgentTools(...) ← Register all tools ────────────────┼─┼─┼─┼─┐
│  │      )                                                                 │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │
│                                                                              │ │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │
│  │  internal/app/app.go:100-161 (RunNonInteractive)                       │ │ │ │ │ │
│  │  func (a *App) RunNonInteractive(ctx, prompt, format, quiet) {         │ │ │ │ │ │
│  │      sess, _ := a.Sessions.Create(ctx, title)                          │ │ │ │ │ │
│  │      a.Permissions.AutoApproveSession(sess.ID)                         │ │ │ │ │ │
│  │      done, _ := a.CoderAgent.Run(ctx, sess.ID, prompt) ←───────────────────┼─┼─┼─┼─┼─┐
│  │      result := <-done                                                  │ │ │ │ │ │ │
│  │      fmt.Println(result.Message.Content())                             │ │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │
└──────────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │
                                       ↓ (from CoderAgent.Run)                   │ │ │ │ │
┌──────────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │
│  LAYER 4: THE AGENT LOOP (THE HEART!)                                        │ │ │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │ │
│  │  internal/llm/agent/agent.go:198-231 (Run)                             │ │ │ │ │ │ │
│  │  func (a *agent) Run(ctx, sessionID, content) (<-chan AgentEvent) {    │ │ │ │ │ │ │
│  │      go func() {                                                       │ │ │ │ │ │ │
│  │          result := a.processGeneration(ctx, sessionID, content) ─────────┼─┼─┼─┼─┼─┼─┐
│  │          events <- result                                              │ │ │ │ │ │ │ │
│  │      }()                                                               │ │ │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │
│                                                                              │ │ │ │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │ │ │
│  │  internal/llm/agent/agent.go:233-311 (processGeneration) ← THE LOOP!   │ │ │ │ │ │ │ │
│  │  func (a *agent) processGeneration(ctx, sessionID, content) AgentEvent{│ │ │ │ │ │ │ │
│  │      msgs, _ := a.messages.List(ctx, sessionID)  ← Get history         │ │ │ │ │ │ │ │
│  │      userMsg := a.createUserMessage(ctx, sessionID, content)           │ │ │ │ │ │ │ │
│  │      msgHistory := append(msgs, userMsg)                               │ │ │ │ │ │ │ │
│  │                                                                        │ │ │ │ │ │ │ │
│  │      for {  ← ──────────────────── THIS IS THE AGENT LOOP ─────────────│ │ │ │ │ │ │ │
│  │          select {                                                      │ │ │ │ │ │ │ │
│  │          case <-ctx.Done():                                            │ │ │ │ │ │ │ │
│  │              return a.err(ctx.Err())  ← User cancelled                 │ │ │ │ │ │ │ │
│  │          default:                                                      │ │ │ │ │ │ │ │
│  │          }                                                             │ │ │ │ │ │ │ │
│  │                                                                        │ │ │ │ │ │ │ │
│  │          agentMsg, toolResults, _ := a.streamAndHandleEvents(          │ │ │ │ │ │ │ │
│  │              ctx, sessionID, msgHistory                                │ │ │ │ │ │ │ │
│  │          ) ─────────────────────────────────────────────────────────────┼─┼─┼─┼─┼─┼─┼─┐
│  │                                                                        │ │ │ │ │ │ │ │ │
│  │          if agentMsg.FinishReason() == FinishReasonToolUse {           │ │ │ │ │ │ │ │ │
│  │              msgHistory = append(msgHistory, agentMsg, *toolResults)   │ │ │ │ │ │ │ │ │
│  │              continue  ← LOOP BACK! LLM will see tool results          │ │ │ │ │ │ │ │ │
│  │          }                                                             │ │ │ │ │ │ │ │ │
│  │                                                                        │ │ │ │ │ │ │ │ │
│  │          return AgentEvent{Message: agentMsg, Done: true}  ← DONE!     │ │ │ │ │ │ │ │ │
│  │      }                                                                 │ │ │ │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │ │
│                                                                              │ │ │ │ │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │ │ │ │
│  │  internal/llm/agent/agent.go:322-438 (streamAndHandleEvents)           │ │ │ │ │ │ │ │ │
│  │  func (a *agent) streamAndHandleEvents(ctx, sessionID, msgHistory) {   │ │ │ │ │ │ │ │ │
│  │      eventChan := a.provider.StreamResponse(ctx, msgHistory, a.tools)  │ │ │ │ │ │ │ │ │
│  │                         ↓                                              │ │ │ │ │ │ │ │ │
│  │      Calls LLM API (Claude, GPT, etc.) with streaming                  │ │ │ │ │ │ │ │ │
│  │                         ↓                                              │ │ │ │ │ │ │ │ │
│  │      for event := range eventChan {                                    │ │ │ │ │ │ │ │ │
│  │          a.processEvent(ctx, sessionID, &assistantMsg, event)          │ │ │ │ │ │ │ │ │
│  │      }                                                                 │ │ │ │ │ │ │ │ │
│  │                         ↓                                              │ │ │ │ │ │ │ │ │
│  │      for _, toolCall := range assistantMsg.ToolCalls() {               │ │ │ │ │ │ │ │ │
│  │          tool := findToolByName(toolCall.Name)                         │ │ │ │ │ │ │ │ │
│  │          result := tool.Run(ctx, toolCall) ← EXECUTE TOOL! ──────────────┼─┼─┼─┼─┼─┼─┼─┼─┐
│  │          toolResults[i] = result                                       │ │ │ │ │ │ │ │ │ │
│  │      }                                                                 │ │ │ │ │ │ │ │ │ │
│  │                                                                        │ │ │ │ │ │ │ │ │ │
│  │      return assistantMsg, toolResultsMsg, nil                          │ │ │ │ │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │ │ │
└──────────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │ │
                                       ↓ (tool.Run)                              │ │ │ │ │ │ │ │
┌──────────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │ │ │ │
│  LAYER 5: TOOLS SYSTEM                                                       │ │ │ │ │ │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │ │ │ │ │
│  │  internal/llm/agent/tools.go:14-41 (CoderAgentTools)                   │ │ │ │ │ │ │ │ │ │
│  │  func CoderAgentTools(...) []tools.BaseTool {                          │ │ │ │ │ │ │ │ │ │
│  │      return []tools.BaseTool{                                          │ │ │ │ │ │ │ │ │ │
│  │          tools.NewBashTool(permissions),    ← bash.go                  │ │ │ │ │ │ │ │ │ │
│  │          tools.NewEditTool(...),            ← edit.go                  │ │ │ │ │ │ │ │ │ │
│  │          tools.NewFetchTool(permissions),   ← fetch.go                 │ │ │ │ │ │ │ │ │ │
│  │          tools.NewGlobTool(),               ← glob.go                  │ │ │ │ │ │ │ │ │ │
│  │          tools.NewGrepTool(),               ← grep.go                  │ │ │ │ │ │ │ │ │ │
│  │          tools.NewLsTool(),                 ← ls.go                    │ │ │ │ │ │ │ │ │ │
│  │          tools.NewSourcegraphTool(),        ← sourcegraph.go           │ │ │ │ │ │ │ │ │ │
│  │          tools.NewViewTool(lspClients),     ← view.go                  │ │ │ │ │ │ │ │ │ │
│  │          tools.NewPatchTool(...),           ← patch.go                 │ │ │ │ │ │ │ │ │ │
│  │          tools.NewWriteTool(...),           ← write.go                 │ │ │ │ │ │ │ │ │ │
│  │          NewAgentTool(...),                 ← agent-tool.go (sub-agent)│ │ │ │ │ │ │ │ │ │
│  │      }                                                                 │ │ │ │ │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │ │ │
│                                                                              │ │ │ │ │ │ │ │ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │ │ │ │ │ │ │ │ │
│  │  internal/llm/tools/tools.go:69-72 (BaseTool Interface)                │ │ │ │ │ │ │ │ │ │
│  │  type BaseTool interface {                                             │ │ │ │ │ │ │ │ │ │
│  │      Info() ToolInfo                  ← Name, Description, Parameters  │ │ │ │ │ │ │ │ │ │
│  │      Run(ctx, params) (ToolResponse)  ← Execute the tool               │ │ │ │ │ │ │ │ │ │
│  │  }                                                                     │ │ │ │ │ │ │ │ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │ │ │
└──────────────────────────────────────────────────────────────────────────────┘ │ │ │ │ │ │ │ │
                                                                                 │ │ │ │ │ │ │ │
   Layers 6-10 support the above core flow                                       │ │ │ │ │ │ │ │
                                                                                 │ │ │ │ │ │ │ │
└─────────────────────────────────────────────────────────────────────────────────┴─┴─┴─┴─┴─┴─┴─┘
```

---

# 2. LAYER 1: ENTRY POINT (main.go)

## File: `main.go`

```go
package main

import (
    "github.com/opencode-ai/opencode/cmd"
    "github.com/opencode-ai/opencode/internal/logging"
)

func main() {
    // Recover from any panics and log them
    defer logging.RecoverPanic("main", func() {
        logging.ErrorPersist("Application terminated due to unhandled panic")
    })

    cmd.Execute()  // ← CALLS Layer 2
}
```

### What This Does

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `package main` | Go entry point must be in package main |
| 3-6 | `import (...)` | Import CLI handler and logging |
| 8 | `func main()` | Program starts here |
| 9-11 | `defer logging.RecoverPanic(...)` | Catch any crashes and log them |
| 13 | `cmd.Execute()` | **Hand off to CLI framework** |

### Connection to Next Layer

```
main.go:13
    ↓
cmd.Execute()  → cmd/root.go:284
```

---

# 3. LAYER 2: CLI FRAMEWORK (cmd/root.go)

## File: `cmd/root.go`

This file uses [Cobra](https://github.com/spf13/cobra), a popular Go CLI framework.

### Part 1: Command Definition (Lines 24-48)

```go
var rootCmd = &cobra.Command{
    Use:   "opencode",
    Short: "Terminal-based AI assistant for software development",
    Long:  `OpenCode is a powerful terminal-based AI assistant...`,
    Example: `
      opencode              # Interactive mode
      opencode -p "Fix bug" # Non-interactive mode
    `,
    RunE: func(cmd *cobra.Command, args []string) error {
        // Main logic here (see Part 2)
    },
}
```

### Part 2: Main Initialization (Lines 49-183)

```go
RunE: func(cmd *cobra.Command, args []string) error {
    // 1. PARSE FLAGS
    debug, _ := cmd.Flags().GetBool("debug")
    cwd, _ := cmd.Flags().GetString("cwd")
    prompt, _ := cmd.Flags().GetString("prompt")

    // 2. CHANGE DIRECTORY if specified
    if cwd != "" {
        os.Chdir(cwd)
    }

    // 3. LOAD CONFIGURATION (.opencode.json)
    config.Load(cwd, debug)

    // 4. CONNECT TO DATABASE (SQLite)
    conn, err := db.Connect()

    // 5. CREATE MAIN CONTEXT (for cancellation)
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // 6. CREATE APPLICATION (Layer 3)
    app, err := app.New(ctx, conn)  // ← CALLS Layer 3
    defer app.Shutdown()

    // 7. INITIALIZE MCP TOOLS
    initMCPTools(ctx, app)

    // 8. DECIDE MODE
    if prompt != "" {
        // Non-interactive: single prompt
        return app.RunNonInteractive(ctx, prompt, outputFormat, quiet)
    }

    // 9. INTERACTIVE MODE: Start TUI
    program := tea.NewProgram(tui.New(app), tea.WithAltScreen())

    // 10. SET UP EVENT SUBSCRIPTIONS
    ch, cancelSubs := setupSubscriptions(app, ctx)

    // 11. RUN THE TUI
    result, err := program.Run()
    return nil
}
```

### Part 3: Execute Function (Lines 284-289)

```go
func Execute() {
    err := rootCmd.Execute()  // Run the Cobra command
    if err != nil {
        os.Exit(1)
    }
}
```

### Part 4: Subscriptions Setup (Lines 249-282)

```go
func setupSubscriptions(app *app.App, parentCtx context.Context) (chan tea.Msg, func()) {
    ch := make(chan tea.Msg, 100)

    // Subscribe to all services - when they publish events, forward to TUI
    setupSubscriber(ctx, &wg, "logging", logging.Subscribe, ch)
    setupSubscriber(ctx, &wg, "sessions", app.Sessions.Subscribe, ch)
    setupSubscriber(ctx, &wg, "messages", app.Messages.Subscribe, ch)
    setupSubscriber(ctx, &wg, "permissions", app.Permissions.Subscribe, ch)
    setupSubscriber(ctx, &wg, "coderAgent", app.CoderAgent.Subscribe, ch)

    return ch, cleanupFunc
}
```

### Connection Diagram

```
cmd/root.go:100                    cmd/root.go:114
app.New(ctx, conn) ──────────────→ app.RunNonInteractive(...)
        ↓                                    ↓
internal/app/app.go:42             internal/app/app.go:100
```

---

# 4. LAYER 3: APPLICATION CORE (internal/app/app.go)

## File: `internal/app/app.go`

### Part 1: App Structure (Lines 25-40)

```go
type App struct {
    Sessions    session.Service      // Conversation sessions
    Messages    message.Service      // Message storage
    History     history.Service      // File change tracking
    Permissions permission.Service   // Tool permission gates

    CoderAgent agent.Service         // THE AI AGENT (Layer 4)

    LSPClients map[string]*lsp.Client // Language Server connections
}
```

### Part 2: App Creation (Lines 42-81)

```go
func New(ctx context.Context, conn *sql.DB) (*App, error) {
    q := db.New(conn)  // Database query wrapper

    // Create services
    sessions := session.NewService(q)
    messages := message.NewService(q)
    history  := history.NewService(q, conn)

    app := &App{
        Sessions:    sessions,
        Messages:    messages,
        History:     history,
        Permissions: permission.NewPermissionService(),
        LSPClients:  make(map[string]*lsp.Client),
    }

    // Initialize LSP clients in background
    go app.initLSPClients(ctx)

    // CREATE THE CODER AGENT (Layer 4)
    app.CoderAgent, err = agent.NewAgent(
        config.AgentCoder,           // Agent name
        app.Sessions,                // Session service
        app.Messages,                // Message service
        agent.CoderAgentTools(       // ALL TOOLS (Layer 5)
            app.Permissions,
            app.Sessions,
            app.Messages,
            app.History,
            app.LSPClients,
        ),
    )

    return app, nil
}
```

### Part 3: Non-Interactive Mode (Lines 100-161)

```go
func (a *App) RunNonInteractive(ctx context.Context, prompt string, outputFormat string, quiet bool) error {
    // 1. Create a new session
    sess, err := a.Sessions.Create(ctx, "Non-interactive: " + prompt)

    // 2. Auto-approve all permissions for non-interactive mode
    a.Permissions.AutoApproveSession(sess.ID)

    // 3. RUN THE AGENT (Layer 4)
    done, err := a.CoderAgent.Run(ctx, sess.ID, prompt)

    // 4. Wait for result
    result := <-done

    // 5. Print the response
    fmt.Println(result.Message.Content())

    return nil
}
```

### Connection Diagram

```
internal/app/app.go:63-74                      internal/app/app.go:131
agent.NewAgent(                                a.CoderAgent.Run(ctx, sess.ID, prompt)
    config.AgentCoder,                                     ↓
    sessions, messages,                        internal/llm/agent/agent.go:198
    agent.CoderAgentTools(...)  ←────────────→ func (a *agent) Run(...)
)
        ↓
internal/llm/agent/tools.go:14
```

---

# 5. LAYER 4: THE AGENT LOOP (internal/llm/agent/)

This is the **HEART** of the coding agent. The agent loop is what makes it "agentic".

## File: `internal/llm/agent/agent.go`

### Part 1: Agent Structure (Lines 59-71)

```go
type agent struct {
    *pubsub.Broker[AgentEvent]  // Event publisher
    sessions session.Service    // Session management
    messages message.Service    // Message storage

    tools    []tools.BaseTool   // ALL AVAILABLE TOOLS
    provider provider.Provider  // LLM API (Claude, GPT, etc.)

    titleProvider     provider.Provider  // For generating titles
    summarizeProvider provider.Provider  // For summarizing

    activeRequests sync.Map  // Track running requests
}
```

### Part 2: Agent Creation (Lines 73-111)

```go
func NewAgent(
    agentName config.AgentName,
    sessions session.Service,
    messages message.Service,
    agentTools []tools.BaseTool,
) (Service, error) {
    // Create the LLM provider (Claude, GPT, etc.)
    agentProvider, err := createAgentProvider(agentName)

    agent := &agent{
        Broker:   pubsub.NewBroker[AgentEvent](),
        provider: agentProvider,
        messages: messages,
        sessions: sessions,
        tools:    agentTools,  // All the tools!
    }

    return agent, nil
}
```

### Part 3: Run Method (Lines 198-231)

```go
func (a *agent) Run(ctx context.Context, sessionID string, content string, attachments ...message.Attachment) (<-chan AgentEvent, error) {
    events := make(chan AgentEvent)

    // Create cancellable context
    genCtx, cancel := context.WithCancel(ctx)
    a.activeRequests.Store(sessionID, cancel)

    // Run in goroutine (async)
    go func() {
        // PROCESS THE GENERATION (the loop!)
        result := a.processGeneration(genCtx, sessionID, content, attachmentParts)

        // Cleanup
        a.activeRequests.Delete(sessionID)
        cancel()

        // Publish result
        a.Publish(pubsub.CreatedEvent, result)
        events <- result
        close(events)
    }()

    return events, nil
}
```

### Part 4: THE AGENT LOOP (Lines 233-311) - CRITICAL!

```go
func (a *agent) processGeneration(ctx context.Context, sessionID, content string, attachmentParts []message.ContentPart) AgentEvent {
    // 1. GET EXISTING MESSAGES (conversation history)
    msgs, err := a.messages.List(ctx, sessionID)

    // 2. CREATE USER MESSAGE
    userMsg, err := a.createUserMessage(ctx, sessionID, content, attachmentParts)

    // 3. BUILD MESSAGE HISTORY
    msgHistory := append(msgs, userMsg)

    // 4. THE AGENT LOOP - THIS IS THE KEY!
    for {
        // Check if user cancelled
        select {
        case <-ctx.Done():
            return a.err(ctx.Err())
        default:
            // Continue processing
        }

        // 5. CALL LLM AND EXECUTE TOOLS
        agentMessage, toolResults, err := a.streamAndHandleEvents(
            ctx, sessionID, msgHistory
        )

        // 6. CHECK IF WE NEED TO LOOP
        if agentMessage.FinishReason() == message.FinishReasonToolUse && toolResults != nil {
            // LLM wants to use tools - we have results
            // ADD to message history and LOOP BACK
            msgHistory = append(msgHistory, agentMessage, *toolResults)
            continue  // ← LOOP BACK! Send updated history to LLM
        }

        // 7. NO MORE TOOL CALLS - WE'RE DONE!
        return AgentEvent{
            Type:    AgentEventTypeResponse,
            Message: agentMessage,
            Done:    true,
        }
    }
}
```

### Part 5: Stream and Handle Events (Lines 322-438)

```go
func (a *agent) streamAndHandleEvents(ctx context.Context, sessionID string, msgHistory []message.Message) (message.Message, *message.Message, error) {
    // 1. CALL LLM WITH STREAMING
    eventChan := a.provider.StreamResponse(ctx, msgHistory, a.tools)

    // 2. CREATE ASSISTANT MESSAGE
    assistantMsg, err := a.messages.Create(ctx, sessionID, message.CreateMessageParams{
        Role:  message.Assistant,
        Parts: []message.ContentPart{},
        Model: a.provider.Model().ID,
    })

    // 3. PROCESS STREAMING EVENTS
    for event := range eventChan {
        a.processEvent(ctx, sessionID, &assistantMsg, event)
        // Events: TextDelta, ToolUseStart, ToolUseDelta, ToolUseStop, Complete
    }

    // 4. EXECUTE EACH TOOL CALL
    toolCalls := assistantMsg.ToolCalls()
    toolResults := make([]message.ToolResult, len(toolCalls))

    for i, toolCall := range toolCalls {
        // Find the tool by name
        var tool tools.BaseTool
        for _, availableTool := range a.tools {
            if availableTool.Info().Name == toolCall.Name {
                tool = availableTool
                break
            }
        }

        if tool == nil {
            toolResults[i] = message.ToolResult{
                ToolCallID: toolCall.ID,
                Content:    "Tool not found: " + toolCall.Name,
                IsError:    true,
            }
            continue
        }

        // 5. EXECUTE THE TOOL
        toolResult, toolErr := tool.Run(ctx, tools.ToolCall{
            ID:    toolCall.ID,
            Name:  toolCall.Name,
            Input: toolCall.Input,
        })

        if toolErr != nil {
            if errors.Is(toolErr, permission.ErrorPermissionDenied) {
                toolResults[i] = message.ToolResult{
                    ToolCallID: toolCall.ID,
                    Content:    "Permission denied",
                    IsError:    true,
                }
                continue
            }
        }

        toolResults[i] = message.ToolResult{
            ToolCallID: toolCall.ID,
            Content:    toolResult.Content,
            Metadata:   toolResult.Metadata,
            IsError:    toolResult.IsError,
        }
    }

    // 6. CREATE TOOL RESULTS MESSAGE
    msg, err := a.messages.Create(context.Background(), assistantMsg.SessionID, message.CreateMessageParams{
        Role:  message.Tool,
        Parts: toolResults,
    })

    return assistantMsg, &msg, nil
}
```

### Visual: The Agent Loop Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                         AGENT LOOP                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User: "Fix the bug in auth.py"                                  │
│         ↓                                                        │
│  msgHistory = [user_message]                                     │
│         ↓                                                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ITERATION 1                                                 │ │
│  │  streamAndHandleEvents(ctx, sessionID, msgHistory)          │ │
│  │      ↓                                                       │ │
│  │  provider.StreamResponse() → Call LLM                       │ │
│  │      ↓                                                       │ │
│  │  LLM returns: "I'll read the file"                          │ │
│  │              + ToolCall: view(file_path="auth.py")          │ │
│  │      ↓                                                       │ │
│  │  Execute tool: view("auth.py") → Returns file contents      │ │
│  │      ↓                                                       │ │
│  │  FinishReason = ToolUse → LOOP BACK!                        │ │
│  │      ↓                                                       │ │
│  │  msgHistory = [user, assistant+tool_call, tool_result]      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│         ↓                                                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ITERATION 2                                                 │ │
│  │  streamAndHandleEvents(ctx, sessionID, msgHistory)          │ │
│  │      ↓                                                       │ │
│  │  LLM now SEES the file contents from previous iteration     │ │
│  │      ↓                                                       │ │
│  │  LLM returns: "Found the bug, fixing..."                    │ │
│  │              + ToolCall: edit(file, old, new)               │ │
│  │      ↓                                                       │ │
│  │  Execute tool: edit() → File modified                       │ │
│  │      ↓                                                       │ │
│  │  FinishReason = ToolUse → LOOP BACK!                        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│         ↓                                                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ITERATION 3                                                 │ │
│  │  streamAndHandleEvents(ctx, sessionID, msgHistory)          │ │
│  │      ↓                                                       │ │
│  │  LLM returns: "Bug fixed successfully!"                     │ │
│  │              (No tool calls)                                 │ │
│  │      ↓                                                       │ │
│  │  FinishReason = EndTurn → EXIT LOOP! ✓                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│         ↓                                                        │
│  Return AgentEvent{Message: "Bug fixed!", Done: true}           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

# 6. LAYER 5: TOOLS SYSTEM (internal/llm/tools/)

## File: `internal/llm/agent/tools.go` - Tool Registration

```go
func CoderAgentTools(
    permissions permission.Service,
    sessions session.Service,
    messages message.Service,
    history history.Service,
    lspClients map[string]*lsp.Client,
) []tools.BaseTool {
    // Get MCP tools from external servers
    otherTools := GetMcpTools(ctx, permissions)

    // Add LSP diagnostics if available
    if len(lspClients) > 0 {
        otherTools = append(otherTools, tools.NewDiagnosticsTool(lspClients))
    }

    // Return ALL tools
    return append(
        []tools.BaseTool{
            tools.NewBashTool(permissions),      // Shell commands
            tools.NewEditTool(...),              // Edit files
            tools.NewFetchTool(permissions),     // Fetch URLs
            tools.NewGlobTool(),                 // Find files
            tools.NewGrepTool(),                 // Search content
            tools.NewLsTool(),                   // List directories
            tools.NewSourcegraphTool(),          // Search public code
            tools.NewViewTool(lspClients),       // Read files
            tools.NewPatchTool(...),             // Apply patches
            tools.NewWriteTool(...),             // Write files
            NewAgentTool(...),                   // Sub-agent for complex searches
        },
        otherTools...,  // MCP tools + LSP diagnostics
    )
}
```

## File: `internal/llm/tools/tools.go` - Base Interface

```go
// Every tool must implement this interface
type BaseTool interface {
    Info() ToolInfo                                   // Tool metadata
    Run(ctx context.Context, params ToolCall) (ToolResponse, error)  // Execute
}

type ToolInfo struct {
    Name        string             // "bash", "edit", "view", etc.
    Description string             // Tells LLM when to use this tool
    Parameters  map[string]any     // JSON schema for parameters
    Required    []string           // Required parameter names
}

type ToolCall struct {
    ID    string  // Unique ID from LLM
    Name  string  // Tool name
    Input string  // JSON parameters
}

type ToolResponse struct {
    Type     string  // "text" or "image"
    Content  string  // The result
    Metadata string  // Optional metadata (JSON)
    IsError  bool    // True if error occurred
}
```

## Tool Implementation Examples

### 1. Bash Tool (`internal/llm/tools/bash.go`)

```go
type bashTool struct {
    permissions permission.Service
}

func (b *bashTool) Info() ToolInfo {
    return ToolInfo{
        Name: "bash",
        Description: "Execute shell commands. Use for git, npm, python, etc.",
        Parameters: map[string]any{
            "command": map[string]any{
                "type":        "string",
                "description": "The shell command to execute",
            },
            "timeout": map[string]any{
                "type":        "integer",
                "description": "Timeout in milliseconds (default 120000)",
            },
        },
        Required: []string{"command"},
    }
}

func (b *bashTool) Run(ctx context.Context, call ToolCall) (ToolResponse, error) {
    // 1. Parse parameters
    var params struct {
        Command string `json:"command"`
        Timeout int    `json:"timeout"`
    }
    json.Unmarshal([]byte(call.Input), &params)

    // 2. Check for banned commands
    banned := []string{"curl", "wget", "nc", "telnet"}
    for _, cmd := range banned {
        if strings.Contains(params.Command, cmd) {
            return NewTextErrorResponse("Command not allowed: " + cmd), nil
        }
    }

    // 3. Request permission (may block waiting for user)
    approved := b.permissions.Request(permission.PermissionRequest{
        ToolName:    "bash",
        Description: params.Command,
        Action:      "execute",
    })
    if !approved {
        return ToolResponse{}, permission.ErrorPermissionDenied
    }

    // 4. Execute command
    cmd := exec.Command("bash", "-c", params.Command)
    output, _ := cmd.CombinedOutput()

    // 5. Truncate if too long
    if len(output) > 30000 {
        output = append(output[:30000], []byte("\n... (truncated)")...)
    }

    return NewTextResponse(string(output)), nil
}
```

### 2. View Tool (`internal/llm/tools/view.go`)

```go
func (v *viewTool) Run(ctx context.Context, call ToolCall) (ToolResponse, error) {
    // 1. Parse parameters
    var params struct {
        FilePath string `json:"file_path"`
        Offset   int    `json:"offset"`
        Limit    int    `json:"limit"`
    }
    json.Unmarshal([]byte(call.Input), &params)

    if params.Limit == 0 {
        params.Limit = 2000  // Default
    }

    // 2. Validate path
    if !filepath.IsAbs(params.FilePath) {
        params.FilePath = filepath.Join(config.WorkingDirectory(), params.FilePath)
    }

    // 3. Read file
    file, err := os.Open(params.FilePath)
    if err != nil {
        return NewTextErrorResponse("Cannot open file: " + err.Error()), nil
    }
    defer file.Close()

    // 4. Read lines with offset and limit
    scanner := bufio.NewScanner(file)
    var lines []string
    lineNum := 0

    for scanner.Scan() {
        lineNum++
        if lineNum <= params.Offset {
            continue
        }
        if len(lines) >= params.Limit {
            break
        }

        line := scanner.Text()
        // Truncate long lines
        if len(line) > 2000 {
            line = line[:2000] + "..."
        }
        // Format: "   42→content here"
        lines = append(lines, fmt.Sprintf("%5d→%s", lineNum, line))
    }

    return NewTextResponse(strings.Join(lines, "\n")), nil
}
```

### 3. Edit Tool (`internal/llm/tools/edit.go`)

```go
func (e *editTool) Run(ctx context.Context, call ToolCall) (ToolResponse, error) {
    // 1. Parse parameters
    var params struct {
        FilePath  string `json:"file_path"`
        OldString string `json:"old_string"`
        NewString string `json:"new_string"`
    }
    json.Unmarshal([]byte(call.Input), &params)

    // 2. Request permission
    approved := e.permissions.Request(permission.PermissionRequest{
        ToolName:    "edit",
        Path:        params.FilePath,
        Description: "Edit file",
        Action:      "write",
    })
    if !approved {
        return ToolResponse{}, permission.ErrorPermissionDenied
    }

    // 3. Read current content
    content, err := os.ReadFile(params.FilePath)
    if err != nil {
        return NewTextErrorResponse("Cannot read file: " + err.Error()), nil
    }

    // 4. Check if old_string exists
    if !strings.Contains(string(content), params.OldString) {
        return NewTextErrorResponse("old_string not found in file"), nil
    }

    // 5. Replace (only FIRST occurrence)
    newContent := strings.Replace(string(content), params.OldString, params.NewString, 1)

    // 6. Write file
    err = os.WriteFile(params.FilePath, []byte(newContent), 0644)
    if err != nil {
        return NewTextErrorResponse("Cannot write file: " + err.Error()), nil
    }

    // 7. Track in history
    e.history.RecordEdit(params.FilePath, newContent)

    // 8. Generate diff for response
    diff := generateDiff(string(content), newContent)

    return NewTextResponse("File edited:\n" + diff), nil
}
```

### Tool Files Summary

| File | Tool Name | Purpose | Needs Permission |
|------|-----------|---------|------------------|
| `bash.go` | bash | Execute shell commands | Yes |
| `view.go` | view | Read file contents | No |
| `edit.go` | edit | Replace text in file | Yes |
| `write.go` | write | Write/create file | Yes |
| `glob.go` | glob | Find files by pattern | No |
| `grep.go` | grep | Search file contents | No |
| `ls.go` | ls | List directory contents | No |
| `patch.go` | patch | Apply unified diff patch | Yes |
| `fetch.go` | fetch | Download from URL | Yes |
| `diagnostics.go` | diagnostics | Get LSP errors | No |
| `sourcegraph.go` | sourcegraph | Search public code | No |
| `agent-tool.go` | agent | Spawn sub-agent | No |

---

# 7. LAYER 6: LLM PROVIDERS (internal/llm/provider/)

## File: `internal/llm/provider/provider.go`

```go
// Provider interface - all LLM providers implement this
type Provider interface {
    // Send messages and get response (blocking)
    SendMessages(ctx context.Context, messages []message.Message, tools []tools.BaseTool) (*ProviderResponse, error)

    // Send messages and get streaming response
    StreamResponse(ctx context.Context, messages []message.Message, tools []tools.BaseTool) <-chan ProviderEvent

    // Get the model info
    Model() models.Model
}

// Create provider based on name
func NewProvider(providerName ModelProvider, opts ...ProviderClientOption) (Provider, error) {
    switch providerName {
    case models.ProviderAnthropic:
        return &anthropicProvider{...}, nil
    case models.ProviderOpenAI:
        return &openaiProvider{...}, nil
    case models.ProviderGemini:
        return &geminiProvider{...}, nil
    case models.ProviderBedrock:
        return &bedrockProvider{...}, nil
    case models.ProviderCopilot:
        return &copilotProvider{...}, nil
    // ... more providers
    }
}
```

### Supported Providers

| Provider | File | Models |
|----------|------|--------|
| Anthropic | `anthropic.go` | Claude 3.5, Claude 4 |
| OpenAI | `openai.go` | GPT-4, GPT-4o, O1, O3 |
| Google | `gemini.go` | Gemini 2.5 |
| AWS | `bedrock.go` | Claude via Bedrock |
| GitHub | `copilot.go` | Copilot models |
| Azure | `azure.go` | Azure OpenAI |
| Groq | Uses `openai.go` | Llama models |

---

# 8. LAYER 7: SYSTEM PROMPTS (internal/llm/prompt/)

## File: `internal/llm/prompt/coder.go`

```go
func CoderPrompt(provider models.ModelProvider) string {
    basePrompt := baseAnthropicCoderPrompt
    switch provider {
    case models.ProviderOpenAI:
        basePrompt = baseOpenAICoderPrompt
    }
    envInfo := getEnvironmentInfo()

    return fmt.Sprintf("%s\n\n%s\n%s", basePrompt, envInfo, lspInformation())
}
```

### Anthropic System Prompt (Key Parts)

```
You are OpenCode, an interactive CLI tool that helps users with software engineering tasks.

# Memory
If OpenCode.md exists in working directory, it contains:
1. Frequently used bash commands (build, test, lint)
2. Code style preferences
3. Useful codebase information

# Tone and Style
- Be concise, direct, to the point
- MUST answer with fewer than 4 lines unless user asks for detail
- One word answers are best
- Avoid unnecessary preamble/postamble

# Proactiveness
- Only do what the user asks
- Don't surprise users with unexpected actions

# Following Conventions
- First understand file's code conventions
- NEVER assume a library is available
- Check neighboring files for patterns
- Follow security best practices

# Tool Usage Policy
- Prefer Agent tool for file searching (reduces context)
- Make parallel tool calls when no dependencies
```

### Environment Info Added to Prompt

```go
func getEnvironmentInfo() string {
    return fmt.Sprintf(`
<env>
Working directory: %s
Is directory a git repo: %s
Platform: %s
Today's date: %s
</env>
<project>
%s
</project>
    `, cwd, isGitRepo, platform, date, lsOutput)
}
```

---

# 9. LAYER 8: DATA STORAGE (internal/db, session, message)

## Database Schema (`internal/db/migrations/`)

```sql
-- Sessions table
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    parent_session_id TEXT,
    title TEXT NOT NULL,
    message_count INTEGER NOT NULL DEFAULT 0,
    prompt_tokens INTEGER NOT NULL DEFAULT 0,
    completion_tokens INTEGER NOT NULL DEFAULT 0,
    cost REAL NOT NULL DEFAULT 0.0,
    updated_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL
);

-- Messages table
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,           -- "user", "assistant", "tool"
    parts TEXT NOT NULL,          -- JSON array
    model TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    finished_at INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- File history for rollback
CREATE TABLE files (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    path TEXT NOT NULL,
    content TEXT NOT NULL,
    version TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
```

## Session Service (`internal/session/session.go`)

```go
type Session struct {
    ID               string
    ParentSessionID  string
    Title            string
    MessageCount     int64
    PromptTokens     int64
    CompletionTokens int64
    Cost             float64
    SummaryMessageID string
    CreatedAt        int64
    UpdatedAt        int64
}

type Service interface {
    Create(ctx, title) (Session, error)
    Get(ctx, id) (Session, error)
    List(ctx) ([]Session, error)
    Save(ctx, session) (Session, error)
    Delete(ctx, id) error
    Subscribe(ctx) <-chan pubsub.Event[Session]
}
```

## Message Service (`internal/message/message.go`)

```go
type Message struct {
    ID        string
    SessionID string
    Role      MessageRole  // User, Assistant, Tool
    Parts     []ContentPart
    Model     ModelID
    CreatedAt int64
    UpdatedAt int64
}

// Content part types
type TextContent struct{ Text string }
type ToolCall struct{ ID, Name, Input string }
type ToolResult struct{ ToolCallID, Content string; IsError bool }
type Finish struct{ Reason string; Time int64 }
```

---

# 10. LAYER 9: PERMISSION SYSTEM (internal/permission/)

## File: `internal/permission/permission.go`

```go
type PermissionRequest struct {
    ID          string
    SessionID   string
    ToolName    string  // "bash", "edit", "write"
    Description string  // What the tool wants to do
    Action      string  // "read", "write", "execute"
    Path        string  // File/directory path
}

type permissionService struct {
    sessionPermissions  []PermissionRequest  // Already approved
    pendingRequests     sync.Map             // Waiting for user
    autoApproveSessions []string             // Auto-approve for non-interactive
}

func (s *permissionService) Request(req PermissionRequest) bool {
    // 1. Check if auto-approved session
    if slices.Contains(s.autoApproveSessions, req.SessionID) {
        return true
    }

    // 2. Check if already approved this session
    for _, p := range s.sessionPermissions {
        if p.ToolName == req.ToolName && p.Path == req.Path {
            return true
        }
    }

    // 3. Publish event to TUI
    s.Publish(pubsub.CreatedEvent, req)

    // 4. Create response channel and wait
    respCh := make(chan bool, 1)
    s.pendingRequests.Store(req.ID, respCh)
    defer s.pendingRequests.Delete(req.ID)

    // 5. BLOCK until user responds
    return <-respCh
}

func (s *permissionService) Grant(req PermissionRequest) {
    // Called when user approves in TUI
    respCh, ok := s.pendingRequests.Load(req.ID)
    if ok {
        respCh.(chan bool) <- true
    }
}
```

### Permission Flow Diagram

```
Tool.Run()
    │
    ├──→ permission.Request()
    │        │
    │        ├──→ Check auto-approve? → Yes → return true
    │        │
    │        ├──→ Check already approved? → Yes → return true
    │        │
    │        ├──→ Publish event to TUI
    │        │
    │        ├──→ Create response channel
    │        │
    │        └──→ BLOCK on channel ←─────────────────────┐
    │                                                     │
    │    TUI shows: "Allow bash: rm -rf /tmp? [Y/N]"     │
    │                   │                                 │
    │                   └──→ User presses Y              │
    │                           │                         │
    │                           └──→ permission.Grant()  │
    │                                    │                │
    │                                    └──→ Send true ──┘
    │
    └──→ Tool continues execution
```

---

# 11. LAYER 10: TERMINAL UI (internal/tui/)

## File: `internal/tui/tui.go`

OpenCode uses [Bubble Tea](https://github.com/charmbracelet/bubbletea), a Go TUI framework.

```go
type appModel struct {
    width, height   int
    currentPage     page.PageID
    pages           map[page.PageID]tea.Model

    // Dialogs
    showPermissions bool
    permissions     dialog.PermissionDialogCmp

    showHelp        bool
    help            dialog.HelpCmp

    showSessionDialog bool
    sessionDialog     dialog.SessionDialog
}

// Bubble Tea lifecycle methods
func (a appModel) Init() tea.Cmd { ... }
func (a appModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) { ... }
func (a appModel) View() string { ... }
```

### TUI Event Subscriptions

```go
// In cmd/root.go
setupSubscriber(ctx, &wg, "logging", logging.Subscribe, ch)
setupSubscriber(ctx, &wg, "sessions", app.Sessions.Subscribe, ch)
setupSubscriber(ctx, &wg, "messages", app.Messages.Subscribe, ch)
setupSubscriber(ctx, &wg, "permissions", app.Permissions.Subscribe, ch)
setupSubscriber(ctx, &wg, "coderAgent", app.CoderAgent.Subscribe, ch)
```

These send events from services → TUI for real-time updates.

---

# 12. COMPLETE EXECUTION TRACE

Let's trace `opencode -p "Fix the bug in auth.py"`:

```
1. main.go:13
   └── cmd.Execute()

2. cmd/root.go:285
   └── rootCmd.Execute()

3. cmd/root.go:49 (rootCmd.RunE)
   ├── config.Load(".", false)
   ├── db.Connect()
   └── app.New(ctx, conn)
       │
       └── internal/app/app.go:42
           ├── session.NewService(q)
           ├── message.NewService(q)
           └── agent.NewAgent(
               │   config.AgentCoder,
               │   sessions, messages,
               │   agent.CoderAgentTools(...)
               │)
               │
               └── internal/llm/agent/agent.go:73
                   ├── createAgentProvider(config.AgentCoder)
                   │   └── provider.NewProvider(ProviderAnthropic, ...)
                   └── return &agent{tools: agentTools, provider: ...}

4. cmd/root.go:114 (Non-interactive mode)
   └── app.RunNonInteractive(ctx, "Fix the bug in auth.py", "text", false)
       │
       └── internal/app/app.go:100
           ├── a.Sessions.Create(ctx, "Non-interactive: Fix...")
           ├── a.Permissions.AutoApproveSession(sess.ID)
           └── a.CoderAgent.Run(ctx, sess.ID, "Fix the bug in auth.py")
               │
               └── internal/llm/agent/agent.go:198
                   └── go func() {
                       │   result := a.processGeneration(...)
                       │}
                       │
                       └── internal/llm/agent/agent.go:233
                           └── THE AGENT LOOP:
                               │
                               │ ITERATION 1:
                               ├── a.streamAndHandleEvents(ctx, sessionID, msgHistory)
                               │   ├── a.provider.StreamResponse(ctx, msgs, tools)
                               │   │   └── Call Claude API (streaming)
                               │   │       Response: "I'll read auth.py first"
                               │   │                 ToolCall: view(file_path="auth.py")
                               │   │
                               │   └── Execute tool:
                               │       └── viewTool.Run(ctx, {Name:"view", Input:`{"file_path":"auth.py"}`})
                               │           └── Returns: "    1→def login(user):\n    2→..."
                               │
                               ├── FinishReason = ToolUse → continue
                               │
                               │ ITERATION 2:
                               ├── a.streamAndHandleEvents(ctx, sessionID, msgHistory)
                               │   ├── a.provider.StreamResponse(ctx, msgs, tools)
                               │   │   └── Claude now sees file contents
                               │   │       Response: "Found bug on line 15, fixing..."
                               │   │                 ToolCall: edit(file_path="auth.py", old_string="...", new_string="...")
                               │   │
                               │   └── Execute tool:
                               │       └── editTool.Run(ctx, {Name:"edit", Input:`{...}`})
                               │           ├── permissions.Request() → Auto-approved
                               │           ├── Read file, replace text, write file
                               │           └── Returns: "File edited successfully"
                               │
                               ├── FinishReason = ToolUse → continue
                               │
                               │ ITERATION 3:
                               ├── a.streamAndHandleEvents(ctx, sessionID, msgHistory)
                               │   └── a.provider.StreamResponse(ctx, msgs, tools)
                               │       └── Response: "Bug fixed! Changed line 15..."
                               │                     (No tool calls)
                               │
                               └── FinishReason = EndTurn → EXIT LOOP
                                   └── return AgentEvent{Message: "Bug fixed!", Done: true}

5. Back in app.go:136
   └── result := <-done
   └── fmt.Println(result.Message.Content())
       Output: "Bug fixed! Changed line 15..."
```

---

# 13. FUNCTION CALL GRAPH

```
main()
└── cmd.Execute()
    └── rootCmd.Execute()
        └── rootCmd.RunE()
            ├── config.Load()
            ├── db.Connect()
            ├── app.New()
            │   ├── session.NewService()
            │   ├── message.NewService()
            │   ├── history.NewService()
            │   ├── permission.NewPermissionService()
            │   └── agent.NewAgent()
            │       ├── createAgentProvider()
            │       │   └── provider.NewProvider()
            │       └── CoderAgentTools()
            │           ├── tools.NewBashTool()
            │           ├── tools.NewEditTool()
            │           ├── tools.NewViewTool()
            │           ├── tools.NewWriteTool()
            │           ├── tools.NewGlobTool()
            │           ├── tools.NewGrepTool()
            │           ├── tools.NewLsTool()
            │           ├── tools.NewPatchTool()
            │           ├── tools.NewFetchTool()
            │           ├── tools.NewSourcegraphTool()
            │           ├── NewAgentTool()
            │           └── GetMcpTools()
            │
            ├── initMCPTools()
            │   └── agent.GetMcpTools()
            │
            └── app.RunNonInteractive() OR tui.New().Run()
                │
                └── app.CoderAgent.Run()
                    └── agent.processGeneration()
                        └── FOR LOOP:
                            └── agent.streamAndHandleEvents()
                                ├── provider.StreamResponse()
                                │   └── anthropicClient.stream()
                                │       └── Call Claude API
                                │
                                └── FOR each toolCall:
                                    └── tool.Run()
                                        ├── bashTool.Run()
                                        │   ├── permissions.Request()
                                        │   └── exec.Command()
                                        │
                                        ├── viewTool.Run()
                                        │   └── os.Open() + scanner.Scan()
                                        │
                                        ├── editTool.Run()
                                        │   ├── permissions.Request()
                                        │   ├── os.ReadFile()
                                        │   ├── strings.Replace()
                                        │   └── os.WriteFile()
                                        │
                                        └── ... other tools
```

---

# SUMMARY

## Key Concepts

1. **Entry Point** (`main.go`) → Just calls `cmd.Execute()`
2. **CLI Framework** (`cmd/root.go`) → Parses flags, loads config, creates App
3. **Application Core** (`internal/app/app.go`) → Creates services and agent
4. **Agent Loop** (`internal/llm/agent/agent.go`) → THE HEART: calls LLM, executes tools, loops
5. **Tools** (`internal/llm/tools/*.go`) → Each tool implements `Info()` and `Run()`
6. **Providers** (`internal/llm/provider/*.go`) → Abstract different LLM APIs
7. **Prompts** (`internal/llm/prompt/*.go`) → System instructions for LLM
8. **Storage** (`internal/db/`, `session/`, `message/`) → SQLite persistence
9. **Permissions** (`internal/permission/`) → Gate dangerous operations
10. **TUI** (`internal/tui/`) → Bubble Tea terminal interface

## The Agent Loop in One Sentence

```
while LLM returns tool calls:
    execute each tool → append results to history → call LLM again
return final response
```

## Why This Makes It "Agentic"

- **Autonomous**: LLM decides which tools to use
- **Iterative**: Keeps going until task complete
- **Context-Aware**: Sees results of previous actions
- **Goal-Oriented**: Works toward completing user's request

---

**Document Version**: 1.0
**Last Updated**: January 2026
**Repository**: https://github.com/opencode-ai/opencode (archived)
