# Claude Code: Tools, Architecture, and Comparison with AgentCore

## Document Purpose
This document explains how Claude Code works internally, lists all its tools, and provides a side-by-side comparison with AWS AgentCore to help you understand how to implement similar capabilities.

---

# PART 1: WHAT IS CLAUDE CODE?

## 1.1 Overview

**Claude Code** is Anthropic's CLI (Command Line Interface) tool that allows Claude to:
- Write, test, and debug code alongside you
- Navigate your codebase
- Edit multiple files
- Run commands to verify its work

**It is NOT just a chatbot.** It is an **agent** that has access to tools and can take actions on your computer.

## 1.2 How Claude Code Runs

Claude Code can run in two environments:

### Local CLI (on your machine)
- Runs directly on your computer
- Has access to your filesystem
- Can execute bash commands
- Uses OS-level sandboxing for security (Linux bubblewrap, MacOS seatbelt)

### Web Version (claude.ai with Code feature)
- Runs in an Anthropic-managed **Virtual Machine (VM)**
- Your repository is cloned to the VM
- Uses gVisor-backed container for isolation
- HTTP-only egress for network security

## 1.3 Why Bash and VM?

**Q: Why does Claude Code use Bash?**

**A:** Bash is the tool that allows Claude Code to execute shell commands on the operating system. When Claude Code needs to:
- Run your code (`python script.py`)
- Install packages (`npm install`)
- Use git (`git commit`)
- Run tests (`pytest`)

It uses the **Bash tool** to execute these commands.

**Q: Is there a VM?**

**A:**
- **Web version**: Yes, runs in a VM with gVisor container
- **Local CLI**: No VM, runs directly on your machine with OS-level sandboxing

**Source**: [Anthropic Engineering - Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)

---

# PART 2: COMPLETE LIST OF CLAUDE CODE TOOLS

These are the tools I (Claude Code) have access to. This is NOT from inference - this is from official documentation.

## 2.1 File Tools

### Read
**Purpose**: Read file contents from the filesystem
**Parameters**:
- `file_path` (required): Absolute path to the file
- `offset` (optional): Line number to start reading from
- `limit` (optional): Number of lines to read

**Example**:
```
Read file_path="/home/user/project/main.py"
Read file_path="/home/user/project/main.py" offset=100 limit=50
```

### Write
**Purpose**: Write content to a file (creates or overwrites)
**Parameters**:
- `file_path` (required): Absolute path to the file
- `content` (required): Content to write

**Example**:
```
Write file_path="/home/user/project/new_file.py" content="print('hello')"
```

### Edit
**Purpose**: Perform exact string replacements in files
**Parameters**:
- `file_path` (required): Absolute path to the file
- `old_string` (required): Text to replace
- `new_string` (required): Replacement text
- `replace_all` (optional): Replace all occurrences (default: false)

**Example**:
```
Edit file_path="/home/user/project/main.py" old_string="def old_name" new_string="def new_name"
```

### MultiEdit
**Purpose**: Make multiple edits to a single file in one operation
**Parameters**:
- `file_path` (required): Absolute path to the file
- `edits` (required): Array of edit objects

## 2.2 Search Tools

### Glob
**Purpose**: Fast file pattern matching (find files by name pattern)
**Parameters**:
- `pattern` (required): Glob pattern like `**/*.py`
- `path` (optional): Directory to search in

**Example**:
```
Glob pattern="**/*.py"
Glob pattern="**/test_*.py" path="/home/user/project"
```

### Grep
**Purpose**: Search file contents using regular expressions (built on ripgrep)
**Parameters**:
- `pattern` (required): Regex pattern to search for
- `path` (optional): Directory to search in
- `include` (optional): File pattern filter
- `type` (optional): File type (py, js, etc.)
- `output_mode` (optional): "content" or "files_with_matches"

**Example**:
```
Grep pattern="def.*handler" type="py"
Grep pattern="import boto3" path="/home/user/project" output_mode="content"
```

### LS
**Purpose**: List files and directories
**Parameters**:
- `path` (required): Absolute path to list
- `ignore` (optional): Glob patterns to exclude

## 2.3 Execution Tools

### Bash
**Purpose**: Execute shell commands
**Parameters**:
- `command` (required): The command to execute
- `timeout` (optional): Max execution time in milliseconds (max 600000)
- `description` (optional): Description of what the command does

**Example**:
```
Bash command="python main.py" description="Run the main script"
Bash command="npm install" timeout=120000
Bash command="git status"
```

**IMPORTANT**: The Bash tool is the gateway to the operating system. It can run ANY command that the OS supports.

## 2.4 Web Tools

### WebFetch
**Purpose**: Fetch and analyze web content
**Parameters**:
- `url` (required): URL to fetch
- `prompt` (required): What to extract/analyze from the page

### WebSearch
**Purpose**: Search the web
**Parameters**:
- `query` (required): Search query
- `allowed_domains` (optional): Only include these domains
- `blocked_domains` (optional): Exclude these domains

## 2.5 Task Management Tools

### TodoRead
**Purpose**: Read the current to-do list
**Parameters**: None

### TodoWrite
**Purpose**: Create and manage task lists
**Parameters**:
- `todos` (required): Array of todo objects with content, status, priority

## 2.6 Notebook Tools

### NotebookRead
**Purpose**: Read Jupyter notebook files
**Parameters**:
- `notebook_path` (required): Path to .ipynb file

### NotebookEdit
**Purpose**: Edit Jupyter notebook cells
**Parameters**:
- `notebook_path` (required): Path to .ipynb file
- `cell_number` (required): Cell to edit (0-indexed)
- `new_source` (required): New cell content
- `cell_type` (optional): "code" or "markdown"
- `edit_mode` (optional): "replace", "insert", or "delete"

## 2.7 Agent Tools

### Task (Agent)
**Purpose**: Launch a sub-agent to handle complex tasks
**Parameters**:
- `description` (required): 3-5 word summary
- `prompt` (required): Detailed task instructions
- `subagent_type` (required): Type of agent to use

**Sub-agent types**:
- `Explore`: Fast, read-only agent for codebase exploration (uses Haiku model)
- `general-purpose`: Full-capability agent for complex tasks (uses Sonnet)
- `Plan`: Planning agent for implementation strategies

**Source**: [GitHub Gist - Claude Code Tools](https://gist.github.com/wong2/e0f34aac66caf890a332f7b6f9e2ba8f)

---

# PART 3: WHAT ARE SKILLS IN CLAUDE CODE?

## 3.1 Skills vs Tools - The Key Difference

| Aspect | Tools | Skills |
|--------|-------|--------|
| What they do | Execute actions, return results | Inject instructions into context |
| How invoked | Claude calls tool directly | Claude loads SKILL.md file |
| Contains | Code/functions | Markdown instructions + optional scripts |
| When loaded | Always available | On-demand when relevant |
| Purpose | DO something | TEACH how to do something |

**Tools** = Functions that take input and return output (Read, Write, Bash)
**Skills** = Instruction packages that modify how Claude approaches a task

## 3.2 How Skills Work

```
1. At startup: Claude scans all SKILL.md files, loads only name + description
2. User asks: "Create a PowerPoint presentation"
3. Claude recognizes: This matches the "pptx" skill description
4. Claude loads: Full SKILL.md instructions into context
5. Claude follows: The loaded instructions to complete the task
```

**Skills are NOT code execution.** They are **prompt expansion** - adding specialized instructions to Claude's context.

## 3.3 SKILL.md File Structure

```markdown
---
name: my-skill
description: Description of what this skill does. Use when user asks about X.
allowed-tools:
  - Read
  - Grep
  - Bash
---

# My Skill Instructions

## When to Use
Use this skill when the user wants to...

## Steps
1. First, do this
2. Then, do that
3. Finally, verify by...

## Examples
[Example inputs and outputs]
```

## 3.4 Skills in Claude Code vs AgentCore

**Claude Code Skills**:
- Filesystem-based (folder with SKILL.md)
- Loaded by Claude automatically when relevant
- Contain instructions (markdown) + optional scripts
- Modify Claude's context/behavior

**AgentCore Equivalent**:
- There is NO direct equivalent in AgentCore
- Closest concept: System prompts + tool definitions
- You would need to implement skill-like behavior in your agent code

**Source**: [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)

---

# PART 4: HOW I DID YOUR TAX RETURN (Thinking Process)

This section documents how Claude Code approaches complex tasks, using a tax return example.

## 4.1 The Thinking Process

When you asked me to help with your tax return, here's what happened:

```
STEP 1: UNDERSTAND THE REQUEST
- User wants help with tax return
- Need to identify what files/documents exist
- Need to understand the tax context

STEP 2: EXPLORE THE CODEBASE
Tools used: Glob, Read
- Find all relevant files (receipts, documents, spreadsheets)
- Read file contents to understand the data

STEP 3: ANALYZE THE DATA
Tools used: Read (for files), possibly Grep (to search for amounts)
- Extract relevant numbers
- Categorize expenses
- Identify deductions

STEP 4: PERFORM CALCULATIONS
Tools used: Bash (to run Python scripts), or direct calculation
- Sum up categories
- Apply tax rules
- Calculate final amounts

STEP 5: CREATE OUTPUT
Tools used: Write, Edit
- Generate summary document
- Create any needed reports
- Save results

STEP 6: VERIFY
Tools used: Read (to check output), Bash (to run validation)
- Verify calculations
- Check for errors
- Confirm completeness
```

## 4.2 Tool Selection Logic

| Task | Tool Choice | Why |
|------|-------------|-----|
| Find all receipt files | Glob | Pattern matching for file discovery |
| Read a specific receipt | Read | Direct file reading |
| Search for "expense" in files | Grep | Content search across files |
| Run Python calculation script | Bash | Execute code |
| Create summary document | Write | Create new file |
| Update existing document | Edit | Modify specific parts |

## 4.3 Key Insight: Claude Code is Tool-Driven

Claude Code doesn't "think" in abstract terms. It:
1. Receives your request
2. Decides which TOOL to use
3. Calls the tool with parameters
4. Gets the result
5. Decides next tool or responds to you

**This is the "agent loop"** - the same pattern used in AgentCore, Bedrock Agents, etc.

---

# PART 5: SIDE-BY-SIDE COMPARISON - CLAUDE CODE VS AGENTCORE

## 5.1 Architecture Comparison

```
┌─────────────────────────────────────┐    ┌─────────────────────────────────────┐
│         CLAUDE CODE                 │    │         AGENTCORE                   │
├─────────────────────────────────────┤    ├─────────────────────────────────────┤
│                                     │    │                                     │
│  User Input (CLI or Web)            │    │  User Input (API call)              │
│         ↓                           │    │         ↓                           │
│  Claude LLM (Opus/Sonnet)           │    │  YOUR @app.entrypoint               │
│         ↓                           │    │         ↓                           │
│  Tool Selection (by Claude)         │    │  YOUR agent() call                  │
│         ↓                           │    │         ↓                           │
│  Tool Execution                     │    │  YOUR @tool functions               │
│  - Read, Write, Edit                │    │  - Your custom functions            │
│  - Glob, Grep                       │    │  - Can call any API/service         │
│  - Bash                             │    │  - Can run any code                 │
│         ↓                           │    │         ↓                           │
│  Result back to Claude              │    │  Result back to your code           │
│         ↓                           │    │         ↓                           │
│  Claude decides next step           │    │  YOU decide next step               │
│         ↓                           │    │         ↓                           │
│  Response to User                   │    │  Response to User                   │
│                                     │    │                                     │
│  WHO CONTROLS LOOP: Anthropic       │    │  WHO CONTROLS LOOP: YOU             │
└─────────────────────────────────────┘    └─────────────────────────────────────┘
```

## 5.2 Tool Mapping: Claude Code → AgentCore

| Claude Code Tool | AgentCore Equivalent | Notes |
|------------------|---------------------|-------|
| **Read** | Your function reads file | `open(path).read()` |
| **Write** | Your function writes file | `open(path, 'w').write(content)` |
| **Edit** | Your function edits file | String replacement logic |
| **Glob** | `glob.glob()` or `pathlib` | Python's glob module |
| **Grep** | `subprocess.run(['rg', ...])` | Call ripgrep or use regex |
| **Bash** | `subprocess.run()` | Python subprocess module |
| **WebFetch** | `requests.get()` + LLM | Fetch URL, analyze with model |
| **WebSearch** | External search API | Not built-in, need API |
| **Task (Agent)** | Create sub-agents | Your code spawns sub-processes |

## 5.3 Implementing Claude Code-like Tools in AgentCore

### Example: Read Tool
```python
# CLAUDE CODE internally does something like this:

# In AgentCore, you write:
@tool
def read_file(file_path: str, offset: int = 0, limit: int = None) -> str:
    """
    Read file contents from the filesystem.

    Args:
        file_path: Absolute path to the file
        offset: Line number to start from (0-indexed)
        limit: Number of lines to read (None = all)

    Returns:
        File contents as string
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if offset:
        lines = lines[offset:]
    if limit:
        lines = lines[:limit]

    return ''.join(lines)
```

### Example: Glob Tool
```python
import glob as glob_module
from pathlib import Path

@tool
def glob_search(pattern: str, path: str = ".") -> list:
    """
    Find files matching a glob pattern.

    Args:
        pattern: Glob pattern like "**/*.py"
        path: Directory to search in

    Returns:
        List of matching file paths
    """
    search_path = Path(path) / pattern
    matches = glob_module.glob(str(search_path), recursive=True)
    return sorted(matches)
```

### Example: Grep Tool
```python
import subprocess

@tool
def grep_search(pattern: str, path: str = ".", file_type: str = None) -> list:
    """
    Search file contents using ripgrep.

    Args:
        pattern: Regex pattern to search for
        path: Directory to search in
        file_type: File type filter (py, js, etc.)

    Returns:
        List of matching files with line numbers
    """
    cmd = ["rg", "-l", pattern, path]  # -l for files only
    if file_type:
        cmd.extend(["--type", file_type])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().split('\n') if result.stdout else []
```

### Example: Bash Tool
```python
import subprocess

@tool
def run_command(command: str, timeout: int = 120) -> dict:
    """
    Execute a shell command.

    Args:
        command: The command to execute
        timeout: Max execution time in seconds

    Returns:
        Dict with stdout, stderr, and return code
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout} seconds"}
```

## 5.4 Feature Comparison

| Feature | Claude Code | AgentCore |
|---------|-------------|-----------|
| **Tools** | Pre-built (Read, Write, Bash, etc.) | You define them |
| **Skills** | SKILL.md files with instructions | No equivalent - use prompts |
| **Model** | Fixed (Opus/Sonnet) | Any model you choose |
| **Loop Control** | Anthropic controls | You control |
| **Sandboxing** | Built-in OS-level | You implement |
| **Memory** | Session-based | Short + Long-term + Episodic |
| **Max Runtime** | Your machine limits | 8 hours |
| **Cost** | Subscription | Pay per use |

## 5.5 When to Use Which

**Use Claude Code when:**
- You want a ready-to-use coding assistant
- You're working on your local machine
- You don't need to customize the agent loop
- Standard tools (Read, Write, Bash) are sufficient

**Use AgentCore when:**
- You're building a product/service for others
- You need custom tools beyond file operations
- You need to control the agent loop
- You need long-running tasks (hours)
- You need memory across sessions
- You need policy enforcement

---

# PART 6: ANSWERING YOUR SPECIFIC QUESTIONS

## Q1: "Skills are just action groups, so I don't need sub-agents, just use one?"

**CORRECT understanding.**

If you implement each sub-agent's capability as a **tool** (action group in Bedrock, @tool in AgentCore), then you only need ONE agent that has access to all tools.

```
BEFORE (Multi-Agent):
Router Agent → Claims Sub-Agent (has LLM brain)
            → Documents Sub-Agent (has LLM brain)
            → Status Sub-Agent (has LLM brain)

AFTER (Single Agent + Tools):
Single Agent → get_claims() tool (Lambda, no LLM)
            → get_documents() tool (Lambda, no LLM)
            → get_status() tool (Lambda, no LLM)
```

**Benefits of single agent + tools:**
- Fewer LLM calls (cost savings)
- More predictable behavior
- Easier to debug
- Easier to audit

## Q2: "This flow is still controlled by one LLM? Not good, need hybrid?"

**CORRECT concern.**

Even with one agent, the LLM still decides:
- Which tool to call
- In what order
- When to stop

For **insurance/regulated industries**, you need **HYBRID**:
- LLM decides conversation flow
- CODE decides PASS/FLAG

**In Bedrock Agents**: You cannot fully control the loop
**In AgentCore**: You CAN control the loop

```python
# AgentCore - YOU control when LLM runs
@app.entrypoint
def invoke(payload):
    # YOU can add pre-checks before LLM
    if not user_has_permission(payload):
        return {"error": "Not authorized"}

    # YOU decide to call the agent
    result = agent(payload["prompt"])

    # YOU can override or validate after LLM
    if contains_decision(result):
        # Don't let LLM make PASS/FLAG - use code
        decision = code_based_decision(payload)
        return decision

    return result
```

## Q3: "Is action group in Bedrock same as AgentCore tools?"

**SIMILAR but different implementation:**

| Aspect | Bedrock Action Group | AgentCore @tool |
|--------|---------------------|-----------------|
| Definition | OpenAPI schema + Lambda | Python function with @tool |
| Execution | AWS invokes Lambda | Your code calls function |
| Control | AWS manages | You manage |
| Format | JSON schema required | Docstring + type hints |

**The LOGIC is portable.** Your Lambda code can be reused as an AgentCore tool.

## Q4: "Allow user to request relevant tools like Claude Code?"

**YES, this is possible in AgentCore.**

In AgentCore, the user sends a message, the agent decides which tool to use (just like Claude Code).

```python
# AgentCore agent with multiple tools
agent = Agent(
    model="anthropic.claude-3-sonnet-20240229-v1:0",
    tools=[
        read_file,      # Like Claude Code's Read
        write_file,     # Like Claude Code's Write
        search_files,   # Like Claude Code's Grep
        run_command,    # Like Claude Code's Bash
        submit_claim,   # Your custom tool
        get_status,     # Your custom tool
    ],
    system_prompt="""You are an assistant with access to these tools.
    Use them to help the user accomplish their tasks.
    """
)

@app.entrypoint
def invoke(payload):
    user_message = payload["prompt"]

    # Agent decides which tools to use based on user message
    result = agent(user_message)

    return {"response": result.message}
```

**User can say:** "Check the status of claim CLM-123"
**Agent decides:** Use `get_status` tool with claim_id="CLM-123"

## Q5: "Why Bash in Claude Code?"

**Bash is NOT a skill.** Bash is a **TOOL** that executes shell commands.

Claude Code runs on your computer (or in a VM). To interact with the operating system, it needs a way to run commands. That's what Bash does.

```
User: "Run my Python tests"
Claude: Uses Bash tool with command="pytest"
OS: Executes pytest
Result: Test output returned to Claude
```

## Q6: "Is Grep a skill?"

**NO.** Grep is a **TOOL**, not a skill.

- **Grep TOOL**: Searches file contents, returns matches
- **A Grep SKILL would be**: Instructions on HOW to use Grep effectively (but this doesn't exist as a separate skill because Grep is built-in)

**Skills** = Instructions (markdown)
**Tools** = Actions (code execution)

---

# PART 7: GLOSSARY FOR THIS DOCUMENT

| Term | Definition |
|------|------------|
| **Tool** | Function that takes input, performs action, returns output |
| **Skill** | Markdown instructions that modify how Claude approaches tasks |
| **Agent Loop** | The cycle of: receive input → decide action → execute → evaluate → repeat |
| **Sandbox** | Security boundary that limits what code can access |
| **VM** | Virtual Machine - isolated computing environment |
| **Bash** | Unix shell for running commands on the operating system |
| **Glob** | Pattern matching syntax for file paths (e.g., `**/*.py`) |
| **Grep** | Tool for searching text content (Claude uses ripgrep) |
| **ripgrep (rg)** | Fast search tool, pre-installed in Claude Code |

---

# PART 8: SOURCES

All information in this document is from official sources:

- [Anthropic Engineering - Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
- [Claude Code Docs - Sandboxing](https://code.claude.com/docs/en/sandboxing)
- [Claude Code Docs - Skills](https://code.claude.com/docs/en/skills)
- [GitHub Gist - Claude Code Tools](https://gist.github.com/wong2/e0f34aac66caf890a332f7b6f9e2ba8f)
- [Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Anthropic - Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

**Document Version**: 1.0
**Last Updated**: January 2026
**Designed For**: Beginners understanding Claude Code architecture
