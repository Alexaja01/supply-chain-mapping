# ⏰ PROJECT REMINDERS - Supply Chain Mapping

**Print this out and keep it visible at your workspace!**

Last Updated: February 11, 2026

---

## 🌅 BEFORE YOU START WORKING

- [ ] Read the last entry in PROJECT_STATE.md (What did I do last time?)
- [ ] Check for any flagged items: `python orchestrator.py --api-key KEY review`
- [ ] Create session_notes.txt scratch file for today

---

## 🌆 BEFORE YOU STOP WORKING

### ✅ **If you made significant changes today:**

- [ ] **Update PROJECT_STATE.md** (5 minutes)
  - [ ] Change "Last Updated" date at top
  - [ ] Add bullets under "Completed Today"
  - [ ] Update data counts (terminals, pipelines, tariffs)
  - [ ] Note any key learnings

- [ ] **Commit to GitHub** (2 minutes)
  - [ ] Open GitHub Desktop
  - [ ] Write meaningful commit message
  - [ ] Commit to main
  - [ ] Push to origin

- [ ] **Delete session_notes.txt** (after transferring info to PROJECT_STATE.md)

### ⏭️ **If you did routine work only:**

- [ ] No documentation update needed
- [ ] Just commit to GitHub if you changed any code

---

## 📅 FRIDAY END-OF-WEEK CHECKLIST

**Every Friday before closing out:** (15 minutes)

- [ ] **Update README.md metrics:**
  - [ ] Terminal count badge
  - [ ] Automation status
  - [ ] Update "Achievements" section
  - [ ] Update "Last Updated" date

- [ ] **Check DEVELOPMENT_GUIDE.md:**
  - [ ] Any new code patterns to document?
  - [ ] Any solutions to tricky problems worth saving?

- [ ] **Commit weekly progress:**
  - [ ] Commit message: "Weekly update: [brief summary]"
  - [ ] Push to GitHub

- [ ] **Backup database:**
  - [ ] Copy supply_chain.db to external drive
  - [ ] Verify copy succeeded

---

## 📆 FIRST OF EACH MONTH CHECKLIST

**Monthly maintenance routine:** (2-3 hours)

### 1. Run Monthly Audit
- [ ] `python orchestrator.py --api-key KEY monthly`
- [ ] Review audit results
- [ ] Address any issues found

### 2. Backup Everything
- [ ] Copy supply_chain.db → External drive
- [ ] Copy entire tariff_library folder → External drive
- [ ] Copy config.py → External drive
- [ ] Verify GitHub is current
- [ ] **Set calendar reminder for next month!**

### 3. Update Documentation
- [ ] Review PROJECT_STATE.md - Archive old "Completed" items if getting long
- [ ] Check BEGINNERS_GUIDE.md - Any process changes?
- [ ] Review DEVELOPMENT_GUIDE.md - Anything to add?
- [ ] Update README.md with current metrics

### 4. Review Performance
- [ ] Check API costs at console.anthropic.com
- [ ] Calculate hours spent on reviews
- [ ] Check automation rate (target: 85%+)
- [ ] Check data quality (target: 95%+)
- [ ] Document in PROJECT_STATE.md

### 5. Plan Next Month
- [ ] What agents to build next?
- [ ] What improvements to make?
- [ ] Update priorities in PROJECT_STATE.md

### 6. Commit Monthly Updates
- [ ] Commit message: "Monthly update: [month] [year] - [key achievements]"
- [ ] Push to GitHub

---

## 🚨 IMMEDIATE ACTION REMINDERS

**DO THIS RIGHT NOW when it happens:**

### If You Built Something New:
✅ Add it to PROJECT_STATE.md "Completed Today" section

### If You Discovered a Bug:
✅ Create GitHub Issue OR add to PROJECT_STATE.md "Known Issues"

### If You Learned a New Pattern:
✅ Add to DEVELOPMENT_GUIDE.md immediately (or you'll forget!)

### If You Change a Process:
✅ Update BEGINNERS_GUIDE.md so future-you knows the new way

### If Database Gets Big (>100MB):
✅ Consider archiving old data or optimizing

### If API Costs Spike:
✅ Investigate immediately - check orchestrator logs

---

## 📊 METRICS TO TRACK

### Weekly Metrics (Track in PROJECT_STATE.md)
- Terminals discovered/added
- Tariffs collected
- Tasks completed
- Items requiring review
- Hours spent on reviews

### Monthly Metrics (Track in PROJECT_STATE.md)
- Total terminals
- Total pipelines
- Total tariffs
- Automation rate
- Data quality score
- API costs
- Review hours

---

## 🔔 CALENDAR REMINDERS TO SET

Set these in your calendar app RIGHT NOW:

1. **Every Friday 4:00 PM:** "Weekly project update - Review REMINDERS.md"
2. **First of every month:** "Monthly backup and maintenance - See REMINDERS.md"
3. **Every 3 months:** "Test backup restore - Can I recover from backup?"

---

## 💡 QUICK TIPS

**Make it a habit:**
- ✅ Leave PROJECT_STATE.md open in a text editor tab all day
- ✅ Add notes to it as you work
- ✅ At end of day, clean it up and commit
- ✅ Treat GitHub commits like saving your game

**Signs you're falling behind:**
- ⚠️ PROJECT_STATE.md "Last Updated" is more than a week old
- ⚠️ You don't remember what you worked on yesterday
- ⚠️ Review queue has 50+ items
- ⚠️ Haven't backed up database in 2+ weeks

**When this happens:**
1. Stop new work
2. Spend a session catching up documentation
3. Clear review queue
4. Backup everything
5. Then resume new work

---

## 📝 SESSION NOTES TEMPLATE

**Create this file each work session:** `session_notes.txt`

```
DATE: [Today's date]
START TIME: [When you started]

GOAL FOR TODAY:
- [What you want to accomplish]

WORK LOG:
- [Note things as you do them]
- [Problems encountered]
- [Solutions found]
- [Data added]

END OF DAY TRANSFER TO PROJECT_STATE.MD:
- [Clean bullets for PROJECT_STATE.md]
- [Metrics: terminals, tariffs, etc.]
- [Key learnings]

NEXT SESSION:
- [What to do next time]

DELETE THIS FILE AFTER UPDATING PROJECT_STATE.MD
```

---

## ✅ PRINT & POST THIS

**Print this page and post it where you can see it while working!**

Or set as desktop background, or pin in your notes app - whatever works for you.

The key is: **Make these reminders VISIBLE so you don't forget!**

---

**Remember:** 5 minutes of documentation saves 5 hours of confusion later!

---

*If this file hasn't been updated in 3+ months, that's okay - it's meant to be stable. But do review it quarterly to see if processes have changed.*

*Last reviewed: February 11, 2026*
