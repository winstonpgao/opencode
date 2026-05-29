# Claude Code & OpenCode Documentation Hub

This folder contains comprehensive documentation for understanding how AI coding assistants work, including Claude Code and OpenCode.

---

## Documents Index

### Beginner Guides (Start Here)

| File | Size | Description |
|------|------|-------------|
| [QUICKSTART.md](./QUICKSTART.md) | 5KB | **INSTALL & USE** - How to install and use OpenCode |
| [BEGINNER_GUIDE.md](./BEGINNER_GUIDE.md) | 15KB | **CONCEPTS** - Explains everything like you're 10 years old |
| [GLOSSARY.md](./GLOSSARY.md) | 12KB | **GLOSSARY** - All technical terms explained for beginners |
| [04_CLAUDE_CODE_TOOLS_AND_ARCHITECTURE.md](./04_CLAUDE_CODE_TOOLS_AND_ARCHITECTURE.md) | 23KB | Claude Code tools, skills, and comparison with AgentCore |

### Complete Guides (Deep Dives)

| File | Size | Description |
|------|------|-------------|
| [05_CLAUDE_CODE_AND_OPENCODE_COMPLETE_GUIDE.md](./05_CLAUDE_CODE_AND_OPENCODE_COMPLETE_GUIDE.md) | 59KB | **COMPREHENSIVE** - Everything about Claude Code & OpenCode |
| [07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md](./07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md) | 45KB | **CURRENT** - TypeScript codebase walkthrough (current version) |
| [06_OPENCODE_BEGINNER_WALKTHROUGH.md](./06_OPENCODE_BEGINNER_WALKTHROUGH.md) | 70KB | *(OLD Go version)* - Historical reference only |

### Reference Docs

| File | Size | Description |
|------|------|-------------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 9KB | System architecture diagrams and explanations |
| [TOOLS_COMPARISON.md](./TOOLS_COMPARISON.md) | 4KB | Side-by-side tool comparison: OpenCode vs Claude Code |

---

## Reading Order

### If you're completely new (no coding knowledge):
```
1. QUICKSTART.md               <- Install and basic usage
2. BEGINNER_GUIDE.md           <- Simple explanations of concepts
3. GLOSSARY.md                 <- Look up any term you don't understand
4. 04_CLAUDE_CODE_TOOLS...md   <- Tools explained with examples
```

### If you know some programming:
```
1. 05_CLAUDE_CODE_AND_OPENCODE_COMPLETE_GUIDE.md  <- Comprehensive overview
2. 07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md          <- Code-level details (CURRENT)
3. TOOLS_COMPARISON.md                             <- Reference
```

### If you want to understand the source code:
```
1. 07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md  <- Line-by-line explanation
2. GLOSSARY.md                             <- Reference for terms
3. Then explore: packages/opencode/src/
```

> ⚠️ **Note**: `06_OPENCODE_BEGINNER_WALKTHROUGH.md` documents an older Go version of OpenCode.
> For the current TypeScript codebase, use `07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md` instead.

---

## What Each Document Covers

### QUICKSTART.md
- Installation (Bun, npm)
- API key setup
- Basic commands
- Common workflows
- Tips and troubleshooting

### BEGINNER_GUIDE.md
- What is a terminal?
- What is OpenCode/Claude Code?
- All 10 tools explained simply
- How the AI uses tools (with diagrams)
- Learning path for beginners

### 04_CLAUDE_CODE_TOOLS_AND_ARCHITECTURE.md
- Complete list of Claude Code tools
- What are Skills vs Tools?
- Comparison with AWS AgentCore
- Q&A about common questions

### 05_CLAUDE_CODE_AND_OPENCODE_COMPLETE_GUIDE.md
- Definition of coding agents
- Claude Code architecture
- OpenCode directory structure
- Agent loop explained
- Tools deep dive
- Building your own agent
- Skills vs Multi-Agent systems research

### 07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md (CURRENT)
- TypeScript syntax explained for beginners
- Layer-by-layer code walkthrough
- Function call graphs
- Complete execution trace
- Every file explained

### 06_OPENCODE_BEGINNER_WALKTHROUGH.md (OLD - Go version)
- ⚠️ Documents the older Go implementation
- Kept for historical reference
- For current code, use 07_OPENCODE_TYPESCRIPT_WALKTHROUGH.md

### GLOSSARY.md
- 50+ technical terms explained simply
- Analogies for every concept
- Code examples where helpful
- Quick reference card

### ARCHITECTURE.md
- Three-layer architecture diagram
- Component details
- Message flow
- Security model

### TOOLS_COMPARISON.md
- Tool-by-tool comparison table
- Unique features of each
- ~90% similarity analysis

---

## Key Concepts Quick Reference

| Concept | Definition |
|---------|------------|
| **Agent Loop** | Think -> Use Tool -> See Result -> Think again -> Repeat until done |
| **Tool** | A function AI can call (Read, Write, Bash, etc.) |
| **Skill** | Instructions that teach AI how to do something |
| **MCP** | Protocol for connecting to external tools |
| **Permission** | Gate that blocks dangerous operations |

---

## Related Resources

### Source Code:
- OpenCode: `D:/Github/opencode/packages/opencode/src/`
- Key files:
  - `tool/` - All tool implementations
  - `agent/agent.ts` - The agent loop
  - `session/` - Conversation management

### Online Docs:
- OpenCode: https://opencode.ai/docs
- Claude Code: https://docs.anthropic.com/claude-code

---

*Last Updated: January 2026*
