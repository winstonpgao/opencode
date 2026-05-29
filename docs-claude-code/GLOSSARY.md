# Glossary: AI Coding Agents Terminology

This glossary explains all technical terms used in the documentation, written for complete beginners.

---

## A

### Agent
**What it is**: A "personality mode" for the AI that determines how it behaves.

**Simple analogy**: Like switching between "work mode" and "explore mode" on a robot.

**Example**:
- "build" agent: Can edit files, run commands - for actual work
- "plan" agent: Can only read files - for safe exploration

### Agent Loop
**What it is**: The core pattern of how AI coding assistants work - think, act, observe, repeat.

**Simple analogy**: Like a chef: read recipe → cook step → taste → adjust → repeat until done.

**Diagram**:
```
Think → Use Tool → See Result → Think Again → Use Tool → ... → Done!
```

### API (Application Programming Interface)
**What it is**: A way for programs to talk to each other.

**Simple analogy**: Like a waiter at a restaurant - you tell the waiter what you want, they bring it from the kitchen.

**Example**: OpenCode uses Anthropic's API to talk to Claude.

### Async/Await
**What it is**: A way to handle things that take time (like waiting for a file to download).

**Simple analogy**: Like ordering food and doing other things while waiting, instead of staring at the kitchen.

**Code example**:
```typescript
const data = await fetchFile()  // WAIT here until file is ready
console.log(data)               // Then continue
```

---

## B

### Bash
**What it is**: A command-line shell - a way to type commands to your computer.

**Simple analogy**: Like texting your computer instead of clicking buttons.

**Example commands**:
```bash
ls           # List files
cd folder    # Go into folder
npm install  # Install packages
```

### Bootstrap
**What it is**: The initialization process when a program starts.

**Simple analogy**: Like warming up before exercise - getting everything ready.

---

## C

### CLI (Command Line Interface)
**What it is**: A text-based way to interact with a program (instead of clicking buttons).

**Simple analogy**: Typing instructions vs pointing and clicking.

**Example**:
```bash
opencode run "Fix the bug"   # CLI way
# vs clicking buttons in a GUI
```

### Context
**What it is**: All the information the AI can "see" at once.

**Simple analogy**: Like the papers on your desk - there's only so much space.

**Why it matters**: AI has limited context (usually 100k-200k tokens), so it can't remember everything.

### Context Window
**What it is**: The maximum amount of text/information an AI can process at once.

**Simple analogy**: Like the size of a whiteboard - only so much can fit.

**Sizes**:
- Small: ~8,000 tokens
- Medium: ~100,000 tokens
- Large: ~200,000 tokens

---

## E

### Execute
**What it is**: To run or perform an action.

**Simple analogy**: Actually doing something vs planning to do it.

**Example**: "Execute the Bash tool" = actually run the command.

---

## G

### Git
**What it is**: A system that saves versions of your code (like save points in a game).

**Simple analogy**: Like "undo history" but for your entire project, forever.

**Common commands**:
```bash
git status   # What changed?
git add .    # Stage changes
git commit   # Save a checkpoint
git push     # Upload to GitHub
```

### Glob
**What it is**: A pattern for matching file names.

**Simple analogy**: Like a search pattern - "find all .txt files".

**Examples**:
```
*.py          # All Python files
**/*.ts       # All TypeScript files in any subfolder
test_*.js     # All JS files starting with "test_"
```

### Grep
**What it is**: A tool for searching inside files for specific text.

**Simple analogy**: Like Ctrl+F but for all files at once.

**Example**: `grep "function login"` finds all files containing "function login".

---

## H

### Hook
**What it is**: Code that runs automatically at specific points.

**Simple analogy**: Like a doorbell that rings when someone arrives - automatic action on event.

**Example**: A "PreToolUse" hook runs before every tool is used.

---

## I

### Interface
**What it is**: A description of what shape data should have.

**Simple analogy**: Like a form template - describes what fields are needed.

**Code example**:
```typescript
interface User {
    name: string    // Must have name (text)
    age: number     // Must have age (number)
}
```

---

## J

### JSON (JavaScript Object Notation)
**What it is**: A text format for storing structured data.

**Simple analogy**: Like a form with labels and values.

**Example**:
```json
{
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "JavaScript"]
}
```

---

## L

### LLM (Large Language Model)
**What it is**: The AI brain - a program trained to understand and generate text.

**Simple analogy**: A very smart autocomplete that can write, code, and reason.

**Examples**: Claude, GPT-4, Gemini

### LSP (Language Server Protocol)
**What it is**: A standard for code intelligence (autocomplete, error detection, etc.).

**Simple analogy**: Like a spell-checker but for code - finds errors, suggests fixes.

---

## M

### MCP (Model Context Protocol)
**What it is**: A standard for connecting AI to external tools and data.

**Simple analogy**: Like USB - a standard way to plug in different tools.

**Example**: Connect to GitHub, databases, or custom tools.

### Message History
**What it is**: The conversation so far (what you said, what AI said).

**Simple analogy**: Like a chat log - all previous messages.

### Middleware
**What it is**: Code that runs in the middle of a process.

**Simple analogy**: Like a filter in a water pipe - processes things as they flow through.

### Model
**What it is**: A specific AI brain (like claude-sonnet-4 or gpt-4).

**Simple analogy**: Different models are like different employees with different skills and costs.

---

## N

### Namespace
**What it is**: A container for grouping related code together.

**Simple analogy**: Like folders on your computer - organizing things by topic.

**Code example**:
```typescript
namespace Tool {
    export function define() { }
    export type Info = { }
}
// Usage: Tool.define()
```

---

## P

### Parameter
**What it is**: An input value for a function or tool.

**Simple analogy**: Like ingredients for a recipe - what you need to provide.

**Example**: The Read tool needs a `file_path` parameter.

### Parse
**What it is**: To break down text into structured parts.

**Simple analogy**: Like reading a sentence and identifying subject, verb, object.

### Permission
**What it is**: A rule about what the AI can or cannot do.

**Simple analogy**: Like asking "May I?" before doing something potentially risky.

**Types**:
- `allow` - Always permitted
- `deny` - Always blocked
- `ask` - Prompt user first

### Promise
**What it is**: An object representing a future value.

**Simple analogy**: Like a "ticket" for food at a busy restaurant - you'll get it eventually.

**Code example**:
```typescript
const promise = fetchData()  // Returns immediately with a "promise"
const data = await promise   // Actually wait for the data
```

### Provider
**What it is**: An AI service company (Anthropic, OpenAI, Google, etc.).

**Simple analogy**: Like different phone carriers - they all provide similar services.

### Prompt
**What it is**: Instructions or questions given to an AI.

**Simple analogy**: Like giving someone directions - telling them what you want.

**Types**:
- System prompt: Background instructions
- User prompt: Your actual request

---

## R

### Regex (Regular Expression)
**What it is**: A pattern for matching text.

**Simple analogy**: Like a search pattern with wildcards.

**Example**: `\d+` matches any number (123, 45, 6789).

### Repository (Repo)
**What it is**: A folder with git version control.

**Simple analogy**: Like a project folder that remembers all its history.

---

## S

### Schema
**What it is**: A description of what data should look like.

**Simple analogy**: Like a blueprint - describes the structure.

**Example** (Zod schema):
```typescript
const UserSchema = z.object({
    name: z.string(),
    age: z.number()
})
```

### Session
**What it is**: A conversation with all its history and state.

**Simple analogy**: Like a phone call - starts, has a conversation, ends.

### Streaming
**What it is**: Receiving data piece by piece instead of all at once.

**Simple analogy**: Like watching a video as it downloads vs waiting for full download.

**Why it matters**: You see AI typing in real-time instead of waiting for full response.

### System Prompt
**What it is**: Hidden instructions that set up the AI's behavior.

**Simple analogy**: Like briefing an employee before they start work.

---

## T

### Terminal
**What it is**: A text-based interface for running commands.

**Simple analogy**: Like texting your computer.

**Other names**: Console, Command Line, Shell

### Token
**What it is**: A piece of text (roughly a word or part of a word).

**Simple analogy**: Like syllables in speech.

**Examples**:
- "Hello" = 1 token
- "Hello world" = 2 tokens
- "authentication" = 3 tokens

**Why it matters**: AI charges per token and has token limits.

### Tool
**What it is**: A function that AI can call to take action.

**Simple analogy**: Like hands for the AI - how it interacts with the world.

**Examples**: Read, Write, Edit, Bash, Grep, Glob

### TUI (Terminal User Interface)
**What it is**: A graphical interface inside a terminal.

**Simple analogy**: Like a colorful app but made of text characters.

### Type
**What it is**: The kind of data (string, number, boolean, etc.).

**Simple analogy**: Like categories - is it text, a number, or true/false?

---

## U

### UI (User Interface)
**What it is**: How you interact with a program.

**Types**:
- GUI: Graphical (clicking buttons)
- CLI: Command line (typing commands)
- TUI: Text-based graphical

---

## V

### VM (Virtual Machine)
**What it is**: A computer simulated inside another computer.

**Simple analogy**: Like a computer inside a computer - isolated and safe.

---

## W

### Webhook
**What it is**: A notification sent when something happens.

**Simple analogy**: Like a doorbell - something happens, you get notified.

---

## Y

### YAML
**What it is**: A text format for configuration files (like JSON but easier to read).

**Simple analogy**: Like a form but without all the brackets.

**Example**:
```yaml
name: Alice
age: 25
skills:
  - Python
  - JavaScript
```

---

## Z

### Zod
**What it is**: A TypeScript library for validating data.

**Simple analogy**: Like a bouncer at a club - checks if data meets requirements.

**Example**:
```typescript
const schema = z.object({ name: z.string() })
schema.parse({ name: "Alice" })  // OK
schema.parse({ name: 123 })      // Error!
```

---

# Quick Reference Card

## Most Important Concepts

| Concept | One-Line Definition |
|---------|---------------------|
| **Agent Loop** | Think → Act → Observe → Repeat |
| **Tool** | Function AI can call (Read, Write, Bash) |
| **Session** | A conversation with history |
| **Provider** | AI service (Anthropic, OpenAI) |
| **Context** | What AI can "see" |
| **Token** | Unit of text (roughly one word) |
| **Permission** | Rule about what AI can do |
| **Streaming** | Getting response piece by piece |

---

*Last Updated: January 2026*
