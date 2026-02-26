# PROJECT STATE - Supply Chain Mapping System

**Last Updated:** February 26, 2026  
**Project Owner:** jalex  
**Current Phase:** Asset Agent Build — Claude Code Integration  
**Session Progress:** Claude Code architecture designed; ready to begin asset agent pipeline build

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

### Current Schema (52 Tables - per create_database.py)

**NOTE:** PROJECT_STATE.md previously stated 16 tables — this was stale. The actual schema created by `create_database.py` contains ~52 tables across 11 groups. Componentized costing infrastructure (costing_items, line_item_types, tariff_costs, etc.) **already exists at the schema level** but is not yet populated with component-level data. The migration work is a data population task, not a schema creation task.

**Table Groups (52 total):**
1. **Master Data (8):** product_categories, products, terminals, terminal_products, pipelines, refineries, rail_connections, marine_facilities
2. **Configuration (4):** line_item_types, costing_items, shipping_setup, price_days
3. **Linkage (5):** terminal_pipeline_links, pipeline_refinery_links, shipping_paths, terminal_path_links, tariff_path_links
4. **Costing (7):** pipeline_tariffs, tariff_libraries, tariff_costs, terminal_rates, transportation_costs, rail_rates, costing
5. **Shipping (2):** shipping_periods, shipping_line_items
6. **Spot Market (3):** spot_markets, index_components, spot_indices
7. **BCS / Buying Cost Sheets (5):** bcs_types, bcs_period_statuses, bcs, bcs_periods, bcs_line_items
8. **Alias / Multi-Tenant (7):** alias_types, terminal_aliases, product_aliases, line_item_type_aliases, index_aliases, price_day_aliases, (+ 1 TBD)
9. **Management (5):** agent_tasks, data_quality_log, agent_metrics, ownership_changes, source_documents
10. **Alias Error Tracking (5):** terminal_alias_errors, product_alias_errors, line_item_type_alias_errors, index_alias_errors, price_day_alias_errors
11. **ETL Tracking (2):** batches, shipping_tracking

**5+ Views:** v_active_terminals, v_active_pipeline_tariffs, v_review_queue, v_costing_detail, v_bcs_detail

### Current Data
- **Terminals: 227** ✅ (snapshot as of 2024-01-01)
- **Transportation Costs: 681** ✅ (227 × 3 products - combined adders only)
- Pipelines: 0
- Tariffs: 0

---

## ⚡ IMMEDIATE NEXT STEPS

**Priority 0: Claude Code — Install & First Session**
- [ ] Install: `npm install -g @anthropic-ai/claude-code`
- [ ] Open terminal in `C:\Users\jalex\supply-chain\supply-chain-mapping`
- [ ] Opening prompt: load PROJECT_STATE.md, config.py, create_database.py, terminal_discovery_agent.py
- [ ] First task: build `terminal_capture_agent.py` using IRS 510 as first source
- [ ] **Design constraints for Claude Code (do not deviate without approval):**
  - New asset agents write to `terminal_capture_staging` — NOT directly to `terminals`
  - All new agents use `uuid.uuid4()` for primary keys (not the legacy `ST####` pattern)
  - Add `web_search` tool explicitly to any Claude API calls needing live data
  - Propose schema changes before implementing — wait for approval
  - Leverage existing schema tables before adding new ones

**Priority 1: Asset Agent Pipeline (Claude Code build)**
- [ ] `terminal_capture_agent.py` — Stage 1: IRS 510 capture → staging table
- [ ] `terminal_validate_agent.py` — Stage 2: conflict detection, geocoding, confidence scoring
- [ ] `terminal_enrich_agent.py` — Stage 3: web enrichment, aliases, EPA RMP, EIA data

**Priority 2: Create first two Skills**
- [ ] `/skills/Tariff_Extraction/SKILL.md`
- [ ] `/skills/PADD3_Costing/SKILL.md`

**Priority 3: Define Colonial GC→ATL corridor completeness checklist**
- [ ] Asset list for corridor
- [ ] Connectivity requirements
- [ ] Costing components required

**Priority 4: Data population (not schema creation)**
- [ ] Populate `transportation_costs` component data into existing costing tables
- [ ] 681 flat combined-adder records → componentized entries in `costing` + `shipping_line_items`
- [ ] Note: schema tables already exist — this is a data migration task

---

## 📚 KEY LEARNINGS

✅ **Combined adder ≠ costing engine** - The flat import was useful to prove data exists, but the real work is building component-level cost tracking.

✅ **Context window management matters** - Restructured Claude projects to keep Core lean. SQL/Excel QC files are local-only and uploaded per session as needed.

✅ **Skills-first beats agents-first** - Encode repeatable procedures as Skills before building agents. Skills are portable to Cowork and future platforms.

✅ **Understanding data structure first** - Critical before coding. Reading process documentation revealed true structure.

✅ **Proven methodology is the IP** - The costing methodology in the Excel docs is the differentiating asset. Encode it as Skills + data model.

✅ **Schema is ahead of the docs** - create_database.py has ~52 tables including full componentized costing infrastructure. Always read the code, not just the documentation, to understand true current state.

✅ **Staging table is non-negotiable** - terminal_discovery_agent.py writes directly to production tables (design flaw). All new asset agents must use a staging buffer. Never write unvalidated captures directly to terminals.

✅ **Claude Code role is clear** - Best operated by someone with domain expertise + coding judgment. Use "propose before write" for all schema changes. Not suitable for non-technical solo operation against production data.

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
- Confirmed schema is ~52 tables (not 16 as previously documented) — componentized costing tables already exist
- Updated config.py: model string corrected to claude-sonnet-4-6
- SC Core Claude Stack Architecture deck updated (2-slide visual with Claude Code deep dive)
- Ready to begin Claude Code first session: asset capture agent build

---

*Last updated: February 26, 2026*
*Keep this file current - it's your project's memory!*
