# OpenCode Analysis - Complete Technical Guide

**From zero knowledge to expert understanding** - Learn how the OpenCode AI coding agent works internally with actual code references.

---

## 🎯 What is OpenCode?

OpenCode is an AI coding assistant controlled by **system prompts** (text files). Everything the AI does is defined by code:
- System prompts guide decisions
- 19 tools provide actions
- 6 agents provide modes
- Session processor orchestrates everything

**Core principle:** Everything is controlled by prompts + code!

---

## 📖 Choose Your Learning Path

### 🎓 Path 1: Beginner (90 min) - Understand Concepts

**Read these in order:**

1. **[01-prompts-explained.md](01-prompts-explained.md)** (15 min)
   - What are prompts? (with analogies)
   - How prompts control AI behavior
   - Real examples

2. **[02-tool-triggers.md](02-tool-triggers.md)** (20 min)
   - When AI uses Glob vs Grep vs Read
   - Decision trees for all 19 tools
   - Trigger patterns

3. **[03-task-breakdown.md](03-task-breakdown.md)** (15 min)
   - How "add auth" becomes 20 steps
   - TodoWrite and task management
   - Decomposition strategies

4. **[04-agent-system.md](04-agent-system.md)** (20 min)
   - 6 agent types (BUILD, PLAN, EXPLORE)
   - Permissions and capabilities
   - When each is used

5. **[07-actual-prompts.md](07-actual-prompts.md)** (30 min)
   - Real prompt files explained
   - Claude vs GPT vs Gemini
   - How prompts combine

**Result:** Solid conceptual understanding

---

### 💻 Path 2: Deep Dive (120 min) - See The Code

**Technical deep dive with code references:**

1. **[05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md)** (45 min)
   - **Complete code flow** from input to response
   - **Actual TypeScript code** from OpenCode
   - **Visual flow charts** with code references
   - **Step-by-step execution** through the codebase
   - Session processor internals
   - Tool execution lifecycle
   - Permission checking flow

   **📍 Code locations:**
   - `packages/opencode/src/session/processor.ts`
   - `packages/opencode/src/session/llm.ts`
   - `packages/opencode/src/session/system.ts`

2. **[06-tool-construction-guide.md](06-tool-construction-guide.md)** (45 min)
   - **How tools are built** with real code
   - **Complete tool examples** (Read, Grep, Question)
   - **Tool architecture** and interfaces
   - **Build your own tool** guide
   - Tool registration system

   **📍 Code locations:**
   - `packages/opencode/src/tool/tool.ts`
   - `packages/opencode/src/tool/registry.ts`
   - `packages/opencode/src/tool/*.ts`

3. **[ALL-PROMPTS-REFERENCE.md](ALL-PROMPTS-REFERENCE.md)** (30 min)
   - All 8 system prompts documented
   - Code references for each
   - Comparison tables

**Result:** Complete technical understanding + can build custom tools

---

### ⚡ Path 3: Quick Reference (30 min)

**For experienced developers:**

1. [05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md) - Flow charts + code
2. [06-tool-construction-guide.md](06-tool-construction-guide.md) - Tool examples
3. [TOOLS-INDEX.md](TOOLS-INDEX.md) - All 19 tools reference

**Result:** Fast lookup and code navigation

---

## 🎬 Quick Example with Code References

```
User: "Fix the bug in login.ts"
    ↓
CLI (run.ts:42)
    session = await Session.create()
    agent = await Agent.get("build")
    ↓
System Prompt Builder (system.ts:15)
    prompt = readFile("session/prompt/anthropic.txt")
    prompt += agent.prompt
    prompt += userInstructions
    ↓
LLM Stream (llm.ts:33)
    result = await streamText({ system: prompt, ... })
    ↓
Session Processor (processor.ts:50)
    for await (part of stream) {
      if (part.type === 'tool-call') {
        result = await executeTool(part)
      }
    }
    ↓
Tool Execution (read.ts:25)
    await ctx.ask({ permission: "read", patterns: [file] })
    content = await fs.readFile(file)
    return { output: content }
    ↓
Back to LLM with result → AI responds
```

**Every decision traceable to actual code!**

---

## 📚 Complete Documentation

### Beginner Guides (Concepts)
- **[01-prompts-explained.md](01-prompts-explained.md)** - What prompts are
- **[02-tool-triggers.md](02-tool-triggers.md)** - When tools are used
- **[03-task-breakdown.md](03-task-breakdown.md)** - Task decomposition
- **[04-agent-system.md](04-agent-system.md)** - Agent types
- **[07-actual-prompts.md](07-actual-prompts.md)** - Real prompt files

### Deep Dive (Code)
- **[05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md)** - Complete code flow
- **[06-tool-construction-guide.md](06-tool-construction-guide.md)** - Build tools

### Reference (Lookup)
- **[ALL-PROMPTS-REFERENCE.md](ALL-PROMPTS-REFERENCE.md)** - All 8 prompts
- **[TOOLS-INDEX.md](TOOLS-INDEX.md)** - All 19 tools

---

## ✅ What's Documented

**8 System Prompts** (with code references)
- anthropic.txt, beast.txt, gemini.txt
- explore.txt, plan.txt, compaction.txt
- title.txt, agent-generator.txt
- All from: `packages/opencode/src/session/prompt/*.txt`

**19 Built-in Tools** (with code examples)
- Search: Glob, Grep, CodeSearch
- Files: Read, Edit, Write
- Execution: Bash, Task
- Management: TodoRead, TodoWrite
- All from: `packages/opencode/src/tool/*.ts`

**6 Agent Types** (with permissions)
- BUILD, PLAN, EXPLORE, GENERAL, COMPACTION, TITLE
- From: `packages/opencode/src/agent/agent.ts`

**Complete Execution Flow** (with flow charts)
- Session processor main loop
- Tool execution lifecycle
- Permission checking
- Doom loop detection
- From: `packages/opencode/src/session/processor.ts`

---

## 🔍 Quick Answers

**Q: How does AI know to use Glob vs Grep?**
A: System prompt says "Glob for file names, Grep for content"
→ [02-tool-triggers.md](02-tool-triggers.md)

**Q: Can I see the actual code flow?**
A: Yes! Complete with code references
→ [05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md)

**Q: How are tools built?**
A: With Tool.Info interface, shown with real examples
→ [06-tool-construction-guide.md](06-tool-construction-guide.md)

**Q: Where is the main execution loop?**
A: `packages/opencode/src/session/processor.ts`
→ [05-execution-flow-deep-dive.md#step-4-session-processor](05-execution-flow-deep-dive.md)

**Q: How do I build my own tool?**
A: Follow the template in 06-tool-construction-guide.md
→ [06-tool-construction-guide.md#creating-your-own-tool](06-tool-construction-guide.md)

---

## 📂 Simple Structure

```
opencode analysis/
├── README.md (start here!)
│
├── Beginner Guides (concepts)
│   ├── 01-prompts-explained.md
│   ├── 02-tool-triggers.md
│   ├── 03-task-breakdown.md
│   ├── 04-agent-system.md
│   └── 07-actual-prompts.md
│
├── Deep Dive (code + flow charts)
│   ├── 05-execution-flow-deep-dive.md    ⭐ NEW!
│   └── 06-tool-construction-guide.md     ⭐ NEW!
│
└── Reference (quick lookup)
    ├── ALL-PROMPTS-REFERENCE.md
    └── TOOLS-INDEX.md
```

**10 files total. No folders. Maximum clarity.**

---

## 🔑 Key Features

✅ **ACTUAL PROMPTS** - Complete, unmodified prompt files from OpenCode
- [07-actual-prompts.md](07-actual-prompts.md) - EXACT anthropic.txt, beast.txt, gemini.txt, plan.txt, explore.txt

✅ **ACTUAL AGENT CODE** - Real TypeScript from agent.ts
- [04-agent-system.md](04-agent-system.md) - All 6 agents with actual TypeScript implementation

✅ **Simplified Educational Examples** - For understanding concepts
- [05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md) - Simplified processor flow ⚠️
- [06-tool-construction-guide.md](06-tool-construction-guide.md) - Simplified tool examples ⚠️

✅ **Direct Code References** - Every concept links to actual OpenCode files

✅ **Beginner + Expert paths** - Choose your depth level

✅ **Complete coverage** - All prompts, tools, agents, flow

---

## 🚀 Get Started

### For Beginners:
1. Read [01-prompts-explained.md](01-prompts-explained.md) (15 min)
2. Read [02-tool-triggers.md](02-tool-triggers.md) (20 min)
3. Read [07-actual-prompts.md](07-actual-prompts.md) (30 min)

### For Developers:
1. Read [05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md) (45 min)
2. Read [06-tool-construction-guide.md](06-tool-construction-guide.md) (45 min)
3. Build your own tool!

### For Quick Lookup:
- [TOOLS-INDEX.md](TOOLS-INDEX.md) - All tools
- [ALL-PROMPTS-REFERENCE.md](ALL-PROMPTS-REFERENCE.md) - All prompts
- [05-execution-flow-deep-dive.md](05-execution-flow-deep-dive.md) - Code locations

---

## 📊 Documentation Coverage

| Topic | Beginner Docs | Deep Dive Docs | Code References |
|-------|---------------|----------------|-----------------|
| **Prompts** | 01, 07 | ALL-PROMPTS-REFERENCE | `src/session/prompt/*.txt` |
| **Tools** | 02 | 06, TOOLS-INDEX | `src/tool/*.ts` |
| **Agents** | 04 | 05 | `src/agent/agent.ts` |
| **Flow** | 03 | 05 | `src/session/processor.ts` |
| **Total** | 5 files | 5 files | All code linked |

---

## 🔗 Code References

**Main OpenCode Repository:**
https://github.com/anomalyco/opencode

**Key Files Referenced:**
- Session processor: `packages/opencode/src/session/processor.ts`
- System prompts: `packages/opencode/src/session/prompt/*.txt`
- Tool definitions: `packages/opencode/src/tool/*.ts`
- Agent system: `packages/opencode/src/agent/agent.ts`
- Permission system: `packages/opencode/src/permission/next.ts`
- LLM streaming: `packages/opencode/src/session/llm.ts`

---

## 📝 Key Takeaways

✅ **Complete code traceability** - Every concept links to actual code

✅ **Visual flow charts** - Understand execution visually

✅ **Real examples** - Actual TypeScript from OpenCode

✅ **Build your own** - Tools, agents, customizations

✅ **Beginner friendly** - Start simple, go deep when ready

✅ **Zero missing pieces** - Complete system documented

---

**Created:** January 26, 2026
**Purpose:** Complete technical guide to OpenCode internals
**Audience:** Zero foundation → Build custom tools
**Method:** Concepts + Code + Flow charts
