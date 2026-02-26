# PROJECT STATE - Supply Chain Mapping System

**Last Updated:** February 26, 2026  
**Project Owner:** jalex  
**Current Phase:** Asset Agent Build — Capture Complete, Validation Next  
**Session Progress:** Session 3 complete — 1,332 IRS terminals staged, ready for Session 4 (validation agent)

---

## 🎯 PROJECT MISSION (UPDATED)

Build a **Supply Chain Intelligence Engine** built **asset-first** in **PADD 3**, layered upward into connectivity, costing, and agent workflows.

**Key design pivot:** The existing 227 terminals + combined adder dataset is an *output* of costing, not the costing process itself. To support recalculation, explainability, updates, and portfolio-wide reasoning, we must build the **engine**, not just store **results**.

**Architecture sequence:** Assets → Connectivity → Costing → Participants → Contracts → Transactions

**Strategic driver:** Built Claude-native but designed to be exportable/licensable to NewTide.ai RisingTide as a standalone system or integrated module.

**Business Value:**
- Cost: ~$4-6K/year in AI API vs $80-120K/year for FTE
- Efficiency: 70-85% reduction in manual work
- Scalability: 500+ terminals vs manual limit of ~50-100

---

## 🗂️ CLAUDE PROJECT STRUCTURE

As of February 18, 2026, work is organized across Claude Projects to manage context window efficiently:

### SC Core (this project)
Persistent brain - always loaded. Contains:
- `PROJECT_STATE.md` - Project memory (this file)
- `DEVELOPMENT_GUIDE.md` - Technical how-to reference
- `README.md` - Project overview
- `HOW_TO_PRESERVE_AND_ITERATE.md` - Long-term maintenance

### SC - PADD3 POC (separate project)
PADD 3 Intelligence Engine work. Contains:
- `README — PADD 3 Supply Chain Project Update.md` - Strategic direction
- `Costings_Process_and_Road_Map.docx` - Costing methodology
- `Costings_Outline_for_BM_02_14_2024.docx` - Costing deliverables reference

### Local Only (do not upload to projects)
Access locally and upload to a session only when actively working that task:
- All SQL QC query files (0-3 series)
- All Excel QC workbooks (EN Costing/Shipping/BCS)
- `QC_Queries_Docs_and_Workbooks.docx`

---

## 🚀 STRATEGIC DIRECTION (February 2026)

### First POC: Colonial Pipeline Corridor - Gulf Coast → Atlanta
Why this corridor:
- Central to PADD 3 logic and real markets
- Maps to NewTide "Gulf Coast → Atlanta" arb demo patterns
- Demonstrates asset completeness, connectivity correctness, costing explainability

Definition of "done" for corridor POC:
- Assets fully specified (terminal attributes, pipeline points, product applicability, constraints)
- Route graph defined (segments + rules)
- Cost components defined + computed (with traceability to sources)
- QC checks pass
- Outputs: landed cost/netback comparison tables + explainable cost breakdown per path

### Layered Architecture
1. **Layer 1 - Knowledge Foundation** - Skills, schemas, corridor playbooks (Claude Projects)
2. **Layer 2 - Asset Database** - Authoritative structured records (local, maintained via Cowork)
3. **Layer 3 - Connectivity Graph** - Routes, multi-hop paths, constraints
4. **Layer 4 - Costing Engine** - Componentized cost model (the IP layer)
5. **Layer 5 - Agent Layer** - Ongoing maintenance, refreshes, QC, use-case workflows

### Skills-First Implementation
Every repeatable procedure becomes a SKILL.md. Initial skills to create:
1. **Tariff Extraction Skill** - extract rates + effective dates from PDFs, normalize units
2. **PADD3 Costing Skill** - component hierarchy, calculation rules, output: cost breakdown
3. **Terminal Validation Skill** - completeness scoring, human review triggers
4. **Netback / Landed Cost Skill** - spot inputs + freight + terminal charges → comparisons

---

## 💾 DATABASE STATUS

### Current Schema (54 Tables)

**NOTE:** Schema was rebuilt February 26 with full componentized costing infrastructure. The old 16-table description is retired.

**Table Groups (54 total):**
- Master Data (8), Configuration (4), Linkage (5), Costing (7), Shipping (2)
- Spot Market (4), BCS (5), Alias/Multi-Tenant (6), Management (5)
- Alias Error Tracking (5), ETL Tracking (2), Asset Capture Staging (1)

**6 Views:** v_active_terminals, v_active_pipeline_tariffs, v_review_queue, v_terminal_products, v_active_shipping, v_bcs_detail

### Current Data
- **Terminals: 0** — fresh database, old 227 not migrated (by design)
- **terminal_capture_staging: 1,332** ✅ IRS TCN Directory captured 2/26/2026
- **Transportation Costs: 0** — componentized population pending
- Pipelines: 0 | Tariffs: 0

### Staging Table Status
- **Capture source:** IRS_510
- **Records:** 1,332
- **Status:** all pending (awaiting validation agent)
- **Confidence scores:** 0.70 across the board
- **Root cause of 0.70:** TCN pattern mismatch (-0.20) + missing operator field (-0.10)
- **TCN format confirmed:** XX-ST-XXXX (e.g. `04-MA-1151`, `02-NH-1056`)
- **config.TCN_PATTERN needs update:** change to `^\d{2}-[A-Z]{2}-\d{4}$` in Session 4

---

## ⚡ IMMEDIATE NEXT STEPS

**Priority 1: Session 4 — terminal_validate_agent.py (Claude Code)**
- [ ] Fix config.TCN_PATTERN: update to `^\d{2}-[A-Z]{2}-\d{4}$`
- [ ] Build validation agent that reads from terminal_capture_staging
- [ ] Promote high-confidence records (>= 0.85) to terminals table
- [ ] Flag low-confidence records for human review
- [ ] Handle operator field — IRS file doesn't include it, need enrichment source

**Priority 2: Session 5 — terminal_enrich_agent.py (Claude Code)**
- [ ] EIA terminal database cross-reference
- [ ] Operator/owner enrichment
- [ ] Geocoding (lat/lon) via Nominatim
- [ ] EPA RMP cross-reference for hazmat facilities

**Priority 3: Create first two Skills (Claude.ai — not Claude Code)**
- [ ] `/skills/Tariff_Extraction/SKILL.md`
- [ ] `/skills/PADD3_Costing/SKILL.md`
- [ ] Upload Costings_Process_and_Road_Map.docx to SC-PADD3 POC project first

**Priority 4: Colonial GC→ATL corridor completeness checklist**
- [ ] Filter terminal_capture_staging for GA, AL, TN, MS terminals
- [ ] Identify Colonial pipeline injection/delivery points
- [ ] Define corridor asset list

---

## 📚 KEY LEARNINGS

✅ **Combined adder ≠ costing engine** - The flat import was useful to prove data exists, but the real work is building component-level cost tracking.

✅ **Context window management matters** - Restructured Claude projects to keep Core lean. SQL/Excel QC files are local-only and uploaded per session as needed.

✅ **Skills-first beats agents-first** - Encode repeatable procedures as Skills before building agents. Skills are portable to Cowork and future platforms.

✅ **Understanding data structure first** - Critical before coding. Reading process documentation revealed true structure.

✅ **Proven methodology is the IP** - The costing methodology in the Excel docs is the differentiating asset. Encode it as Skills + data model.

✅ **Schema is ahead of the docs** - create_database.py has 54 tables including full componentized costing infrastructure. Always read the code, not just the documentation, to understand true current state.

✅ **Staging table is non-negotiable** - terminal_discovery_agent.py writes directly to production tables (design flaw). All new asset agents must use terminal_capture_staging as a buffer. Never write unvalidated captures directly to terminals.

✅ **Claude Code model matters** - Default is Opus 4.6 in the desktop app. Switch to Sonnet 4.6 at the start of every session — same quality for agent building, significantly faster and cheaper.

✅ **GitHub Desktop ≠ Git** - Claude Code requires Git for Windows (git-scm.com) installed separately. GitHub Desktop has its own internal Git that Claude Code cannot access.

✅ **IRS TCN data is NOT in Publication 510** - The terminal listing is a separate downloadable file called the TCN Directory at irs.gov/pub/irs-sbse/tcn-db.xlsx. Publication 510 is the excise tax rules document only.

✅ **IRS TCN format is XX-ST-XXXX not XX-XXXXXXX** - Format is `04-MA-1151` (2-digit region, 2-letter state, 4-digit number). config.TCN_PATTERN must be updated to `^\d{2}-[A-Z]{2}-\d{4}$`.

✅ **IRS TCN directory has no operator field** - The IRS file contains TERMNO, TERMNAME, TERMADDR1, TERMADDR2, TERMCITY, TERMST, TERMZIP. Operator/owner data requires enrichment from a separate source (EIA, EPA RMP, web search).

✅ **Diagnostic first, fix second** - When a data source returns 0 records, print raw column names and first 3 rows before attempting to fix the parser. Saves multiple debugging cycles.

---

## 📋 SESSION LOG

**Session 1 (February 10, 2026):**
- Complete infrastructure built (16 tables)
- 227 terminals imported, 681 transportation cost records created
- Excel Import Agent, Terminal Discovery Agent, Orchestrator built
- 1,800+ lines of code, 10+ documentation files
- GitHub repository configured

**Session 2 (February 18, 2026):**
- Strategic pivot: asset-first, corridor-first, componentized costing
- PADD 3 focus established, Colonial GC→ATL as first POC corridor
- Claude project structure redesigned for context efficiency
- SC Core trimmed to 4 files; PADD3 POC project to be created
- NewTide.ai RisingTide exportability established as strategic driver

**Session 3 (February 26, 2026):**
- Claude Code integrated into stack architecture as primary build tool
- Asset agent pipeline designed: Capture → Validate → Enrich (3-stage, staging-table pattern)
- Identified design flaw in terminal_discovery_agent.py: direct production writes, no staging, no web_search tool, non-UUID IDs
- Confirmed schema is 54 tables (not 16 as previously documented) — componentized costing tables already exist at schema level; migration is data population not schema creation
- Updated config.py: model string corrected to claude-sonnet-4-6; ASSET_STAGING_TABLE, STAGING_REVIEW_THRESHOLD, CAPTURE_SOURCES constants added
- Fixed data_quality_log schema in create_database.py to match agent INSERT columns
- Added terminal_capture_staging table to create_database.py
- Folder structure cleaned: agents\, skills\, Reference\ folders created; clutter removed to Reference\
- Fresh supply_chain.db created with 54 tables, 6 views, 35 indexes
- Git for Windows 2.53.0 installed (required for Claude Code desktop app)
- Claude Code desktop app confirmed connected to Alexaja01/supply-chain-mapping on main branch
- **terminal_capture_agent.py built by Claude Code — 547 lines, committed to repo**
- **1,332 IRS TCN terminals captured to terminal_capture_staging ✅**
- IRS TCN format confirmed: `XX-ST-XXXX` (e.g. `04-MA-1151`) — NOT `^\d{2}-\d{7}$`
- config.TCN_PATTERN needs update to `^\d{2}-[A-Z]{2}-\d{4}$` — defer to Session 4
- Confidence scores at 0.70 — TCN pattern mismatch + missing operator field — calibrate in validation agent
- Operators confirmed in data: Irving Oil, Sprague, Global Companies, Energy Transfer, Citgo, ExxonMobil
- **Claude Code model: always switch to Sonnet 4.6 at session start — default is Opus 4.6**

---

*Last updated: February 26, 2026*
*Keep this file current - it's your project's memory!*
