# 🚀 BEGINNER'S GUIDE - Supply Chain Mapping System

**No Tech Experience Required!**

This guide will walk you through using the supply chain mapping system, step by step. Everything is explained in plain language.

Last Updated: February 10, 2026

---

## 📋 TABLE OF CONTENTS

1. [What This System Does](#what-this-system-does)
2. [What You Need](#what-you-need)
3. [One-Time Setup](#one-time-setup)
4. [Daily Usage](#daily-usage)
5. [Understanding the Results](#understanding-the-results)
6. [Common Problems & Solutions](#common-problems--solutions)
7. [Getting Help](#getting-help)

---

## 🎯 What This System Does

Think of this system as a **smart assistant** that automatically:

- 📍 **Finds terminals** across the US (places where fuel is stored)
- 🚰 **Tracks pipelines** connecting refineries to terminals
- 🚂 **Monitors rail rates** for transporting fuel
- 💰 **Collects tariffs** (pricing for transportation)
- ✅ **Validates everything** to make sure data is accurate

**Instead of you spending 65 hours/week doing this manually**, the AI does it in minutes and only asks for your help when it's unsure about something.

**Your job:** Spend 10-15 hours/week reviewing what the AI found and making sure it looks correct.

**Savings:** About $70,000-110,000 per year compared to hiring someone to do it manually!

---

## 🧰 What You Need

### Required (Must Have)
1. ✅ **Computer** - Windows, Mac, or Linux
2. ✅ **Internet connection**
3. ✅ **Anthropic API Key** - This is like a password that lets you use Claude AI
   - Get one at: https://console.anthropic.com/
   - Costs about $5 to start, then ~$400-500/month when running
4. ✅ **The project files** - You already have these!

### Optional (Nice to Have)
- External hard drive (for backups)
- Second monitor (easier to review data)
- Spreadsheet software (Excel, Google Sheets)

---

## ⚙️ ONE-TIME SETUP (Do This Once - Takes 30 Minutes)

### Step 1: Get Your API Key (5 minutes)

1. **Go to:** https://console.anthropic.com/
2. **Sign up** for an account (or log in if you have one)
3. **Click:** "API Keys" in the menu
4. **Click:** "Create Key"
5. **Copy the key** - it starts with `sk-ant-api03-...`
6. **Save it** somewhere safe (you'll need it in Step 5)

💡 **Cost:** Add $5 to start. You'll use about $10-15 per day when running regularly.

---

### Step 2: Check Python is Installed (2 minutes)

**Windows:**
1. Press **Windows key**
2. Type **cmd**
3. Press **Enter**
4. In the black window, type: `python --version`
5. Press **Enter**

**You should see:** `Python 3.x.x`

**If you see an error:**
1. Go to: https://www.python.org/downloads/
2. Download Python
3. **IMPORTANT:** During install, check "Add Python to PATH"
4. Install and restart your computer

**Mac:**
- Python is already installed! Skip this step.

---

### Step 3: Install Claude AI Library (2 minutes)

In the same command window from Step 2:

**Type:**
```
pip install anthropic
```

**Press:** Enter

**Wait** for it to finish (about 30 seconds)

**You should see:** `Successfully installed anthropic`

✅ **Done!**

---

### Step 4: Find Your Project Folder (1 minute)

Your project files are in:
```
C:\Users\jalex\supply-chain\supply-chain-mapping
```

**To get there:**
1. Open **File Explorer** (Windows + E)
2. Type in the address bar: `C:\Users\jalex\supply-chain\supply-chain-mapping`
3. Press **Enter**

**You should see files like:**
- config.py
- orchestrator.py
- terminal_discovery_agent.py
- README.md
- And more!

---

### Step 5: Test Everything Works (5 minutes)

**Open Command Prompt/Terminal:**
- Windows: Press Windows key → type `cmd` → Enter
- Mac: Press Cmd+Space → type `terminal` → Enter

**Go to your project folder:**
```
cd C:\Users\jalex\supply-chain\supply-chain-mapping
```

**Test the setup:**
```
python getting_started_simple.py YOUR_API_KEY
```
(Replace YOUR_API_KEY with your actual key from Step 1)

**What you'll see:**
```
✅ Complete database created: supply_chain.db
✅ API key is valid!
✅ Setup Complete!
```

**If it works:** Perfect! You're ready! 🎉

**If it doesn't work:** See [Common Problems](#common-problems--solutions) below

---

### Step 6: Set Up Easy Double-Click (10 minutes) - OPTIONAL BUT RECOMMENDED

Instead of typing commands, you can just **double-click** a file!

**See:** [EASY_DOUBLE_CLICK_GUIDE.md](EASY_DOUBLE_CLICK_GUIDE.md) for complete instructions.

**Quick version:**

**Windows:**
1. Right-click `run_daily_update.bat`
2. Choose **Edit**
3. Find line 22: `set API_KEY=YOUR_API_KEY_HERE`
4. Replace `YOUR_API_KEY_HERE` with your actual API key
5. **Save** and close

Now you can double-click `run_daily_update.bat` to run updates!

---

## 💼 DAILY USAGE (Takes 2-3 Minutes)

Once set up, here's your daily routine:

### Option A: Double-Click Method (Easiest!)

1. **Go to your project folder** in File Explorer
2. **Double-click:** `run_daily_update.bat` (Windows) or `run_daily_update.sh` (Mac)
3. **A window opens** and shows progress
4. **When done,** it shows what needs your review
5. **Close the window**

**That's it!** ✅

---

### Option B: Command Line Method

1. **Open command prompt/terminal**
2. **Type:**
   ```
   cd C:\Users\jalex\supply-chain\supply-chain-mapping
   ```
3. **Press Enter**
4. **Type:**
   ```
   python orchestrator.py --api-key YOUR_KEY daily
   ```
   (Use your actual API key)
5. **Press Enter**
6. **Wait 1-2 minutes** for it to finish

---

### What the Daily Update Does

Every day, the system:
- ✅ Checks for new pipeline tariffs posted by FERC
- ✅ Looks for ownership changes (companies buying/selling terminals)
- ✅ Runs quality checks on 50 random records
- ✅ Flags anything unusual for you to review

**Time:** 1-2 minutes to run  
**Cost:** About $0.30-0.50 per day  
**Your effort:** 2-3 minutes to run, plus review time if items flagged

---

## 📊 UNDERSTANDING THE RESULTS

### What You'll See After Running

```
================================================
   SUPPLY CHAIN MAPPING - DAILY UPDATE
================================================

Starting daily update...

✓ Created: PIPELINE_TARIFF_20260210_060000
✓ Created: OWNERSHIP_TRACKING_20260210_060001
✓ Created: QUALITY_ASSURANCE_20260210_060002

🔄 Processing 3 tasks...

  → PIPELINE_TARIFF_20260210_060000
    ✓ Completed - No new tariffs found

  → OWNERSHIP_TRACKING_20260210_060001
    ✓ Completed - No changes detected

  → QUALITY_ASSURANCE_20260210_060002
    ⚠️  Requires human review - Found 2 terminals with low confidence

================================================
   Update complete!
================================================

Checking for items needing your review...

📋 Review Queue (2 items):
1. Terminal "ABC Storage - Houston" - Missing city county
2. Terminal "XYZ Terminal - Chicago" - Operator name unclear

Press any key to close...
```

---

### What Each Symbol Means

✅ **Green Checkmark** = Everything good, no action needed

⚠️ **Yellow Warning** = Something needs your attention

❌ **Red X** = Error occurred, task failed

🔄 **Blue Circle** = Working on it...

---

### What "Requires Human Review" Means

The AI is **smart but cautious**. When it finds data but isn't 100% sure, it asks you to check.

**Examples:**
- Found a terminal name but couldn't find the exact address
- Found a tariff rate but the PDF was poorly scanned
- Data conflicts with what's already in the database

**What to do:** See the "Weekly Review" section below

---

## 📅 WEEKLY REVIEW (Takes 1-2 Hours)

Once a week, you'll review items the AI flagged:

### Step 1: See What Needs Review

**Command:**
```
python orchestrator.py --api-key YOUR_KEY review
```

**You'll see a list like:**
```
📋 Items Needing Review (5 items):

1. Terminal Discovery - Houston TX terminal
   Issue: Missing county information
   Confidence: Medium (0.75)

2. Pipeline Tariff - Colonial Pipeline
   Issue: Effective date unclear in PDF
   Confidence: Low (0.65)

(etc.)
```

---

### Step 2: Check the Database

**Easy Way - Use a Free Tool:**

1. Download "DB Browser for SQLite" (free)
   - Go to: https://sqlitebrowser.org/dl/
   - Download and install

2. Open the program

3. Click **"Open Database"**

4. Select `supply_chain.db` from your project folder

5. Click **"Browse Data"** tab

6. From dropdown, select: **v_review_queue**

Now you can see all flagged items in a spreadsheet-like view!

---

### Step 3: Make Decisions

For each item:

**Look at what the AI found**
- Check the original source if needed (PDFs in tariff_library folder)
- Use your expertise to verify

**Decide:**
- ✅ **Accept** - Data looks good, mark as reviewed
- ✏️ **Correct** - Data needs small fix, update it
- ❌ **Reject** - Data is wrong, delete it

**Update the database** using DB Browser or by running correction scripts

---

### Step 4: Document Your Decisions

**Update PROJECT_STATE.md:**
- How many items reviewed
- How many accepted vs. corrected vs. rejected
- Any patterns noticed (same error repeating?)
- Notes for improving the AI agents

This helps track quality over time!

---

## 📈 CHECKING STATUS

Want to see how much data you have?

**Command:**
```
python orchestrator.py --api-key YOUR_KEY status
```

**You'll see:**
```
=== SUPPLY CHAIN STATUS ===

Database: supply_chain.db (2.4 MB)

Terminals: 147
Pipelines: 23
Pipeline Tariffs: 89
Rail Connections: 34
Tasks Completed: 234
Tasks Pending: 3

Automation Rate: 85%
Items Needing Review: 12

Last Update: 2026-02-10 08:30:15
```

---

## 🗂️ UNDERSTANDING YOUR FILES

### In Your Project Folder

**Python Files (The Brains):**
- `config.py` - All settings in one place
- `orchestrator.py` - Coordinates everything
- `terminal_discovery_agent.py` - Finds terminals
- `create_database.py` - Sets up the database

**Scripts (Easy to Run):**
- `run_daily_update.bat` - Double-click to run (Windows)
- `run_daily_update.sh` - Double-click to run (Mac)

**Database:**
- `supply_chain.db` - All your data stored here (back this up!)

**Documentation:**
- `README.md` - Project overview
- `PROJECT_STATE.md` - Current status
- `DEVELOPMENT_GUIDE.md` - Technical details
- `BEGINNERS_GUIDE.md` - This file!

**Reference Materials:**
- `reference/excel/` - Your previous Excel work
- `reference/sample_tariffs/` - Example PDFs

---

### Outside Your Project Folder

**Tariff Library:**
`C:\Users\jalex\supply-chain\tariff_library\`

This has ALL your tariff PDFs (100+). It's kept separate because it's large.

**Organized as:**
```
tariff_library/
├── pipelines/
│   ├── Colonial/
│   ├── BP_WHD/
│   └── ...
├── railroads/
│   ├── Union_Pacific/
│   └── ...
└── terminals/
```

---

## 🔄 MONTHLY MAINTENANCE (Takes 2-3 Hours)

Once a month:

### 1. Run Monthly Update
```
python orchestrator.py --api-key YOUR_KEY monthly
```

This does a **deep audit** of all data.

---

### 2. Check Performance Metrics

**How well is the system working?**

- Automation rate (target: 85%+)
- Data quality score (target: 95%+)
- Human review hours (target: <15/week)
- Cost per month (target: <$500)

**Document in PROJECT_STATE.md**

---

### 3. Backup Your Data

**Critical files to back up:**

1. `supply_chain.db` - Your database
2. Entire `tariff_library` folder
3. `config.py` - Your settings

**Where to back up:**
- External hard drive
- OneDrive / Google Drive
- USB stick

**Set a calendar reminder!** First of every month.

---

### 4. Update Documentation

Did anything change? Update:
- PROJECT_STATE.md - Current status
- DEVELOPMENT_GUIDE.md - If you learned new patterns
- This file - If process changed

Helps future you remember what you did!

---

## ❗ COMMON PROBLEMS & SOLUTIONS

### Problem: "Python is not recognized"

**What it means:** Python isn't installed or not in your system PATH

**Solution:**
1. Go to https://www.python.org/downloads/
2. Download Python
3. Run installer
4. **⚠️ IMPORTANT:** Check "Add Python to PATH" box
5. Finish installation
6. Restart computer
7. Try again

---

### Problem: "No module named 'anthropic'"

**What it means:** Claude AI library not installed

**Solution:**
```
pip install anthropic
```

Wait for it to finish, then try again.

---

### Problem: "API key invalid"

**What it means:** Your API key is wrong or expired

**Solution:**
1. Check you copied the FULL key (starts with `sk-ant-api03-`)
2. No spaces before or after the key
3. If still doesn't work, generate a new key at console.anthropic.com

---

### Problem: "Database is locked"

**What it means:** Another program has the database open

**Solution:**
1. Close DB Browser for SQLite (if open)
2. Close any Excel files viewing exported data
3. Close any other programs using the database
4. Try again

---

### Problem: "Could not find tariff PDF"

**What it means:** The system is looking for a PDF that moved or was renamed

**Solution:**
1. Check the tariff_library folder structure
2. Make sure PDFs are in correct operator folders
3. Check config.py has correct path to tariff_library

---

### Problem: "Permission denied"

**What it means:** Windows is blocking access to the file

**Solution:**
1. Right-click the file
2. Properties → Unblock
3. Apply and OK
4. Try again

---

## 📚 GETTING HELP

### Self-Help Resources

**Quick Reference:**
- QUICK_START_CHEATSHEET.txt - All commands in one page
- EASY_DOUBLE_CLICK_GUIDE.md - Simplest usage

**Technical Help:**
- DEVELOPMENT_GUIDE.md - Code examples and troubleshooting
- README.md - Complete overview

**Current Status:**
- PROJECT_STATE.md - Where you are, what's next

---

### Using Claude AI for Help

Claude (the AI) can help you!

1. **Go to:** claude.ai
2. **Start a chat**
3. **Upload:** PROJECT_STATE.md
4. **Say:** "I'm working on the supply chain mapping project. I need help with [your problem]."

Claude will understand your project and help!

---

### When to Ask for Human Help

**You should ask someone for help if:**

- You've tried solutions and nothing works
- You don't understand error messages
- You want to add new features
- Something broke and you don't know why

**Who to ask:**
- Technical team member
- Developer friend
- Claude AI (as described above)

---

## 🎯 QUICK WINS - Start Here!

### First Week Goals

**Day 1:** Complete setup (you probably already did this!)  
**Day 2:** Run your first daily update  
**Day 3:** Check the status, see what data you have  
**Day 4:** Set up double-click scripts  
**Day 5:** Review any flagged items  

**Success!** 🎉

---

### First Month Goals

- Run daily updates 5 days/week
- Complete 4 weekly reviews
- Import your existing Excel data (200+ terminals)
- Get comfortable with the review process
- Achieve 70%+ automation rate

---

## 🎓 UNDERSTANDING THE BIG PICTURE

### The Workflow

```
1. AI Agents Collect Data
   ↓
2. AI Validates Quality
   ↓
3. High Confidence → Stored Automatically
   ↓
4. Low Confidence → Flagged for You
   ↓
5. You Review → Accept/Correct/Reject
   ↓
6. Data Updated in Database
   ↓
7. Reports Generated
```

**Your role:** The quality checker! AI does the grunt work, you ensure accuracy.

---

### Why This Saves Time

**Before (Manual):**
- You: 65 hours/week finding and entering data
- Errors: Common (typos, missed updates)
- Scalability: Limited to 50-100 terminals

**After (AI-Assisted):**
- AI: Does 80-90% automatically
- You: 10-15 hours/week reviewing
- Errors: Rare (AI is consistent)
- Scalability: 500+ terminals easily

**Time saved:** 50 hours/week!  
**Money saved:** $70-110K/year!

---

## 🔐 SAFETY & SECURITY

### Keep Your API Key Safe

**DO:**
- ✅ Store in password manager
- ✅ Keep it secret
- ✅ Don't share with anyone

**DON'T:**
- ❌ Email it to people
- ❌ Post it online
- ❌ Save in public documents

If your key is exposed, **regenerate it immediately** at console.anthropic.com

---

### Backup Your Data

**Weekly:** Copy supply_chain.db to external drive  
**Monthly:** Copy entire tariff_library folder  
**Always:** Keep GitHub repository updated

**Lost data = lost work!** Back up regularly.

---

## ✅ BEGINNER'S CHECKLIST

Print this out and check off as you go:

**Setup (One Time):**
- [ ] Got Anthropic API key
- [ ] Installed Python
- [ ] Installed anthropic library
- [ ] Found project folder
- [ ] Tested setup successfully
- [ ] Set up double-click scripts (optional)

**Daily (2-3 minutes):**
- [ ] Run daily update
- [ ] Check for any warnings
- [ ] Note items flagged for review

**Weekly (1-2 hours):**
- [ ] Check review queue
- [ ] Review flagged items
- [ ] Accept/correct/reject data
- [ ] Update PROJECT_STATE.md

**Monthly (2-3 hours):**
- [ ] Run monthly update
- [ ] Check performance metrics
- [ ] Backup database and tariffs
- [ ] Update documentation

---

## 🎊 YOU'RE READY!

You now know how to:
- ✅ Set up the system
- ✅ Run daily updates
- ✅ Review AI findings
- ✅ Check status
- ✅ Solve common problems
- ✅ Get help when needed

**Start with small wins:**
1. Run your first daily update tomorrow
2. Review the results
3. Get comfortable with the process
4. Build from there!

**Remember:** The AI is your assistant. It does the tedious work, you provide the expertise and quality control.

---

## 📞 Support Quick Reference

**For setup help:** This file (BEGINNERS_GUIDE.md)  
**For daily use:** EASY_DOUBLE_CLICK_GUIDE.md  
**For quick commands:** QUICK_START_CHEATSHEET.txt  
**For technical issues:** DEVELOPMENT_GUIDE.md  
**For current status:** PROJECT_STATE.md  
**For AI help:** Upload PROJECT_STATE.md to claude.ai

---

**Good luck! You're automating what used to take 65 hours/week. That's amazing! 🚀**

*Last updated: February 10, 2026*
