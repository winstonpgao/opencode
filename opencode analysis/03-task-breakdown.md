# Task Breakdown - How AI Splits Complex Tasks

## The Big Question

**How does the AI know to break "Add user authentication" into 20 steps instead of trying to do it all at once?**

Answer: **The system prompt teaches it a structured approach!**

## Simple Analogy

Imagine you're asked to "make dinner for 10 people":

**Beginner approach (fails):**
```
1. Make dinner ← Too vague! Overwhelmed!
```

**Expert approach (succeeds):**
```
1. Plan the menu
2. Check what ingredients we have
3. Make shopping list for missing items
4. Go shopping
5. Prepare ingredients (wash, chop)
6. Cook main course
7. Cook side dishes
8. Set table
9. Serve food
```

The AI does the same thing with coding tasks!

## How Task Breakdown Works

### Step 1: Analyze the Request

When you ask something complex like: **"Add authentication to my app"**

The AI's thought process (guided by prompt):
```
1. What does "authentication" involve?
   - Login page
   - User database
   - Password hashing
   - Session management
   - Middleware
   - Logout functionality

2. What do I need to know first?
   - What framework is this? (React? Express?)
   - Is there existing auth code?
   - What database do we use?

3. Break into logical steps
```

### Step 2: Use TodoWrite

The prompt tells AI:
```
For complex tasks (3+ steps):
1. Use TodoWrite to create a task list
2. Mark tasks as: pending, in_progress, completed
3. Only ONE task should be in_progress at a time
4. Update the list as you go
```

AI creates a plan:
```typescript
TodoWrite([
  {content: "Explore existing auth code", status: "pending"},
  {content: "Create login page component", status: "pending"},
  {content: "Add auth API endpoints", status: "pending"},
  {content: "Set up password hashing", status: "pending"},
  {content: "Add session middleware", status: "pending"},
  {content: "Create logout functionality", status: "pending"},
  {content: "Write tests", status: "pending"}
])
```

### Step 3: Execute Step by Step

```
AI marks first task as in_progress:
TodoWrite([
  {content: "Explore existing auth code", status: "in_progress"},
  ...
])

AI executes:
- Glob("**/auth*.{ts,tsx}")
- Grep(pattern="authentication")
- Read found files

AI completes and moves to next:
TodoWrite([
  {content: "Explore existing auth code", status: "completed"},
  {content: "Create login page component", status: "in_progress"},
  ...
])
```

## Breakdown Strategies

### Strategy 1: Top-Down (Feature-Based)

**User request:** "Add a blog to my website"

**AI breakdown:**
```
1. Research & Planning Phase
   ├─ Explore existing code structure
   ├─ Check what frameworks we're using
   └─ Decide on blog architecture

2. Data Layer
   ├─ Create blog post database schema
   ├─ Set up migration
   └─ Add blog post model

3. API Layer
   ├─ Create GET /api/posts endpoint
   ├─ Create POST /api/posts endpoint
   ├─ Create PUT /api/posts/:id endpoint
   └─ Create DELETE /api/posts/:id endpoint

4. UI Layer
   ├─ Create blog list component
   ├─ Create blog post component
   ├─ Create blog editor component
   └─ Add routing

5. Testing & Verification
   ├─ Write API tests
   ├─ Write component tests
   └─ Manual testing
```

### Strategy 2: Bottom-Up (Dependency-Based)

**User request:** "Fix the broken checkout process"

**AI breakdown:**
```
1. Investigation
   ├─ Read checkout component
   ├─ Read payment integration code
   └─ Check error logs

2. Identify Root Cause
   ├─ Find where error occurs
   ├─ Understand why it fails
   └─ Check dependencies

3. Fix Dependencies First (if needed)
   ├─ Fix payment API integration
   └─ Update environment variables

4. Fix Main Issue
   ├─ Update checkout logic
   └─ Add error handling

5. Test
   ├─ Run unit tests
   └─ Test manually
```

### Strategy 3: Iterative (Agile-Style)

**User request:** "Improve the app's performance"

**AI breakdown:**
```
Iteration 1: Measure
├─ Run performance profiler
├─ Identify slowest parts
└─ List optimization opportunities

Iteration 2: Quick Wins
├─ Add React.memo to heavy components
├─ Implement lazy loading
└─ Test improvements

Iteration 3: Deep Optimizations
├─ Optimize database queries
├─ Add caching layer
└─ Test improvements

Iteration 4: Verify
├─ Run performance tests
└─ Compare before/after metrics
```

## Prompt Instructions for Task Breakdown

### From `anthropic.txt`:

```markdown
## Task Management

Use TodoWrite tool for:
- Complex tasks with 3+ steps
- Non-trivial tasks requiring planning
- When user provides multiple tasks

Task tracking:
1. Create task list BEFORE starting work
2. Mark ONE task as in_progress
3. Complete the task
4. Mark it completed IMMEDIATELY
5. Move to next task

Example:
User: "Add dark mode"

You should:
1. TodoWrite: Create task list
2. Start first task (mark in_progress)
3. Do the work
4. Mark completed
5. Move to next task
```

### From `beast.txt` (GPT prompt):

```markdown
## Structured Problem Solving

Before executing:
1. Break down the task into steps
2. Identify dependencies
3. Plan order of execution
4. Execute step by step
5. Verify after each step

Avoid doom loops:
- Don't repeat same action 3+ times
- If stuck, break down further
- Ask for help if needed
```

## Real Example: Complete Breakdown

**User Request:** "Create a Todo app with React and Express"

### AI's Internal Process

**Phase 1: Understanding**
```
AI analyzes request:
- Frontend: React
- Backend: Express
- Feature: Todo CRUD operations
- Complexity: Medium-High (10+ steps)

Decision: Use TodoWrite to plan
```

**Phase 2: Todo List Creation**
```typescript
TodoWrite([
  // Setup Phase
  {
    content: "Explore existing project structure",
    status: "pending",
    activeForm: "Exploring existing project structure"
  },
  {
    content: "Check installed dependencies",
    status: "pending",
    activeForm: "Checking installed dependencies"
  },

  // Backend Phase
  {
    content: "Create Todo model/schema",
    status: "pending",
    activeForm: "Creating Todo model/schema"
  },
  {
    content: "Create Express API routes",
    status: "pending",
    activeForm: "Creating Express API routes"
  },
  {
    content: "Add database integration",
    status: "pending",
    activeForm: "Adding database integration"
  },

  // Frontend Phase
  {
    content: "Create Todo list component",
    status: "pending",
    activeForm: "Creating Todo list component"
  },
  {
    content: "Create Todo item component",
    status: "pending",
    activeForm: "Creating Todo item component"
  },
  {
    content: "Add API service layer",
    status: "pending",
    activeForm: "Adding API service layer"
  },
  {
    content: "Connect components to API",
    status: "pending",
    activeForm: "Connecting components to API"
  },

  // Testing Phase
  {
    content: "Write API tests",
    status: "pending",
    activeForm: "Writing API tests"
  },
  {
    content: "Test full application",
    status: "pending",
    activeForm: "Testing full application"
  }
])
```

**Phase 3: Execution**
```
Step 1: Mark first task in_progress
AI: Glob("**/{package.json,tsconfig.json,src/**}")

Step 2: Complete exploration
AI: TodoWrite([...update first to completed, second to in_progress...])

Step 3: Check dependencies
AI: Read("package.json")
AI: Bash("npm list")

[Continues through all tasks...]
```

## When NOT to Break Down Tasks

The prompt also teaches when to keep it simple:

```
DON'T use TodoWrite for:
- Single, straightforward tasks
- Trivial changes (fixing typo)
- Tasks completable in 1-2 steps
- Simple questions/explanations
```

**Example:**
```
User: "Fix the typo in README.md"

AI should:
✅ Read("README.md")
✅ Edit(file, old, new)
❌ DON'T create todo list (too simple!)
```

## Adaptive Breakdown

The AI adjusts based on complexity:

### Simple Request
```
User: "Change port to 3000"

No breakdown needed:
1. Read config file
2. Edit the port
3. Done
```

### Medium Request
```
User: "Add error handling to the API"

Small breakdown (3-5 tasks):
1. Find all API endpoints
2. Add try-catch blocks
3. Create error response format
4. Update each endpoint
5. Test
```

### Complex Request
```
User: "Migrate from REST to GraphQL"

Large breakdown (15+ tasks):
1. Research existing REST endpoints
2. Plan GraphQL schema
3. Install GraphQL dependencies
4. Create GraphQL server
5. Define type definitions
6. Create resolvers
7. Migrate endpoint 1
8. Migrate endpoint 2
   [... more endpoints ...]
15. Update frontend to use GraphQL
16. Write tests
17. Remove old REST code
```

## Breakdown Triggers

What makes AI decide to break down a task?

### Trigger 1: Multiple Verbs
```
User: "Create, test, and deploy the feature"
       ^^^^^^  ^^^^  ^^^^^^^^^^^
       3 verbs = 3+ tasks → Use TodoWrite
```

### Trigger 2: Complex Domain
```
User: "Add authentication"
      ↓
      AI knows: Auth is complex
      - Login, logout, session, middleware, security
      → Use TodoWrite
```

### Trigger 3: Multiple Files
```
User: "Refactor the user system"
      ↓
      AI searches: finds 10 files related to users
      → Use TodoWrite (track changes across files)
```

### Trigger 4: User Provides List
```
User: "I need: 1) login page, 2) dashboard, 3) settings"
      ↓
      Explicit list = TodoWrite
```

### Trigger 5: Uncertainty
```
User: "Make the app better"
      ↓
      Vague request → Ask question first
      Then create breakdown based on answer
```

## Progress Tracking

The AI keeps you informed:

```
Todo list state:
✓ Create database schema
✓ Add API endpoints
→ Create frontend components (in progress)
  - Write tests
  - Deploy

AI output:
"I've completed the database schema and API endpoints.
Now working on the frontend components..."
```

## Doom Loop Prevention

The prompt includes protection against infinite loops:

```markdown
Doom Loop Detection:
- If AI repeats same tool call 3+ times
- System detects the loop
- Breaks execution
- AI must try different approach

Example of doom loop:
Grep("function login")  → No results
Grep("function login")  → No results
Grep("function login")  → STOPPED! Try different search
```

**Better approach:**
```
Grep("function login")  → No results
Grep("login")  → Broader search
Glob("**/login*")  → Find login files
Read files → Find the function
```

## Summary

**How tasks are broken down:**

1. **Analysis** - Understand complexity
2. **TodoWrite** - Create structured plan
3. **Sequential Execution** - One step at a time
4. **Progress Updates** - Mark completed immediately
5. **Adaptive** - Adjust if issues arise

**Key principles:**
- Complex tasks (3+ steps) → TodoWrite
- Simple tasks → Just do it
- Always update progress
- One task in_progress at a time
- Break down further if stuck

**The magic:** The system prompt teaches these strategies, and the AI follows them consistently!

Next: Read [04-agent-system.md](04-agent-system.md) to understand different types of agents!
