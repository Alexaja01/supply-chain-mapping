# HOW TO PRESERVE & ITERATE - Long-Term Project Maintenance

**Keeping Your Project Healthy for Months and Years**

This guide ensures you can work on this project indefinitely without losing progress or knowledge.

Last Updated: February 10, 2026

---

## ✅ YOU'RE ALREADY SET UP!

Good news! You've already completed the critical setup:

- ✅ **GitHub repository created** - supply-chain-mapping (private)
- ✅ **GitHub Desktop installed** - Easy version control
- ✅ **Complete documentation** - 10+ comprehensive guides
- ✅ **PROJECT_STATE.md created** - Your project memory
- ✅ **All code committed** - Safe and backed up

**You're in great shape!** This guide shows you how to maintain it.

---

## 🎯 THE GOLDEN RULE

**Keep PROJECT_STATE.md current = Never lose your place**

After every significant change:
1. Update PROJECT_STATE.md
2. Commit to GitHub
3. Done!

Future you (or Claude) can pick up exactly where you left off.

---

## 📋 TABLE OF CONTENTS

1. [Daily Habits](#daily-habits)
2. [Weekly Maintenance](#weekly-maintenance)
3. [Monthly Check-Ins](#monthly-check-ins)
4. [GitHub Workflow](#github-workflow)
5. [Backup Strategy](#backup-strategy)
6. [Resuming Work After Breaks](#resuming-work-after-breaks)
7. [Working with Claude](#working-with-claude)
8. [Scaling the Project](#scaling-the-project)

---

## 🌅 DAILY HABITS

### What to Do Every Day (5 minutes)

**After running daily updates:**

1. **Quick check**
   - Did it run successfully? ✅
   - Any errors? ❌
   - Items flagged for review? ⚠️

2. **Note issues**
   - If errors, add to to-do list
   - If items flagged, mark for weekly review
   - If patterns emerge, note in PROJECT_STATE.md

3. **That's it!**
   - Don't need to commit every day
   - Don't need to update docs daily
   - Just run and note

---

## 🗓️ WEEKLY MAINTENANCE

### Every Week (30-60 minutes)

#### 1. Review Flagged Items

```bash
python orchestrator.py --api-key YOUR_KEY review
```

- Check quality of flagged data
- Accept, correct, or reject
- Document patterns

#### 2. Update PROJECT_STATE.md

**Update these sections:**

```markdown
## 📊 CURRENT DATA STATE

**As of [Today's Date]:**
- Terminals: 147 (was 132 last week)
- Pipelines: 23 (was 21)
- Tariffs: 89 (was 84)
- Tasks Completed: 234 (was 198)

**This Week:**
- Added 15 terminals from IRS discovery
- Updated 5 pipeline tariffs
- Fixed bug in quality scoring
```

#### 3. Commit to GitHub

1. Open **GitHub Desktop**
2. Review what changed
3. **Commit message:**
   ```
   Weekly update: Added 15 terminals, fixed quality scoring bug
   ```
4. **Push** to GitHub

#### 4. Check Performance

Track these metrics weekly:

| Metric | Target | This Week | Last Week |
|--------|--------|-----------|-----------|
| Automation Rate | 85%+ | ___ | ___ |
| Data Quality | 95%+ | ___ | ___ |
| Review Time | <15 hrs | ___ | ___ |
| Items Flagged | <20 | ___ | ___ |

**Trending up? Great!**  
**Trending down? Investigate why.**

---

## 📅 MONTHLY CHECK-INS

### First of Every Month (2-3 hours)

#### 1. Run Monthly Audit

```bash
python orchestrator.py --api-key YOUR_KEY monthly
```

This does deep validation of all data.

#### 2. Backup Everything

**Critical files:**

- [ ] `supply_chain.db` → External drive
- [ ] Entire `tariff_library` folder → External drive
- [ ] `config.py` → External drive
- [ ] Verify GitHub is current

**Set calendar reminder!**

#### 3. Review Documentation

**Check if these need updates:**

- PROJECT_STATE.md - Always update with current status
- DEVELOPMENT_GUIDE.md - Add new patterns discovered
- README.md - Update metrics and status
- BEGINNERS_GUIDE.md - Any process changes?

#### 4. Analyze Costs

**Track monthly:**
- API costs from console.anthropic.com
- Time spent on reviews
- System reliability

**Compare to targets:**
- Cost: <$500/month ✅
- Review time: <60 hours/month ✅
- Uptime: >95% ✅

#### 5. Plan Next Month

**In PROJECT_STATE.md:**
- What agents to build next?
- What data to add?
- What improvements to make?
- What's the priority?

---

## 🔄 GITHUB WORKFLOW

### Your GitHub is Already Set Up!

**Repository:** https://github.com/[yourusername]/supply-chain-mapping  
**Tool:** GitHub Desktop (already installed)  
**Status:** Private repository, all code backed up

### Daily Workflow (If You Made Changes)

**Don't commit every tiny change!** Commit when:
- Built a feature
- Fixed a bug
- Made significant progress
- End of work session

**How to commit:**

1. **Open GitHub Desktop**
   - Automatically shows changed files

2. **Review changes**
   - Check what's different
   - Make sure it makes sense

3. **Write good message**
   - Bad: "changes"
   - Bad: "updates"
   - Good: "Added pipeline tariff agent"
   - Good: "Fixed database locking issue in orchestrator"

4. **Commit & Push**
   - Click "Commit to main"
   - Click "Push origin"

**Done!** Changes are backed up to GitHub cloud.

---

### When to Create Branches (Advanced - Optional)

For most work, just commit to `main`. But if you're:

- **Testing major changes** → Create branch
- **Trying experimental features** → Create branch
- **Working on multiple features** → Create branch

**How:**
1. In GitHub Desktop: Current Branch → New Branch
2. Name it: `feature-pipeline-tariff-agent`
3. Work on the branch
4. When done, merge back to main

For now, **just use main** - it's simpler!

---

## 💾 BACKUP STRATEGY

### Three-Layer Protection

#### Layer 1: GitHub (Automatic)
- ✅ All code backed up
- ✅ All documentation backed up
- ✅ Version history maintained
- ✅ Accessible from anywhere

**No action needed - it's automatic!**

#### Layer 2: Local Backups (Weekly)

**What to back up:**

```
Weekly backup (every Friday):
  ☐ Copy supply_chain.db to external drive
  ☐ Takes 10 seconds
```

**Where to back up:**
- External hard drive
- USB stick
- OneDrive/Google Drive folder

#### Layer 3: Full Archive (Monthly)

**First of each month:**

```
Monthly full backup:
  ☐ Copy entire supply-chain-mapping folder
  ☐ Copy tariff_library folder
  ☐ ZIP both
  ☐ Name: supply-chain-backup-2026-02.zip
  ☐ Store on external drive
  ☐ Takes 5 minutes
```

### Testing Your Backups

**Every 3 months:**
1. Try restoring from backup
2. Verify database opens
3. Verify code runs
4. Make sure nothing is corrupted

**If you can't restore, your backup is worthless!**

---

## ⏸️ RESUMING WORK AFTER BREAKS

### After a Weekend

**No special prep needed!**

Just run your daily update:
```bash
python orchestrator.py --api-key YOUR_KEY daily
```

---

### After a Week

**Quick refresh:**

1. **Read PROJECT_STATE.md**
   - Where you left off
   - What was next

2. **Check status**
   ```bash
   python orchestrator.py --api-key YOUR_KEY status
   ```

3. **Review queue**
   ```bash
   python orchestrator.py --api-key YOUR_KEY review
   ```

4. **Continue where you left off!**

---

### After a Month or More

**Full reorientation:**

#### 1. Pull Latest from GitHub

**GitHub Desktop:**
- Click "Fetch origin"
- Click "Pull" if there are changes
- (In case you worked from another computer)

#### 2. Review Project State

**Read these files:**
- PROJECT_STATE.md - Current status
- DEVELOPMENT_GUIDE.md - How things work
- README.md - Overview

Takes 15-30 minutes to refresh your memory.

#### 3. Test the System

```bash
# Make sure Python still works
python --version

# Make sure libraries installed
pip list | grep anthropic

# Test the database
python config.py

# Check status
python orchestrator.py --api-key YOUR_KEY status
```

#### 4. Start Small

**Don't dive into complex work immediately!**

- Run a simple daily update
- Review some flagged items
- Get comfortable again
- Then tackle new features

---

## 🤖 WORKING WITH CLAUDE

### Your Secret Weapon for Long-Term Success

**Claude can help you resume work at any time!**

### Starting a New Session (After Time Away)

**Upload these files:**
1. PROJECT_STATE.md
2. DEVELOPMENT_GUIDE.md
3. The specific file you're working on

**Say:**
```
Hi Claude! I'm back working on the supply chain mapping project
after a break. I've uploaded PROJECT_STATE.md showing current status.

I want to [build new agent / fix bug / add feature / etc.].
Can you help?
```

**Claude will:**
- Understand exactly where you are
- Know what's built and what's not
- Continue from where you left off
- No need to re-explain everything

### Claude as Your Documentation Assistant

**Use Claude to:**

- **Update PROJECT_STATE.md** when you forget
  > "Here's what I did this week. Can you update PROJECT_STATE.md?"

- **Review your code** before committing
  > "Does this look right? Any bugs you see?"

- **Explain old code** you wrote months ago
  > "I wrote this function but forgot what it does. Can you explain?"

- **Generate documentation** for new features
  > "I built this agent. Can you write documentation for README.md?"

**See NEW_SESSION_TEMPLATE.md for more examples**

---

## 📈 SCALING THE PROJECT

### As Your Project Grows

#### Stage 1: Learning (Weeks 1-4)
- Current stage
- 0-50 terminals
- Getting comfortable
- Testing the approach

**Maintenance:** Light - just learning

---

#### Stage 2: Growing (Weeks 5-12)
- 50-200 terminals
- Multiple agents working
- Regular updates
- Building confidence

**Maintenance:** Moderate - weekly reviews important

---

#### Stage 3: Production (Weeks 13+)
- 200-500+ terminals
- All agents operational
- Automated scheduling
- Minimal intervention

**Maintenance:** Efficient - mostly automated

---

### When to Upgrade Infrastructure

**Keep SQLite if:**
- <500 terminals ✅
- Single user ✅
- Fast enough ✅

**Consider PostgreSQL if:**
- >500 terminals
- Multiple users
- Need advanced features

**Consider cloud deployment if:**
- Running 24/7
- Need high availability
- Team collaboration

**For now:** SQLite is perfect! Don't over-engineer.

---

## 📊 HEALTH INDICATORS

### Project is Healthy When:

✅ **Can resume work in <5 minutes**
- GitHub up to date
- Documentation current
- System runs without errors

✅ **Automation rate >80%**
- Most tasks run without human review
- Quality remains high
- Cost stays under budget

✅ **Clear next steps**
- PROJECT_STATE.md shows what's next
- Priorities are documented
- No confusion about direction

✅ **Manageable review queue**
- <20 items flagged per week
- Can review in <15 hours
- Not falling behind

---

### Warning Signs

⚠️ **Review queue building up**
- >50 items pending
- Behind more than 2 weeks

**Fix:** Dedicate a day to catch up, adjust thresholds

⚠️ **Automation rate dropping**
- Was 85%, now 70%
- More items flagged

**Fix:** Investigate why, improve agent logic

⚠️ **Documentation out of date**
- PROJECT_STATE.md last updated months ago
- Don't remember what you were doing

**Fix:** Spend 1 hour updating all docs

⚠️ **Costs creeping up**
- Was $400/month, now $800
- Unclear why

**Fix:** Analyze agent metrics, optimize queries

---

## 🎯 LONG-TERM BEST PRACTICES

### Documentation

**Update Regularly:**
- PROJECT_STATE.md - After every significant change
- DEVELOPMENT_GUIDE.md - When you discover new patterns
- README.md - Monthly with current metrics

**Keep It Real:**
- Don't document what you wish you had
- Document what actually exists
- Update when things change

### Code Quality

**Before Committing:**
- Test it works
- Add comments for complex logic
- Use config.py for paths
- Follow existing patterns

**Refactor When:**
- Same code in 3+ places → Make function
- File over 500 lines → Split it up
- Configuration scattered → Move to config.py

### Communication

**With Future You:**
- Write clear commit messages
- Document why, not just what
- Leave breadcrumbs in comments

**With Claude:**
- Always upload PROJECT_STATE.md
- Be specific about goals
- Test suggestions before moving on

---

## 🔮 FUTURE CONSIDERATIONS

### Year 1: Foundation
- ✅ Get system working (you're here!)
- Build 10 agent types
- Map 400+ terminals
- Prove the approach

### Year 2: Optimization
- Improve automation rate
- Reduce review time
- Add analytics
- Fine-tune quality

### Year 3: Expansion
- Additional products (diesel, jet fuel)
- International supply chains
- Advanced predictions
- Commercial product?

**Keep these in mind, but focus on Year 1 first!**

---

## ✅ MAINTENANCE CHECKLIST

### Daily (5 minutes)
- [ ] Run daily update
- [ ] Note any errors
- [ ] Mark items for weekly review

### Weekly (1-2 hours)
- [ ] Review flagged items
- [ ] Update PROJECT_STATE.md
- [ ] Commit to GitHub
- [ ] Check performance metrics

### Monthly (2-3 hours)
- [ ] Run monthly audit
- [ ] Backup database and tariff library
- [ ] Review and update documentation
- [ ] Analyze costs
- [ ] Plan next month's priorities

### Quarterly (Half day)
- [ ] Test backup restore
- [ ] Review overall progress
- [ ] Update roadmap
- [ ] Refactor messy code
- [ ] Deep clean review queue

### Annually (Full day)
- [ ] Full system review
- [ ] Update all documentation
- [ ] Consider infrastructure upgrades
- [ ] Celebrate achievements! 🎉

---

## 🎊 SUMMARY

**You're Already Set Up for Success!**

✅ GitHub: Backing up all your code  
✅ Documentation: Complete and comprehensive  
✅ PROJECT_STATE.md: Your project memory  
✅ Tools: GitHub Desktop, Python, Claude API  

**To Maintain Long-Term:**

1. **Update PROJECT_STATE.md** after significant changes
2. **Commit to GitHub** weekly
3. **Back up database** weekly
4. **Full backup** monthly
5. **Use Claude** to resume after breaks

**Time Investment:**
- Daily: 5 minutes
- Weekly: 1-2 hours
- Monthly: 2-3 hours

**Result:** Project stays healthy indefinitely!

---

## 📞 QUICK REFERENCE

**Stuck after time away?**
1. Read PROJECT_STATE.md
2. Run `python orchestrator.py --api-key KEY status`
3. Start new Claude session with PROJECT_STATE.md

**Made changes?**
1. Update PROJECT_STATE.md
2. Commit to GitHub
3. Done!

**Monthly routine?**
1. Audit + Backup + Review docs + Plan next month

**That's it!** Simple, sustainable, effective.

---

**Your project is built to last. Keep PROJECT_STATE.md current and you'll never lose your place!** 🚀

*Last updated: February 10, 2026*
