# Tools Comparison: OpenCode vs Claude Code

This document compares the tools available in OpenCode and Claude Code.

---

## Tool-by-Tool Comparison

### 1. Read Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Read files | Yes | Yes |
| Line offset | Yes | Yes |
| Line limit | Yes | Yes |
| Read images | Yes | Yes |
| Read PDFs | Yes | Yes |
| Read Jupyter notebooks | Yes | Yes |

**Prompt (nearly identical):**
- Both explain the tool reads files
- Both mention line numbers start at 1
- Both can read images, PDFs, notebooks

---

### 2. Write Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Create new files | Yes | Yes |
| Overwrite existing | Yes | Yes |
| Must read first (existing) | Yes | Yes |

**Key rule in both:**
> "ALWAYS prefer editing existing files. NEVER write new files unless explicitly required."

---

### 3. Edit Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Find and replace | Yes | Yes |
| Must be unique match | Yes | Yes |
| replace_all option | Yes | Yes |

**Same requirement:**
> "You must use your Read tool at least once before editing."

---

### 4. Bash Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Run shell commands | Yes | Yes |
| Timeout option | Yes | Yes |
| Background execution | Yes | Yes |
| Working directory | `workdir` param | `cd &&` pattern |

**Git safety rules (identical):**
- Never force push
- Never amend without permission
- Never skip hooks
- Never update git config

---

### 5. Glob Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| File pattern matching | Yes | Yes |
| Recursive search | Yes | Yes |
| Sorted by modification | Yes | Yes |

**Same patterns:** `*.js`, `src/**/*.tsx`, etc.

---

### 6. Grep Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Content search | Yes | Yes |
| Regex support | Yes | Yes |
| Context lines (-A/-B/-C) | Yes | Yes |
| File type filter | Yes | Yes |
| Output modes | Yes | Yes |

---

### 7. WebFetch Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Fetch URL content | Yes | Yes |
| Process with AI | Yes | Yes |
| HTML to markdown | Yes | Yes |

---

### 8. WebSearch Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Search internet | Yes | Yes |
| Domain filtering | Yes | Yes |

---

### 9. Task Tool (Subagents)

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Spawn subagents | Yes | Yes |
| Background tasks | Yes | Yes |
| Explore agent | Yes | Yes |
| Plan agent | Yes | Yes |

---

### 10. TodoWrite Tool

| Feature | OpenCode | Claude Code |
|---------|----------|-------------|
| Track task progress | Yes | Yes |
| States: pending/in_progress/completed | Yes | Yes |

---

## Unique Features

### OpenCode Only:
- **LSP Integration** - Language Server Protocol for better code understanding
- **Multiple providers** - Works with Claude, OpenAI, Google, local models
- **TUI focus** - Rich terminal interface
- **Client/server architecture** - Can run remotely

### Claude Code Only:
- **Anthropic optimized** - Tuned specifically for Claude models
- **IDE extensions** - VS Code, JetBrains integration
- **Claude.ai integration** - Seamless with web interface

---

## Conclusion

**Similarity: ~90%**

The tools are nearly identical in:
- Functionality
- Parameters
- Prompt instructions
- Safety rules

OpenCode was clearly designed to mirror Claude Code's tool system, making knowledge of one transferable to the other.
