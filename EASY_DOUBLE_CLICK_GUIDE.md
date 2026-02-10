# 🖱️ EASY DOUBLE-CLICK GUIDE - Simplest Way to Run

**No Command Line Needed! Just Double-Click!**

After a quick one-time setup, you can run your supply chain mapping system by simply **double-clicking a file**. No typing commands, no technical knowledge required.

Last Updated: February 10, 2026

---

## 🎯 What This Guide Does

Shows you how to set up "double-click" files so you can run the system like this:

**Before:** Type commands in terminal ❌  
**After:** Double-click a file ✅

**Time saved:** 30 seconds per run  
**Convenience:** 📈📈📈

---

## 📋 TABLE OF CONTENTS

1. [For Windows Users](#for-windows-users-)
2. [For Mac Users](#for-mac-users-)
3. [What the Script Does](#what-the-script-does)
4. [Creating Desktop Shortcuts](#creating-desktop-shortcuts-extra-convenience)
5. [Troubleshooting](#troubleshooting)

---

## 🪟 FOR WINDOWS USERS

### One-Time Setup (5 Minutes)

#### Step 1: Find the File

Go to your project folder:
```
C:\Users\jalex\supply-chain\supply-chain-mapping
```

Find the file: **`run_daily_update.bat`**

---

#### Step 2: Edit the File

1. **Right-click** `run_daily_update.bat`
2. Select **"Edit"** (or "Edit with Notepad")
3. The file opens in Notepad

---

#### Step 3: Add Your API Key

**Find this line** (around line 22):
```
set API_KEY=YOUR_API_KEY_HERE
```

**Change it to** (using your real API key from console.anthropic.com):
```
set API_KEY=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
```

(This is just an example - use YOUR actual key!)

---

#### Step 4: Save and Close

1. **Click:** File → Save
2. **Close** Notepad
3. **Done!** ✅

---

### Daily Use - Just Double-Click!

**Every day:**

1. Go to your project folder
2. **Double-click** `run_daily_update.bat`
3. A window opens and runs the update
4. When done, it shows what needs your review
5. Press any key to close

**That's it!** Takes 1-2 minutes total.

---

### What You'll See When It Runs

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
    Check FERC eTariff for new pipeline tariff filings
    ✓ Completed

  → OWNERSHIP_TRACKING_20260210_060001
    Search for terminal/pipeline M&A announcements
    ✓ Completed

  → QUALITY_ASSURANCE_20260210_060002
    Run quality checks on 50 random terminal records
    ⚠️  Requires human review

================================================
   Update complete!
================================================

Checking for items needing your review...

📋 Review Queue (1 item):

  QUALITY_ASSURANCE_20260210_060002
    Run quality checks on 50 random terminal records
    Found 3 terminals with low confidence scores

Press any key to close this window...
```

---

## 🍎 FOR MAC USERS

### One-Time Setup (5 Minutes)

#### Step 1: Find the File

Go to your project folder:
```
/Users/[yourname]/supply-chain/supply-chain-mapping
```

Find the file: **`run_daily_update.sh`**

---

#### Step 2: Edit the File

1. **Right-click** `run_daily_update.sh`
2. Select **"Open With"** → **"TextEdit"**
3. The file opens

---

#### Step 3: Add Your API Key

**Find this line** (around line 13):
```
API_KEY="YOUR_API_KEY_HERE"
```

**Change it to** (using your real API key):
```
API_KEY="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"
```

(Use YOUR actual key from console.anthropic.com!)

---

#### Step 4: Save and Close

1. **Click:** File → Save
2. **Close** TextEdit

---

#### Step 5: Make It Executable (One Time Only)

1. Open **Terminal** (Command + Space, type "terminal", Enter)
2. Type:
   ```
   chmod +x ~/supply-chain/supply-chain-mapping/run_daily_update.sh
   ```
3. Press **Enter**
4. **Done!** ✅

---

### Daily Use - Two Methods

#### Method 1: Double-Click

1. Go to your project folder in Finder
2. **Double-click** `run_daily_update.sh`
3. If asked, select **"Open with Terminal"**
4. Terminal opens and runs the update
5. When done, close the Terminal window

#### Method 2: From Terminal (Faster)

1. Open Terminal
2. Type:
   ```
   ~/supply-chain/supply-chain-mapping/run_daily_update.sh
   ```
3. Press Enter

Both work great! Use whichever you prefer.

---

## 🔄 WHAT THE SCRIPT DOES

When you double-click the script, here's what happens automatically:

### 1. Checks Configuration ✅
- Verifies your API key is set
- Confirms you're in the right folder
- Makes sure Python is installed

### 2. Runs Daily Update 🔄
- Checks FERC for new pipeline tariffs (last 24 hours)
- Searches for ownership change announcements
- Runs quality checks on random sample of data
- Takes about 1-2 minutes

### 3. Shows Results 📊
- Displays what was found
- Shows what completed successfully
- Highlights anything needing your review

### 4. Checks Review Queue ⚠️
- Lists items that need human attention
- Shows confidence scores
- Explains why each item was flagged

### 5. Waits for You 🖱️
- Keeps the window open so you can read results
- Press any key to close when you're done

---

## 🖥️ CREATING DESKTOP SHORTCUTS (Extra Convenience)

Want to run it from your Desktop? Create a shortcut!

### Windows

1. **Go to:** `C:\Users\jalex\supply-chain\supply-chain-mapping`
2. **Right-click** `run_daily_update.bat`
3. Select **"Create shortcut"**
4. **Drag the shortcut** to your Desktop
5. **Rename it** to "Supply Chain Update" (optional)

Now just **double-click the Desktop icon** to run! 🎯

---

### Mac

1. **Go to:** Your project folder in Finder
2. **Right-click** `run_daily_update.sh`
3. Select **"Make Alias"**
4. **Drag the alias** to your Desktop
5. **Rename it** to "Supply Chain Update" (optional)

Now just **double-click the Desktop icon** to run! 🎯

---

## 🗓️ WEEKLY & MONTHLY SCRIPTS (Optional)

You can create similar scripts for weekly and monthly updates!

### For Weekly Updates

**Copy** your `run_daily_update` file and **rename** it to `run_weekly_update`

**Edit the new file** and change this line:

**Windows (.bat file):**
```
python orchestrator.py --api-key %API_KEY% weekly
```

**Mac (.sh file):**
```
python3 orchestrator.py --api-key "$API_KEY" weekly
```

Now you have a weekly update you can double-click!

---

### For Monthly Updates

Same process, but change to:

**Windows:**
```
python orchestrator.py --api-key %API_KEY% monthly
```

**Mac:**
```
python3 orchestrator.py --api-key "$API_KEY" monthly
```

---

## 🛠️ TROUBLESHOOTING

### "This file is not recognized" or "API key error"

**Problem:** You didn't edit the file to add your API key

**Solution:**
1. Right-click the file
2. Select "Edit" (Windows) or "Open With → TextEdit" (Mac)
3. Add your API key as shown in setup steps above
4. Save and try again

---

### "Python is not recognized" (Windows)

**Problem:** Python isn't installed or not in your system PATH

**Solution:**
1. Download Python from python.org
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH" during install
4. Restart computer
5. Try again

---

### "Permission denied" (Mac)

**Problem:** The script doesn't have permission to run

**Solution:**
Run this in Terminal:
```
chmod +x ~/supply-chain/supply-chain-mapping/run_daily_update.sh
```

Then try again.

---

### Script Opens Then Immediately Closes

**Problem:** There's an error, but window closes too fast to see it

**Solution - See the Error:**

**Windows:**
1. Open Command Prompt (Windows key → cmd → Enter)
2. Type: `cd C:\Users\jalex\supply-chain\supply-chain-mapping`
3. Type: `run_daily_update.bat`
4. Now you can see the error message!

**Mac:**
1. Open Terminal
2. Type: `~/supply-chain/supply-chain-mapping/run_daily_update.sh`
3. Now you can see the error message!

---

### "Could not find the path specified"

**Problem:** The script can't find your project folder

**Solution:**
1. Check the path in the script matches your actual folder location
2. Edit the script and update the path if needed
3. Make sure you didn't move or rename folders

---

## 🔐 SECURITY NOTE

### Your API Key is in the File! 🔒

**Important:** Your API key is stored in the script file. This means:

✅ **Convenient** - You don't type it every time  
⚠️ **Keep it private** - Don't share this file with anyone  
⚠️ **Don't upload it** - This file should NOT go to GitHub or cloud storage  

**If you share your computer:** Use the manual command line method instead, where you type the API key each time.

---

## 📊 USAGE PATTERNS

### Recommended Schedule

**Daily (Mon-Fri):** Double-click the daily update script  
**Weekly (Monday):** Run weekly update  
**Monthly (1st of month):** Run monthly update

**Time commitment:**
- Daily: 2-3 minutes
- Weekly: 1-2 hours (includes review)
- Monthly: 2-3 hours (includes audit)

**Total: ~10-15 hours per week** vs. 65 hours manually! 🎉

---

## 🎯 TIPS FOR SUCCESS

### 1. Make It a Habit

**Best time:** First thing in the morning with your coffee ☕

**Set a reminder:** Add to your calendar or to-do list

**Consistency:** Run daily = better data quality

---

### 2. Review Right Away

When items are flagged for review:
- ✅ Address them the same day if possible
- ✅ Don't let review queue build up
- ✅ 10 minutes now saves 2 hours later

---

### 3. Watch for Patterns

If the same issue keeps appearing:
- 📝 Document it in PROJECT_STATE.md
- 🔧 Fix the agent to handle it better
- 💬 Ask Claude for help improving the agent

---

### 4. Celebrate Wins! 🎉

- First successful daily update? Celebrate!
- Zero items needing review? Awesome!
- Reached 85% automation? Amazing!

**Track your progress** in PROJECT_STATE.md

---

## 🚀 GOING EVEN FURTHER

### Automate with Windows Task Scheduler (Advanced)

Want it to run automatically every day without you clicking?

1. Open "Task Scheduler" (search in Start menu)
2. Click "Create Basic Task"
3. Name it "Supply Chain Daily Update"
4. Trigger: Daily, 6:00 AM
5. Action: Start a program
6. Program: `C:\Users\jalex\supply-chain\supply-chain-mapping\run_daily_update.bat`
7. Finish

Now it runs every morning automatically!

---

### Automate on Mac (Advanced)

Use **Automator** or **cron** to schedule automatic runs.

**Easy way (Automator):**
1. Open Automator
2. Create new "Calendar Alarm"
3. Add "Run Shell Script"
4. Paste your update command
5. Save

**Advanced way (cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 6am):
0 6 * * * ~/supply-chain/supply-chain-mapping/run_daily_update.sh
```

---

## ✅ QUICK CHECKLIST

### One-Time Setup
- [ ] Found the run_daily_update script file
- [ ] Opened it for editing
- [ ] Added my API key to the file
- [ ] Saved the file
- [ ] (Mac only) Made it executable with chmod
- [ ] Tested it by double-clicking - it works!

### Optional Enhancements
- [ ] Created desktop shortcut
- [ ] Created weekly update script
- [ ] Created monthly update script
- [ ] Set up automatic scheduling (advanced)

### Daily Usage
- [ ] Double-click the script
- [ ] Watch it run (1-2 minutes)
- [ ] Note any items flagged for review
- [ ] Close the window when done

---

## 🎊 YOU'RE DONE!

You now have the **easiest possible way** to run your supply chain mapping system!

**From now on:**
1. Double-click the file
2. Wait 1-2 minutes
3. Done!

**No typing, no command line, no complexity.** Just point and click! 🖱️✨

---

## 📞 NEED HELP?

**For setup issues:** See [BEGINNERS_GUIDE.md](BEGINNERS_GUIDE.md)  
**For technical details:** See [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)  
**For understanding results:** See [README.md](README.md)  
**For current status:** See [PROJECT_STATE.md](PROJECT_STATE.md)

---

**Enjoy your super-simple, double-click supply chain mapping system! 🚀**

*Last updated: February 10, 2026*
