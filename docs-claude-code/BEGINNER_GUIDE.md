# OpenCode Beginner's Guide
## Understanding AI Coding Assistants - Explained Simply

---

# Part 1: The Basics (Start Here!)

## What is OpenCode / Claude Code?

Imagine you have a **super smart robot friend** who can:
- Read all your code files
- Write new code for you
- Run commands on your computer
- Search the internet for answers
- Fix bugs in your programs

That's what OpenCode and Claude Code are! They're AI assistants that help you write code.

**Think of it like this:**
```
You (the human)  -->  Talk to AI  -->  AI does the work  -->  You get results
     |                    |                   |                    |
  "Fix the bug"     AI understands      AI edits files      Bug is fixed!
```

---

## What is a Terminal?

A **terminal** (also called "command line" or "console") is like texting your computer.

Instead of clicking buttons with a mouse, you TYPE instructions.

**Example - Using a Mouse vs Terminal:**

| Task | With Mouse | With Terminal |
|------|------------|---------------|
| Open a folder | Double-click folder icon | Type: `cd my-folder` |
| Create a file | Right-click > New File | Type: `touch newfile.txt` |
| Delete a file | Right-click > Delete | Type: `rm oldfile.txt` |
| See what's in a folder | Look at the window | Type: `ls` |

**Why use a terminal?**
- It's FASTER once you learn it
- You can do things that aren't possible with clicking
- AI assistants communicate through terminals

---

## Key Words You'll See (Glossary)

| Word | Simple Meaning | Example |
|------|----------------|---------|
| **CLI** | Command Line Interface - typing commands | When you type `opencode` to start |
| **TUI** | Text User Interface - a visual app in terminal | OpenCode's colorful screen |
| **API** | A way for programs to talk to each other | How OpenCode talks to Claude |
| **Git** | Saves versions of your code (like save points in games) | `git commit` saves your work |
| **Repository (Repo)** | A folder with git tracking | Your project folder |
| **LLM** | Large Language Model - the AI brain | Claude, GPT, etc. |
| **Prompt** | Instructions you give to AI | "Write a function that adds numbers" |
| **Token** | A piece of text (word or part of word) | "Hello" = 1 token |

---

# Part 2: How Does It Work?

## The Big Picture

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|   YOU (Human)    | --> |   OpenCode/      | --> |   AI Brain       |
|                  |     |   Claude Code    |     |   (Claude, etc)  |
|  "Add a button"  |     |   [Middleman]    |     |   [Thinks...]    |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
                                  |
                                  v
                         +------------------+
                         |                  |
                         |   Your Files     |
                         |   [Gets edited]  |
                         |                  |
                         +------------------+
```

**Step by step:**

1. **You type** a request: "Add a login button to my website"
2. **OpenCode reads** your files to understand your code
3. **OpenCode sends** your request + code context to AI
4. **AI thinks** and decides what to do
5. **AI responds** with actions (edit this file, run this command)
6. **OpenCode executes** those actions on your computer
7. **You see** the results!

---

## The Tools (AI's Hands)

The AI can't directly touch your computer. It uses **tools** - like giving a robot different hands for different jobs.

### Tool 1: Read (The Eyes)

**What it does:** Looks at a file to see what's inside

**Like:** Opening a book to read it

**Example:**
```
AI thinks: "I need to see what's in the login page"
AI uses: Read tool on "login.html"
AI now knows: The file contains a form with username/password fields
```

**Real usage:**
```
Tool: Read
File: /my-project/login.html
Result: Shows all the code in that file
```

---

### Tool 2: Write (The Pen)

**What it does:** Creates a new file or completely replaces a file

**Like:** Writing a new page in a notebook

**Example:**
```
AI thinks: "I need to create a new page for user settings"
AI uses: Write tool to create "settings.html"
Result: New file appears with the code AI wrote
```

**When to use Write vs Edit:**
- **Write**: Creating new files, or replacing everything
- **Edit**: Changing just part of a file

---

### Tool 3: Edit (The Eraser + Pen)

**What it does:** Changes PART of a file (find old text, replace with new text)

**Like:** Using white-out to fix one word in a sentence

**Example:**
```
File before:
  <button>Click Me</button>

AI uses Edit:
  Find: "Click Me"
  Replace with: "Login Now"

File after:
  <button>Login Now</button>
```

**Why not just rewrite the whole file?**
- Faster (only change what's needed)
- Safer (won't accidentally delete other code)
- Clearer (you see exactly what changed)

---

### Tool 4: Bash (The Doer)

**What it does:** Runs commands on your computer

**Like:** Telling your computer to DO something, not just look at files

**Examples of commands:**
```
npm install          --> Download code libraries
npm run build        --> Compile your website
git status           --> See what files changed
python app.py        --> Run a Python program
```

**Example in action:**
```
You say: "Run the tests"
AI uses Bash: npm test
Result: Shows which tests pass/fail
```

**Safety note:** This tool can do powerful things, so it asks permission first!

---

### Tool 5: Glob (The Searcher - By Name)

**What it does:** Finds files by their NAME pattern

**Like:** Looking for all books with "Harry Potter" in the title

**Example patterns:**
```
*.js          --> All files ending in .js
src/**/*.tsx  --> All .tsx files in src folder and subfolders
test_*.py     --> All Python files starting with "test_"
```

**Example in action:**
```
You say: "Show me all the test files"
AI uses Glob: test_*.py
Result:
  - test_login.py
  - test_signup.py
  - test_payment.py
```

---

### Tool 6: Grep (The Searcher - By Content)

**What it does:** Finds files containing specific TEXT inside them

**Like:** Searching for which book mentions "Voldemort"

**Example:**
```
You say: "Where do we use the login function?"
AI uses Grep: search for "login("
Result:
  - app.py line 45: user = login(username, password)
  - test_login.py line 12: result = login("test", "123")
```

**Glob vs Grep:**
- **Glob**: Searches file NAMES (what files are called)
- **Grep**: Searches file CONTENTS (what's inside files)

---

### Tool 7: WebFetch (The Browser)

**What it does:** Gets information from a website

**Like:** Looking up something on the internet

**Example:**
```
You say: "Check the React documentation for hooks"
AI uses WebFetch: https://react.dev/reference/react/hooks
Result: AI reads the webpage and summarizes it
```

---

### Tool 8: WebSearch (The Google)

**What it does:** Searches the internet for answers

**Like:** Googling something

**Example:**
```
You say: "How do I fix this Python error?"
AI uses WebSearch: "Python AttributeError NoneType"
Result: Finds Stack Overflow answers and documentation
```

---

### Tool 9: Task (The Helper)

**What it does:** Creates a "mini AI assistant" for complex jobs

**Like:** Asking a friend to help with part of a big project

**When it's used:**
- Searching through lots of files
- Doing research that takes many steps
- Working on something while you do something else

**Example:**
```
You say: "Find all the places where we handle errors"
AI uses Task: Creates a helper to search the entire codebase
Result: Comes back with a complete list
```

---

### Tool 10: TodoWrite (The Checklist)

**What it does:** Keeps track of tasks the AI is working on

**Like:** A to-do list that shows what's done and what's left

**Example:**
```
You say: "Add login, signup, and password reset"

AI creates todo list:
  [ ] Add login functionality
  [ ] Add signup functionality
  [ ] Add password reset functionality

As AI works:
  [x] Add login functionality       <-- Done!
  [>] Add signup functionality      <-- Working on this
  [ ] Add password reset functionality
```

---

# Part 3: How The Code Is Organized

## OpenCode Folder Structure (Simplified)

```
opencode/
|
+-- packages/              <-- All the main code lives here
|   |
|   +-- opencode/          <-- THE CORE (most important!)
|   |   +-- src/
|   |       +-- tool/      <-- All the tools (Read, Write, Bash, etc.)
|   |       +-- agent/     <-- The AI brain configuration
|   |       +-- session/   <-- Conversation management
|   |       +-- provider/  <-- Connections to Claude, OpenAI, etc.
|   |
|   +-- app/               <-- Web interface components
|   +-- desktop/           <-- Desktop app (like VS Code)
|   +-- docs/              <-- Documentation website
|
+-- README.md              <-- Start here!
+-- CONTRIBUTING.md        <-- How to help improve OpenCode
```

---

## Understanding a Tool File

Let's look at a real tool file and understand it:

**File: `packages/opencode/src/tool/read.ts`**

```typescript
// This is the "Read" tool - it lets AI look at files

// 1. WHAT INFO THE TOOL NEEDS (inputs)
const parameters = {
  file_path: "The file to read",      // Required: which file?
  offset: "Start from which line?",    // Optional: skip to line 50
  limit: "How many lines to read?"     // Optional: just read 100 lines
}

// 2. WHAT THE TOOL DOES
async function execute(params) {
  // Open the file
  const content = await readFile(params.file_path)

  // Return the content to AI
  return content
}
```

**In simple terms:**
1. AI says: "I want to read file X"
2. Tool opens file X
3. Tool sends content back to AI
4. AI now knows what's in the file!

---

## Understanding Agents

**What's an Agent?**

An agent is like a "personality mode" for the AI.

**OpenCode has 2 built-in agents:**

| Agent | Personality | Can Do | Can't Do |
|-------|-------------|--------|----------|
| **build** | The Worker | Edit files, run commands, make changes | - |
| **plan** | The Thinker | Read files, search, analyze | Edit files (asks first) |

**Why have different agents?**

- **build**: When you want to actually make changes
- **plan**: When you want to explore without breaking anything

**Example:**
```
Using "build" agent:
  You: "Add a dark mode toggle"
  AI: *directly edits your CSS and adds the button*

Using "plan" agent:
  You: "How would I add dark mode?"
  AI: *reads your code, explains the approach, asks before changing*
```

---

# Part 4: The Flow (Putting It All Together)

## Example: "Add a login button"

Here's exactly what happens when you ask the AI to add a login button:

```
STEP 1: You type your request
+------------------------------------------+
|  You: "Add a login button to the header" |
+------------------------------------------+
              |
              v
STEP 2: AI reads your files to understand the project
+------------------------------------------+
|  AI uses: Glob tool                      |
|  Searches for: *.html, *.css, *.js       |
|  Finds: index.html, header.html, etc.    |
+------------------------------------------+
              |
              v
STEP 3: AI reads the specific file it needs to change
+------------------------------------------+
|  AI uses: Read tool                      |
|  Reads: header.html                      |
|  Sees: <nav>Home | About | Contact</nav> |
+------------------------------------------+
              |
              v
STEP 4: AI plans what to change
+------------------------------------------+
|  AI thinks:                              |
|  "I need to add a button after Contact"  |
|  "I should also add some CSS styling"    |
+------------------------------------------+
              |
              v
STEP 5: AI makes the changes
+------------------------------------------+
|  AI uses: Edit tool on header.html       |
|  Changes: <nav>Home|About|Contact</nav>  |
|  To:      <nav>Home|About|Contact|       |
|           <button>Login</button></nav>   |
+------------------------------------------+
              |
              v
STEP 6: AI might add styles too
+------------------------------------------+
|  AI uses: Edit tool on styles.css        |
|  Adds: .login-btn { color: blue; }       |
+------------------------------------------+
              |
              v
STEP 7: AI tells you what it did
+------------------------------------------+
|  AI: "I added a login button to the      |
|  header in header.html and styled it     |
|  in styles.css"                          |
+------------------------------------------+
```

---

# Part 5: How to Learn More

## Step-by-Step Learning Path

### Week 1: Terminal Basics
1. Open your terminal
2. Learn these 5 commands:
   - `ls` - list files
   - `cd folder` - go into a folder
   - `cd ..` - go back up
   - `pwd` - where am I?
   - `cat file.txt` - show file contents

### Week 2: Git Basics
1. Learn what git does (version control)
2. Learn these commands:
   - `git status` - what changed?
   - `git add .` - stage changes
   - `git commit -m "message"` - save changes
   - `git push` - upload to GitHub

### Week 3: Read OpenCode Source
1. Start with `packages/opencode/src/tool/read.ts`
2. Then `bash.ts`, `write.ts`, `edit.ts`
3. Look at the `.txt` files - they're the instructions!

### Week 4: Try Running OpenCode
1. Install Bun: https://bun.sh
2. Run: `bun install`
3. Run: `bun dev`
4. Try talking to it!

---

## Quick Reference Card

### The 10 Tools Summary

| Tool | Does What | Like... |
|------|-----------|---------|
| Read | See file contents | Opening a book |
| Write | Create/replace files | Writing new page |
| Edit | Change part of file | Using eraser |
| Bash | Run commands | Telling computer to DO something |
| Glob | Find files by name | Looking for books by title |
| Grep | Find files by content | Searching inside books |
| WebFetch | Get webpage | Opening a website |
| WebSearch | Search internet | Using Google |
| Task | Create helper AI | Asking friend to help |
| TodoWrite | Track progress | Making a checklist |

### Common Patterns

```
"Read a file"        --> AI uses Read
"Search for X"       --> AI uses Grep or Glob
"Change this code"   --> AI uses Edit
"Create a new file"  --> AI uses Write
"Run the tests"      --> AI uses Bash
"Look this up"       --> AI uses WebSearch
```

---

## Still Confused?

That's okay! Here's what to do:

1. **Try it yourself** - Nothing beats hands-on practice
2. **Ask questions** - Use Claude Code or OpenCode to explain code
3. **Read slowly** - Start with one tool, understand it fully
4. **Build something** - Make a simple project with AI help

Remember: Everyone was a beginner once. The experts just practiced more!

---

*This guide was created to help beginners understand how AI coding assistants work.*
*Updated: January 2026*
