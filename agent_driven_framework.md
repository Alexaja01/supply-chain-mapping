# Agent-Driven Supply Chain Mapping Project Framework
## Using Claude and Automation Tools

---

## Overview

This framework creates a semi-autonomous system where Claude agents handle 80-90% of the data collection, processing, and maintenance work, with humans only involved for:
- Strategic decisions
- Data validation checkpoints
- Exception handling
- Quality assurance reviews

---

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                       │
│              (Claude as Project Manager Agent)               │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
        ┌───────▼──────┐            ┌──────▼───────┐
        │ Data         │            │ Processing   │
        │ Collection   │            │ & Validation │
        │ Agents       │            │ Agents       │
        └───────┬──────┘            └──────┬───────┘
                │                           │
        ┌───────▼──────────────────────────▼───────┐
        │         Data Storage & Management         │
        │    (SQLite/PostgreSQL + File System)      │
        └───────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼──────┐    ┌──────▼───────┐
            │ Update       │    │ Reporting &  │
            │ Agents       │    │ Visualization│
            └──────────────┘    └──────────────┘
```

---

## Agent Types & Responsibilities

### 1. **Orchestrator Agent** (Master Claude Instance)
**Purpose:** Project management, workflow coordination, human escalation

**Capabilities:**
- Maintains project state and progress
- Assigns tasks to specialized agents
- Identifies when human review is needed
- Generates status reports
- Manages data quality thresholds

**Implementation:**
- Long-running Claude API session with extended thinking
- Maintains conversation history for context
- Uses artifacts for project dashboards

---

### 2. **Data Collection Agents**

#### **2A. Terminal Discovery Agent**
**Task:** Find all terminals with IRS TCNs

**Process:**
1. Web search for IRS Publication 510 and updates
2. Extract terminal listings with TCNs
3. Cross-reference with existing database
4. Identify new terminals for addition
5. Flag terminals removed from IRS list

**Tools Used:**
- `web_search` - Find IRS publications
- `web_fetch` - Download PDFs/pages
- Python (pymupdf/pdfplumber) - Extract data from PDFs
- Structured output to database

**Automation Level:** 95% - Human review only for ambiguous cases

---

#### **2B. Pipeline Tariff Agent**
**Task:** Collect and update pipeline tariffs from FERC

**Process:**
1. Access FERC tariff database (https://etariff.ferc.gov)
2. Search for pipeline company filings
3. Download relevant tariff documents
4. Extract rate tables using OCR/parsing
5. Convert to standardized format ($/gallon)
6. Store with effective dates

**Tools Used:**
- `web_search` - Find current tariffs
- `web_fetch` - Download tariff PDFs
- Python libraries:
  - `pdfplumber` - Extract tables from PDFs
  - `tabula-py` - Parse complex tariff tables
  - `pytesseract` - OCR for scanned documents
- Pattern matching for rate extraction

**Automation Level:** 85% - Human review for new pipeline systems or unusual formats

**Example Code:**
```python
import pdfplumber
import re

def extract_pipeline_tariffs(pdf_path):
    """Extract tariff rates from FERC filing PDF"""
    rates = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                # Pattern match for origin-destination-rate
                for row in table:
                    if contains_tariff_pattern(row):
                        rate = parse_tariff_row(row)
                        rates.append(rate)
    return rates
```

---

#### **2C. Rail Rate Agent**
**Task:** Collect rail tariffs (especially ethanol)

**Process:**
1. Monitor Class I railroad websites for rate updates
2. Access STB (Surface Transportation Board) filings
3. Parse rail tariff documents
4. Track mileage-based rates and fuel surcharges
5. Maintain railroad routing information

**Tools Used:**
- `web_search` + `web_fetch` - Railroad websites, STB database
- Python parsing for structured data
- Geographic calculations for routing

**Automation Level:** 80% - Rail tariffs often require interpretation

---

#### **2D. Terminal Information Agent**
**Task:** Gather terminal operational details

**Process:**
1. Search for terminal operator websites
2. Extract: capacity, products handled, receiving methods
3. Identify pipeline connections from tariff data
4. Locate rail sidings using geographic data
5. Determine marine/dock access

**Tools Used:**
- `web_search` - Terminal operator information
- `web_fetch` - Company websites, terminal fact sheets
- Cross-reference with pipeline/rail data
- GIS analysis for infrastructure proximity

**Automation Level:** 75% - Some terminals have limited public information

---

#### **2E. Refinery Linkage Agent**
**Task:** Map refineries to distribution networks

**Process:**
1. Access EIA refinery database
2. Identify refinery tailgate pipeline connections
3. Determine product slate and volumes
4. Map to terminal supply chains
5. Track ownership changes

**Tools Used:**
- `web_search` - EIA data, company disclosures
- `web_fetch` - EIA-810, EIA-820 reports
- Parsing of structured energy data

**Automation Level:** 85% - EIA data is well-structured

---

#### **2F. Ownership Tracking Agent**
**Task:** Monitor asset ownership changes

**Process:**
1. Set up Google Alerts for terminal/pipeline M&A
2. Monitor SEC filings (8-K, merger documents)
3. Track bankruptcy proceedings
4. Update ownership records with effective dates

**Tools Used:**
- `web_search` - News monitoring, SEC EDGAR
- RSS/alert monitoring
- Document parsing for transaction details

**Automation Level:** 70% - Requires interpretation of transaction terms

---

### 3. **Processing & Validation Agents**

#### **3A. Data Normalization Agent**
**Task:** Standardize data from multiple sources

**Process:**
1. Convert units (cents/barrel → $/gallon)
2. Standardize location names (county matching)
3. Normalize company names (BP vs BP Products)
4. Geocode addresses to lat/long
5. Validate data types and ranges

**Tools Used:**
- Python data processing (pandas)
- Geocoding APIs
- Fuzzy matching for name standardization

**Automation Level:** 90% - Rule-based with exception handling

---

#### **3B. Quality Assurance Agent**
**Task:** Validate data completeness and accuracy

**Process:**
1. Check for required fields
2. Validate rate ranges (flag outliers)
3. Verify geographic consistency
4. Cross-reference terminal-pipeline linkages
5. Identify data gaps

**Tools Used:**
- Statistical analysis for outlier detection
- Graph analysis for network validation
- Completeness scoring

**Automation Level:** 95% - Automated checks with human review of failures

---

#### **3C. Linkage Validation Agent**
**Task:** Ensure end-to-end supply chain connections

**Process:**
1. Verify terminal → transportation → refinery paths
2. Check for orphaned records (terminals with no connections)
3. Validate product type consistency
4. Calculate path distances and times
5. Flag impossible connections

**Tools Used:**
- Graph database queries (Neo4j or networkx)
- Geographic validation
- Logic checking

**Automation Level:** 90%

---

### 4. **Maintenance & Update Agents**

#### **4A. Scheduled Update Agent**
**Task:** Execute regular data refresh cycles

**Process:**
1. Run weekly checks for new tariff filings
2. Monthly terminal census updates
3. Quarterly comprehensive reviews
4. Annual full audit

**Implementation:**
- Cron jobs triggering Claude API calls
- Workflow orchestration (Airflow, Prefect, or custom)
- Progress tracking and logging

**Automation Level:** 95%

---

#### **4B. Change Detection Agent**
**Task:** Identify when data has changed

**Process:**
1. Compare current data to historical versions
2. Flag material changes (>5% rate change)
3. Identify new terminals/pipelines
4. Detect removed assets
5. Generate change summary

**Automation Level:** 100%

---

### 5. **Reporting & Visualization Agents**

#### **5A. Dashboard Agent**
**Task:** Generate interactive status dashboards

**Process:**
1. Create data summary statistics
2. Build network visualization
3. Generate maps with terminal/pipeline overlays
4. Produce data quality scorecards

**Tools Used:**
- React artifacts for interactive dashboards
- KML generation for mapping
- Plotly/D3.js for visualizations

**Automation Level:** 100%

---

#### **5B. Report Generation Agent**
**Task:** Create stakeholder reports

**Process:**
1. Monthly progress reports
2. Quarterly data quality reports
3. Ad-hoc analysis on request
4. Exception reports (failed validations)

**Tools Used:**
- Document creation (docx, PDF)
- Data summarization
- Natural language generation

**Automation Level:** 100%

---

## Technical Implementation

### Database Schema

```sql
-- Terminals Table
CREATE TABLE terminals (
    terminal_id TEXT PRIMARY KEY,
    terminal_name TEXT,
    irs_tcn TEXT UNIQUE,
    state TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    operator TEXT,
    owner TEXT,
    capacity_bpd INTEGER,
    products_handled TEXT[], -- Array of product types
    receiving_methods TEXT[], -- Pipeline, Rail, Truck, Marine
    effective_date DATE,
    end_date DATE,
    data_quality_score REAL,
    last_verified TIMESTAMP
);

-- Transportation Assets
CREATE TABLE pipelines (
    pipeline_id TEXT PRIMARY KEY,
    pipeline_name TEXT,
    operator TEXT,
    owner TEXT,
    pipeline_type TEXT, -- Common carrier, Private
    product_types TEXT[],
    origin_point TEXT,
    destination_point TEXT,
    length_miles REAL,
    effective_date DATE,
    end_date DATE
);

CREATE TABLE rail_connections (
    rail_connection_id TEXT PRIMARY KEY,
    railroad_name TEXT,
    terminal_id TEXT REFERENCES terminals(terminal_id),
    siding_location TEXT,
    latitude REAL,
    longitude REAL,
    effective_date DATE,
    end_date DATE
);

CREATE TABLE marine_facilities (
    dock_id TEXT PRIMARY KEY,
    facility_name TEXT,
    terminal_id TEXT REFERENCES terminals(terminal_id),
    waterway TEXT,
    vessel_types TEXT[],
    effective_date DATE,
    end_date DATE
);

-- Refineries
CREATE TABLE refineries (
    refinery_id TEXT PRIMARY KEY,
    refinery_name TEXT,
    operator TEXT,
    location TEXT,
    latitude REAL,
    longitude REAL,
    capacity_bpd INTEGER,
    product_slate JSONB,
    effective_date DATE,
    end_date DATE
);

-- Connections (Links)
CREATE TABLE terminal_pipeline_links (
    link_id TEXT PRIMARY KEY,
    terminal_id TEXT REFERENCES terminals(terminal_id),
    pipeline_id TEXT REFERENCES pipelines(pipeline_id),
    connection_type TEXT, -- Receives, Ships
    effective_date DATE,
    end_date DATE
);

CREATE TABLE pipeline_refinery_links (
    link_id TEXT PRIMARY KEY,
    pipeline_id TEXT REFERENCES pipelines(pipeline_id),
    refinery_id TEXT REFERENCES refineries(refinery_id),
    connection_point TEXT,
    effective_date DATE,
    end_date DATE
);

-- Costings
CREATE TABLE pipeline_tariffs (
    tariff_id TEXT PRIMARY KEY,
    pipeline_id TEXT REFERENCES pipelines(pipeline_id),
    origin TEXT,
    destination TEXT,
    product_type TEXT,
    rate_per_gallon REAL,
    rate_basis TEXT, -- $/gallon, cents/barrel, etc
    effective_date DATE,
    end_date DATE,
    source_document TEXT, -- Path to tariff PDF
    ferc_tariff_number TEXT
);

CREATE TABLE terminal_rates (
    rate_id TEXT PRIMARY KEY,
    terminal_id TEXT REFERENCES terminals(terminal_id),
    rate_type TEXT, -- Throughput, Additive, Facilities
    product_type TEXT,
    rate_per_gallon REAL,
    effective_date DATE,
    end_date DATE,
    source_document TEXT
);

CREATE TABLE rail_rates (
    rate_id TEXT PRIMARY KEY,
    railroad_name TEXT,
    origin TEXT,
    destination TEXT,
    product_type TEXT,
    rate_per_gallon REAL,
    distance_miles REAL,
    fuel_surcharge REAL,
    effective_date DATE,
    end_date DATE,
    source_document TEXT
);

-- Ownership History
CREATE TABLE ownership_changes (
    change_id TEXT PRIMARY KEY,
    asset_type TEXT, -- Terminal, Pipeline, Refinery
    asset_id TEXT,
    previous_owner TEXT,
    new_owner TEXT,
    transaction_date DATE,
    transaction_type TEXT, -- Acquisition, Merger, Divestiture
    source_document TEXT,
    notes TEXT
);

-- Data Quality Tracking
CREATE TABLE data_quality_log (
    log_id TEXT PRIMARY KEY,
    record_type TEXT,
    record_id TEXT,
    quality_check TEXT,
    check_result TEXT, -- Pass, Fail, Warning
    check_timestamp TIMESTAMP,
    agent_name TEXT
);

-- Agent Task Queue
CREATE TABLE agent_tasks (
    task_id TEXT PRIMARY KEY,
    agent_type TEXT,
    task_description TEXT,
    priority INTEGER,
    status TEXT, -- Pending, In Progress, Completed, Failed
    assigned_timestamp TIMESTAMP,
    completed_timestamp TIMESTAMP,
    result_summary TEXT,
    requires_human_review BOOLEAN
);
```

---

## Workflow Orchestration System

### Using Python + Claude API

```python
# orchestrator.py - Main coordination script

import anthropic
import sqlite3
from datetime import datetime, timedelta
import json

class SupplyChainOrchestrator:
    """
    Master orchestrator that coordinates all agent activities
    """
    
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.db = sqlite3.connect('supply_chain.db')
        self.model = "claude-sonnet-4-20250514"
        
    def create_agent_task(self, agent_type, description, priority=5):
        """Add task to queue for specific agent"""
        cursor = self.db.cursor()
        task_id = f"{agent_type}_{datetime.now().isoformat()}"
        cursor.execute("""
            INSERT INTO agent_tasks 
            (task_id, agent_type, task_description, priority, status, assigned_timestamp)
            VALUES (?, ?, ?, ?, 'Pending', ?)
        """, (task_id, agent_type, description, priority, datetime.now()))
        self.db.commit()
        return task_id
    
    def execute_agent_task(self, task_id):
        """Execute a single agent task using Claude"""
        cursor = self.db.cursor()
        task = cursor.execute("""
            SELECT agent_type, task_description 
            FROM agent_tasks 
            WHERE task_id = ?
        """, (task_id,)).fetchone()
        
        agent_type, description = task
        
        # Update status
        cursor.execute("""
            UPDATE agent_tasks 
            SET status = 'In Progress' 
            WHERE task_id = ?
        """, (task_id,))
        self.db.commit()
        
        # Create specialized system prompt for agent type
        system_prompt = self.get_agent_system_prompt(agent_type)
        
        # Execute using Claude
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": description
                }]
            )
            
            result = response.content[0].text
            
            # Parse result and determine if human review needed
            requires_review = self.assess_result_quality(result, agent_type)
            
            # Update task status
            cursor.execute("""
                UPDATE agent_tasks 
                SET status = 'Completed',
                    completed_timestamp = ?,
                    result_summary = ?,
                    requires_human_review = ?
                WHERE task_id = ?
            """, (datetime.now(), result[:500], requires_review, task_id))
            self.db.commit()
            
            return result, requires_review
            
        except Exception as e:
            cursor.execute("""
                UPDATE agent_tasks 
                SET status = 'Failed',
                    result_summary = ?
                WHERE task_id = ?
            """, (str(e), task_id))
            self.db.commit()
            raise
    
    def get_agent_system_prompt(self, agent_type):
        """Return specialized system prompt for each agent type"""
        
        base_prompt = """You are a specialized data collection and processing agent 
        for a refined products supply chain mapping project. Your role is to be 
        thorough, accurate, and autonomous while flagging ambiguous cases for human review."""
        
        agent_prompts = {
            "terminal_discovery": base_prompt + """
            
            Your specific task is to find terminals with IRS Terminal Control Numbers (TCNs).
            
            Process:
            1. Search for IRS Publication 510 and any updates
            2. Extract all listed terminals with their TCNs
            3. Parse: Terminal Name, Location (City, State), TCN, Operator
            4. Return structured JSON format
            5. Flag any ambiguous entries for human review
            
            Output format:
            {
                "terminals": [
                    {
                        "name": "Terminal Name",
                        "city": "City",
                        "state": "ST",
                        "tcn": "XX-XXXXXXX",
                        "operator": "Company Name",
                        "confidence": "high|medium|low"
                    }
                ],
                "requires_review": ["List of terminal names with low confidence"],
                "sources": ["List of URLs/documents used"]
            }
            """,
            
            "pipeline_tariff": base_prompt + """
            
            Your task is to extract pipeline tariffs from FERC filings.
            
            Process:
            1. Search FERC eTariff database for specified pipeline
            2. Download current tariff document
            3. Extract rate tables (origin, destination, rate)
            4. Convert all rates to $/gallon
            5. Include effective dates
            
            Handle:
            - Tables in various formats (PDF, scanned images)
            - Unit conversions (cents/barrel → $/gallon)
            - Multiple rate schedules
            
            Output JSON format with all extracted rates.
            Flag unusual rates (>$0.50/gal) for review.
            """,
            
            # Add more agent-specific prompts...
        }
        
        return agent_prompts.get(agent_type, base_prompt)
    
    def assess_result_quality(self, result, agent_type):
        """Determine if result needs human review"""
        # Simple heuristic - can be made more sophisticated
        try:
            data = json.loads(result)
            if 'requires_review' in data and data['requires_review']:
                return True
            if 'confidence' in data:
                low_confidence = [item for item in data.get('terminals', []) 
                                if item.get('confidence') == 'low']
                return len(low_confidence) > 0
        except:
            return True  # If can't parse, needs review
        
        return False
    
    def daily_orchestration(self):
        """Main daily workflow - runs all routine tasks"""
        
        print(f"Starting daily orchestration: {datetime.now()}")
        
        # 1. Check for new FERC tariff filings (daily)
        self.create_agent_task(
            "pipeline_tariff",
            "Check FERC eTariff for new pipeline tariff filings from last 24 hours",
            priority=8
        )
        
        # 2. Monitor for terminal ownership changes (daily)
        self.create_agent_task(
            "ownership_tracking",
            "Search for terminal/pipeline M&A announcements from last 24 hours",
            priority=7
        )
        
        # 3. Validate data quality on random sample (daily)
        self.create_agent_task(
            "quality_assurance",
            "Run quality checks on 50 random terminal records",
            priority=6
        )
        
        # Execute all pending tasks
        self.process_task_queue()
    
    def weekly_orchestration(self):
        """Weekly deep checks"""
        
        # Terminal census update
        self.create_agent_task(
            "terminal_discovery",
            "Check IRS Publication 510 for new terminals added this week",
            priority=8
        )
        
        # Rail rate updates
        self.create_agent_task(
            "rail_rate",
            "Check Class I railroad websites for rate updates",
            priority=7
        )
        
    def monthly_orchestration(self):
        """Monthly comprehensive updates"""
        
        # Full terminal verification
        self.create_agent_task(
            "terminal_information",
            "Update operational details for all terminals added > 30 days ago",
            priority=9
        )
        
        # Refinery linkage audit
        self.create_agent_task(
            "refinery_linkage",
            "Verify refinery connections and product slates from EIA data",
            priority=8
        )
    
    def process_task_queue(self, max_tasks=10):
        """Process pending tasks in priority order"""
        cursor = self.db.cursor()
        tasks = cursor.execute("""
            SELECT task_id FROM agent_tasks 
            WHERE status = 'Pending'
            ORDER BY priority DESC, assigned_timestamp ASC
            LIMIT ?
        """, (max_tasks,)).fetchall()
        
        results = []
        for (task_id,) in tasks:
            result, needs_review = self.execute_agent_task(task_id)
            results.append({
                'task_id': task_id,
                'result': result,
                'needs_review': needs_review
            })
        
        # Generate summary for human review
        review_items = [r for r in results if r['needs_review']]
        if review_items:
            self.generate_human_review_report(review_items)
        
        return results
    
    def generate_human_review_report(self, items):
        """Create summary of items needing human attention"""
        # This would send email, create dashboard alert, etc.
        print(f"\n⚠️  {len(items)} items require human review")
        for item in items:
            print(f"  - Task: {item['task_id']}")


# Example usage
if __name__ == "__main__":
    orchestrator = SupplyChainOrchestrator(api_key="your-api-key")
    
    # Run daily tasks
    orchestrator.daily_orchestration()
```

---

## Data Collection Agent Example

```python
# terminal_discovery_agent.py

import anthropic
from web_search import search_web
from pdf_parser import extract_text_from_pdf
import json
import re

class TerminalDiscoveryAgent:
    """
    Specialized agent for discovering terminals with IRS TCNs
    """
    
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        
    def discover_terminals(self):
        """Main discovery process"""
        
        # Step 1: Find IRS Publication 510
        pub_510_url = self.find_irs_publication_510()
        
        # Step 2: Download and parse
        terminal_data = self.extract_terminals_from_publication(pub_510_url)
        
        # Step 3: Validate and structure
        validated_terminals = self.validate_terminal_data(terminal_data)
        
        # Step 4: Check for updates since last run
        new_terminals = self.identify_new_terminals(validated_terminals)
        
        return new_terminals
    
    def find_irs_publication_510(self):
        """Use web search to find current Pub 510"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": """Search for the current version of IRS Publication 510 
                (Excise Taxes). Find the official IRS.gov URL for the PDF download.
                
                Return only the direct PDF URL."""
            }],
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }]
        )
        
        # Extract URL from response
        url = self.parse_url_from_response(response)
        return url
    
    def extract_terminals_from_publication(self, pdf_url):
        """Extract terminal listings from IRS pub"""
        
        # Download PDF
        pdf_text = extract_text_from_pdf(pdf_url)
        
        # Use Claude to parse structured data
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": f"""Parse this IRS Publication 510 text and extract all 
                terminal listings with their Terminal Control Numbers (TCNs).
                
                Each terminal entry should include:
                - Terminal name
                - City and State
                - Terminal Control Number (TCN format: XX-XXXXXXX)
                - Operator/owner name
                
                Return as JSON array.
                
                Text:
                {pdf_text[:50000]}  # Truncate if too long
                """
            }]
        )
        
        # Parse JSON response
        terminals = json.loads(response.content[0].text)
        return terminals
    
    def validate_terminal_data(self, terminals):
        """Validate extracted data quality"""
        
        validated = []
        for terminal in terminals:
            # Check TCN format
            if not re.match(r'\d{2}-\d{7}', terminal.get('tcn', '')):
                terminal['confidence'] = 'low'
                terminal['issues'] = ['Invalid TCN format']
            else:
                terminal['confidence'] = 'high'
            
            validated.append(terminal)
        
        return validated
    
    # Additional methods...
```

---

## Human-in-the-Loop Interface

### Web Dashboard for Review Queue

```python
# dashboard.py - Simple Flask app for human review

from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard showing items needing review"""
    db = sqlite3.connect('supply_chain.db')
    cursor = db.cursor()
    
    # Get tasks needing review
    tasks = cursor.execute("""
        SELECT task_id, agent_type, task_description, result_summary
        FROM agent_tasks
        WHERE requires_human_review = 1 AND status = 'Completed'
        ORDER BY completed_timestamp DESC
    """).fetchall()
    
    return render_template('dashboard.html', tasks=tasks)

@app.route('/review/<task_id>')
def review_task(task_id):
    """Detailed view of single task"""
    db = sqlite3.connect('supply_chain.db')
    cursor = db.cursor()
    
    task = cursor.execute("""
        SELECT * FROM agent_tasks WHERE task_id = ?
    """, (task_id,)).fetchone()
    
    return render_template('review.html', task=task)

@app.route('/approve/<task_id>', methods=['POST'])
def approve_task(task_id):
    """Human approves agent result"""
    db = sqlite3.connect('supply_chain.db')
    cursor = db.cursor()
    
    # Update task status
    cursor.execute("""
        UPDATE agent_tasks 
        SET requires_human_review = 0,
            status = 'Approved'
        WHERE task_id = ?
    """, (task_id,))
    db.commit()
    
    return jsonify({'status': 'approved'})

# Run dashboard
if __name__ == '__main__':
    app.run(port=5000)
```

---

## Deployment Strategy

### Phase 1: Proof of Concept (Weeks 1-4)

**Goal:** Validate agent-driven approach with limited scope

1. **Set up infrastructure:**
   - SQLite database with core tables
   - Python environment with Claude API
   - Basic orchestrator script

2. **Deploy 3 agents:**
   - Terminal Discovery Agent
   - Pipeline Tariff Agent (1-2 pipelines)
   - Quality Assurance Agent

3. **Test on pilot scope:**
   - 10-15 terminals
   - 2-3 pipelines
   - Run daily for 2 weeks

4. **Measure:**
   - Automation rate achieved
   - Data quality scores
   - Human review time required

**Expected Outcome:** 70-80% automation with acceptable quality

---

### Phase 2: Expand Coverage (Weeks 5-12)

1. **Add more agent types:**
   - Rail Rate Agent
   - Terminal Information Agent
   - Ownership Tracking Agent

2. **Scale up scope:**
   - Expand to 50-100 terminals
   - Add 10-15 major pipelines
   - Include ethanol rail network

3. **Improve orchestration:**
   - Add scheduling (cron jobs)
   - Build review dashboard
   - Implement email alerts

4. **Refine prompts:**
   - Based on POC learnings
   - Add error handling patterns
   - Improve data extraction accuracy

---

### Phase 3: Full Production (Weeks 13-24)

1. **Complete agent suite:**
   - All 13 agent types deployed
   - Full terminal coverage (200-500+)
   - Complete pipeline/rail networks

2. **Production infrastructure:**
   - Move to PostgreSQL
   - Deploy on cloud (AWS/GCP/Azure)
   - Add monitoring and alerting
   - Implement backup/recovery

3. **Maintenance automation:**
   - Scheduled daily/weekly/monthly runs
   - Automatic quality reporting
   - Change detection and alerts

4. **Human review optimization:**
   - Streamlined review interface
   - Priority queue management
   - Approval workflows

---

## Cost Estimation

### Claude API Costs (Approximate)

**Daily operations:**
- Terminal Discovery: 1 call/day × $0.50 = $0.50
- Pipeline Tariffs: 5 calls/day × $0.75 = $3.75
- Rail Rates: 2 calls/day × $0.60 = $1.20
- Ownership Tracking: 3 calls/day × $0.40 = $1.20
- QA Checks: 10 calls/day × $0.30 = $3.00

**Daily total: ~$10-15**
**Monthly total: ~$300-450**

**Plus one-time setup:**
- Initial data load: ~$500-1000
- Historical backfill: ~$200-500

**Annual estimate: $4,000-6,000** for Claude API usage

This is remarkably cost-effective compared to:
- 1 FTE data analyst: $80,000-120,000/year
- Commercial data subscriptions: $50,000-200,000/year
- Manual process inefficiency: Immeasurable

---

## Human Resource Requirements

### With Agent System:

**Initial Setup (Weeks 1-4):**
- 1 technical lead: 40 hours
- 1 SME for validation: 20 hours

**Ongoing Operations:**
- Review queue: 5-10 hours/week
- Exception handling: 3-5 hours/week
- Strategic oversight: 2-3 hours/week

**Total: 10-18 hours/week (~0.25-0.5 FTE)**

### Without Agent System (Traditional Approach):

- Data collection: 30 hours/week
- Processing/validation: 20 hours/week
- Updates/maintenance: 15 hours/week

**Total: 65 hours/week (~1.5-2 FTE)**

**Efficiency gain: 70-85% reduction in human hours**

---

## Risk Mitigation

### Quality Control Safeguards

1. **Multi-layer validation:**
   - Agent self-validation (confidence scores)
   - QA agent cross-checking
   - Statistical outlier detection
   - Human review of flagged items

2. **Progressive automation:**
   - Start with high human review rate (50%)
   - Gradually reduce as confidence increases
   - Never go below 10% sampling

3. **Fallback mechanisms:**
   - Agent failures trigger alerts
   - Critical tasks have backup manual process
   - Regular audits against known-good data

4. **Version control:**
   - All data changes tracked
   - Ability to rollback bad updates
   - Historical comparison reports

---

## Success Metrics

**Track these KPIs:**

1. **Automation Rate:** % of tasks completed without human intervention
   - Target: 80-90%

2. **Data Quality Score:** Completeness + accuracy measures
   - Target: 95%+

3. **Update Latency:** Time from source change to database update
   - Target: <24 hours for critical items

4. **Human Review Time:** Hours/week spent on review
   - Target: <15 hours

5. **Cost per Record:** Total cost / number of terminal records
   - Target: <$10/record/year

6. **Coverage:** % of IRS TCN terminals in system
   - Target: 95%+

---

## Next Steps to Get Started

1. **Week 1: Environment Setup**
   - Set up Claude API access
   - Create SQLite database with schema
   - Build basic orchestrator

2. **Week 2: First Agent**
   - Deploy Terminal Discovery Agent
   - Run on 5 test terminals
   - Validate output quality

3. **Week 3: Expand**
   - Add Pipeline Tariff Agent
   - Test on 2 pipelines
   - Refine prompts

4. **Week 4: Review & Iterate**
   - Analyze results
   - Calculate automation rate
   - Plan Phase 2 expansion
