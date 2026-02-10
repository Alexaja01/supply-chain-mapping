# NEW SESSION TEMPLATE - Starting Fresh with Claude

**How to Get the Best Help from Claude in Future Sessions**

This template helps you start new conversations about this project with all the right context.

Last Updated: February 10, 2026

---

## 🎯 Quick Start

When starting a new Claude session about this project:

### Essential Upload

**Always upload:**
1. **PROJECT_STATE.md** - Shows where you are now
2. **The specific file you're working on** - The code/doc you want help with

**Optional but helpful:**
3. **DEVELOPMENT_GUIDE.md** - If you need technical reference
4. **Error screenshot** - If troubleshooting

### Good Opening Message

```
Hi Claude! I'm working on the supply chain mapping project.

[Upload PROJECT_STATE.md]

I want to [specific goal]. Can you help me [specific action]?

[If relevant: Here's the error I'm getting: ...]
```

---

## 📋 COMPLETE TEMPLATE

**Copy and customize this template for each new session:**

---

### 📌 Project Context

Hi Claude! I'm working on an agent-driven supply chain mapping project.

**Project:** Autonomous system using Claude AI to map US refined products supply chain  
**Tech Stack:** Python 3, Claude API (Sonnet 4), SQLite  
**Location:** `C:\Users\jalex\supply-chain\supply-chain-mapping`  

**Current Status:** [Choose one]
- [ ] Just set up, starting to populate data
- [ ] Have some data, working on new agents
- [ ] System running, need improvements/fixes
- [ ] Other: _______________

---

### 📎 What I've Uploaded

- [ ] **PROJECT_STATE.md** - Current status and next steps
- [ ] **DEVELOPMENT_GUIDE.md** - Technical reference
- [ ] **The file I'm working on:** _______________
- [ ] **Error screenshot/message** (if troubleshooting)
- [ ] **Sample data** (if relevant)

---

### 🎯 What I Want to Accomplish

**Goal:** [Be specific!]

**Examples:**
- Build a pipeline tariff agent that extracts FERC tariffs
- Fix bug where orchestrator crashes on status command
- Import my existing Excel data (200+ terminals) into database
- Add error handling to terminal discovery agent
- Create a review dashboard for flagged items
- Optimize database queries for better performance

**My specific goal today:**
[Write your goal here]

---

### ❓ Specific Questions/Issues

**Question 1:**
[Your first question]

**Question 2:**
[Your second question]

**Error message (if any):**
```
[Paste full error here]
```

---

### 📊 Current Project State Summary

*Fill this in from PROJECT_STATE.md or leave blank if you uploaded the file*

**Data:**
- Terminals: _____
- Pipelines: _____
- Tariffs: _____

**Agents Built:**
- [ ] Terminal Discovery (working)
- [ ] Excel Import
- [ ] Pipeline Tariff
- [ ] Other: _____

**What's Working:**
- [List what works]

**What's Not Working:**
- [List issues/blockers]

---

## 🎓 EXAMPLES OF GOOD SESSION STARTS

### Example 1: Building a New Agent

```
Hi Claude! I'm working on the supply chain mapping project.

[Upload: PROJECT_STATE.md, terminal_discovery_agent.py]

I want to build a pipeline tariff agent that:
1. Searches FERC eTariff database for new pipeline filings
2. Downloads tariff PDFs
3. Extracts rate tables using your help
4. Stores rates in the database

I've uploaded terminal_discovery_agent.py as an example of the pattern
I want to follow. Can you help me build the pipeline tariff agent
following the same structure?
```

**Why this is good:**
- ✅ Provides context (PROJECT_STATE.md)
- ✅ Shows example pattern (terminal_discovery_agent.py)
- ✅ Specific about what the agent should do
- ✅ Clear steps listed

---

### Example 2: Fixing a Bug

```
Hi Claude! I'm working on the supply chain mapping project.

[Upload: PROJECT_STATE.md, orchestrator.py]

The orchestrator is crashing when I run the status command.

Error message:
```
sqlite3.OperationalError: no such table: v_active_terminals
```

I think the database views aren't being created properly. Can you help
me debug this?
```

**Why this is good:**
- ✅ Context provided
- ✅ Specific problem stated
- ✅ Full error message included
- ✅ Uploaded relevant file
- ✅ Has a hypothesis

---

### Example 3: Importing Data

```
Hi Claude! I'm working on the supply chain mapping project.

[Upload: PROJECT_STATE.md, Costing_Data_Final.xlsx, create_database.py]

I have existing Excel data with 200+ terminals that I want to import
into the database. 

The Excel has these sheets:
- Shipping Line Items (terminal rates)
- Paths and Tariffs (pipeline connections)
- Tariff Cross Reference (source docs)

Can you help me build an Excel import agent that reads this data and
loads it into the database tables? I've uploaded the Excel file and
the database schema.
```

**Why this is good:**
- ✅ Context provided
- ✅ Data source explained
- ✅ Schema provided for mapping
- ✅ Clear deliverable (import agent)

---

### Example 4: Improving Existing Code

```
Hi Claude! I'm working on the supply chain mapping project.

[Upload: PROJECT_STATE.md, terminal_discovery_agent.py]

The terminal discovery agent works but I want to improve it:
1. Add retry logic for failed API calls
2. Better error handling when PDFs can't be parsed
3. Logging to file instead of just console

Can you show me how to add these improvements while keeping the
existing structure?
```

**Why this is good:**
- ✅ Context provided
- ✅ Current code uploaded
- ✅ Specific improvements listed
- ✅ Wants to maintain existing patterns

---

## ❌ EXAMPLES OF SESSIONS THAT NEED IMPROVEMENT

### Bad Example 1: Too Vague

```
Help me with my project
```

**Why this is bad:**
- ❌ No context - Claude doesn't know what project
- ❌ No files uploaded
- ❌ Not specific about what help is needed

**Better version:**
```
I'm working on the supply chain mapping system (PROJECT_STATE.md
uploaded). The orchestrator is giving me an error. Can you help me
debug it?

[Upload PROJECT_STATE.md + orchestrator.py + error screenshot]
```

---

### Bad Example 2: Too Much at Once

```
Hi, I need you to:
1. Build 5 new agents
2. Create a web dashboard
3. Optimize the database
4. Set up automated deployment
5. Add machine learning
All in this session.
```

**Why this is bad:**
- ❌ Unrealistic scope for one session
- ❌ No priorities
- ❌ Would take many hours

**Better version:**
```
I want to build the pipeline tariff agent first (high priority).
After that works, I'll come back for the rail rate agent.

Can you help me build the pipeline tariff agent?
```

---

### Bad Example 3: Missing Key Info

```
My code doesn't work. Fix it.
```

**Why this is bad:**
- ❌ Didn't upload the code
- ❌ No error message
- ❌ No context about what "doesn't work" means

**Better version:**
```
My orchestrator.py crashes when I run it. Here's the error:
[paste error]

I've uploaded the file. Can you help me find the bug?

[Upload PROJECT_STATE.md + orchestrator.py]
```

---

## 🎯 SESSION TYPES & WHAT TO UPLOAD

### Building a New Agent

**Upload:**
- PROJECT_STATE.md
- terminal_discovery_agent.py (as template)
- Any sample data for the agent to process

**Ask for:**
- Complete agent file following the pattern
- Integration with orchestrator
- Test examples

---

### Fixing a Bug

**Upload:**
- PROJECT_STATE.md
- The file with the bug
- Error screenshot/message

**Ask for:**
- Explanation of what's wrong
- Fix with explanation
- How to prevent similar bugs

---

### Importing/Processing Data

**Upload:**
- PROJECT_STATE.md
- create_database.py (shows schema)
- Sample of data file (Excel, CSV, PDF)

**Ask for:**
- Mapping between data and database
- Import script or agent
- Validation logic

---

### Creating Reports/Dashboards

**Upload:**
- PROJECT_STATE.md
- Sample data or database schema
- Example of desired output (if you have one)

**Ask for:**
- Query examples
- Visualization code
- Report templates

---

### Improving Performance

**Upload:**
- PROJECT_STATE.md
- The slow code
- Performance metrics (if you have them)

**Ask for:**
- Performance analysis
- Optimization suggestions
- Benchmarking approach

---

## 💡 TIPS FOR EFFECTIVE SESSIONS

### DO:
✅ Start with PROJECT_STATE.md for context  
✅ Upload specific files you're working with  
✅ Paste exact error messages  
✅ Describe what you've already tried  
✅ Be specific about what you want  
✅ Ask follow-up questions if unclear  
✅ Test Claude's suggestions before moving on  

### DON'T:
❌ Expect Claude to remember previous conversations  
❌ Upload dozens of files (be selective)  
❌ Ask vague questions like "make it better"  
❌ Skip context (always provide PROJECT_STATE.md)  
❌ Forget to test the solutions  
❌ Move on before understanding the answer  

---

## 🔄 MULTI-TURN SESSIONS

### First Message
```
Hi Claude! I'm working on the supply chain mapping project.
[Upload PROJECT_STATE.md]

I want to build a pipeline tariff agent. Can you help?
```

### Follow-Up Messages
```
Thanks! That looks good. Now can you add error handling for
when the PDF can't be parsed?
```

```
Perfect. How do I integrate this with the orchestrator?
```

```
Great! Can you show me how to test this?
```

**Key:** Build incrementally, test each piece, then add more.

---

## 📝 AFTER THE SESSION CHECKLIST

After working with Claude:

- [ ] Test that the changes work
- [ ] Update PROJECT_STATE.md with what changed
- [ ] Commit to GitHub (or backup your files)
- [ ] Document any new learnings in DEVELOPMENT_GUIDE.md
- [ ] Note any follow-up tasks for next session

**This helps future you pick up where you left off!**

---

## 🎯 SESSION GOALS BY SIZE

### Small Task (30 minutes)
- Fix one specific bug
- Add one feature to existing code
- Create one simple query
- Improve one function

**Upload:** PROJECT_STATE.md + 1-2 files

---

### Medium Task (1-2 hours)
- Build complete new agent
- Import and clean dataset
- Add major feature to orchestrator
- Create basic dashboard

**Upload:** PROJECT_STATE.md + 3-4 files + examples

---

### Large Task (Multiple Sessions)
- Integrate all Excel data
- Build complete review workflow
- Create production deployment
- Implement advanced features

**Approach:** Break into smaller tasks, multiple sessions

Start small, build confidence, then tackle bigger projects!

---

## 🆘 WHEN THINGS GO WRONG

### If Claude's Solution Doesn't Work

**Don't just say:** "That didn't work"

**Instead say:**
```
I tried your suggestion but got this error:
[paste exact error]

Here's what I did:
1. [Step 1]
2. [Step 2]
3. [Error appeared at step 3]

What should I try next?
```

---

### If You're Confused

**Don't just say:** "I don't understand"

**Instead say:**
```
I'm not sure I understand the approach you suggested.

Can you:
1. Explain in simpler terms why this approach works?
2. Show me a smaller example?
3. Break it into smaller steps?
```

---

### If You Disagree with Approach

**Don't just say:** "That won't work"

**Instead say:**
```
I'm concerned this approach might be too slow because our
dataset has 500+ terminals and this would query each one
individually.

What if we did X instead? Or is there a way to batch this?
```

---

## 📚 REFERENCE: KEY FILES TO UPLOAD

### Always Helpful:
- **PROJECT_STATE.md** - Current status
- **README.md** - High-level overview

### For Building New Agents:
- **terminal_discovery_agent.py** - Example pattern
- **orchestrator.py** - See how to integrate
- **agent_driven_framework.md** - Templates
- **DEVELOPMENT_GUIDE.md** - Best practices

### For Database Work:
- **create_database.py** - Schema definition
- **config.py** - Path configuration
- Example queries or data

### For Troubleshooting:
- **The file with the error**
- **Error message/screenshot**
- **What you were trying to do**

---

## 🎉 YOU'RE READY!

Save this template and use it every time you start a new Claude session.

**The pattern:**
1. Upload PROJECT_STATE.md
2. Tell Claude what you want to accomplish
3. Upload relevant files
4. Be specific
5. Test the solutions
6. Update PROJECT_STATE.md

**This ensures every session is productive!**

---

## 📞 REMEMBER

**PROJECT_STATE.md is your "save game" file**

Always upload it to give Claude context about:
- What's already built
- What's working vs. not working
- What you're trying to accomplish next
- Lessons learned

**With good context, Claude can help you 10x faster!**

---

Good luck with your supply chain mapping project! 🚀

*Last updated: February 10, 2026*
