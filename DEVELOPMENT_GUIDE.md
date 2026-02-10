# DEVELOPMENT GUIDE - Supply Chain Mapping Project

**Quick Reference:** Common patterns, code snippets, and how-tos for this project

Last Updated: February 10, 2026

---

## 📚 TABLE OF CONTENTS

1. [How to Use config.py](#how-to-use-configpy)
2. [Creating a New Agent](#creating-a-new-agent)
3. [Working with the Database](#working-with-the-database)
4. [Processing PDFs](#processing-pdfs)
5. [Using the Orchestrator](#using-the-orchestrator)
6. [Common Code Patterns](#common-code-patterns)
7. [Testing Your Code](#testing-your-code)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 How to Use config.py

### Basic Import

**At the top of ANY Python file:**

```python
import config
```

That's it! Now you have access to all paths and settings.

### Common Uses

#### Database Connection
```python
import config
import sqlite3

# Connect to database
conn = sqlite3.connect(config.DATABASE_PATH)
cursor = conn.cursor()

# Do your work
cursor.execute("SELECT * FROM terminals")

# Close when done
conn.close()
```

#### Access Tariff Library
```python
import config
import os
import glob

# Get all Colonial Pipeline tariffs
colonial_path = config.get_tariff_path('pipeline', 'Colonial')
pdf_files = glob.glob(os.path.join(colonial_path, "*.pdf"))

print(f"Found {len(pdf_files)} Colonial tariffs")
```

#### Use API Settings
```python
import config
import anthropic

# Create Claude client with config settings
client = anthropic.Anthropic(api_key=your_api_key)

response = client.messages.create(
    model=config.CLAUDE_MODEL,        # Uses setting from config
    max_tokens=config.DEFAULT_MAX_TOKENS,
    messages=[{"role": "user", "content": "Hello"}]
)
```

#### Check Data Quality
```python
import config

# Use quality thresholds from config
def needs_human_review(confidence_score):
    if confidence_score < config.MIN_CONFIDENCE_SCORE:
        return True  # Too low, needs review
    elif confidence_score >= config.HIGH_CONFIDENCE_SCORE:
        return False  # High confidence, auto-accept
    else:
        return True  # Medium confidence, review to be safe
```

### All Available Settings

```python
# Paths
config.PROJECT_ROOT           # Root of GitHub repo
config.DATABASE_PATH          # supply_chain.db location
config.TARIFF_LIBRARY         # Full tariff PDF collection
config.PIPELINE_TARIFFS       # Pipeline subfolder
config.RAIL_TARIFFS          # Railroad subfolder
config.TERMINAL_TARIFFS      # Terminal subfolder
config.SAMPLE_TARIFFS        # Sample PDFs for testing
config.OUTPUT_DIR            # Where to save reports

# API Settings
config.CLAUDE_MODEL          # "claude-sonnet-4-20250514"
config.DEFAULT_MAX_TOKENS    # 8000

# Quality Thresholds
config.MIN_CONFIDENCE_SCORE  # 0.7
config.HIGH_CONFIDENCE_SCORE # 0.9

# Priorities
config.PRIORITY_CRITICAL     # 10
config.PRIORITY_HIGH         # 8
config.PRIORITY_MEDIUM       # 5
config.PRIORITY_LOW          # 3

# Helper Functions
config.ensure_directories_exist()              # Create missing folders
config.get_tariff_path(type, name)            # Get path to operator folder
```

---

## 🤖 Creating a New Agent

### Template for New Agent

**Copy this template when creating a new agent:**

```python
#!/usr/bin/env python3
"""
[Agent Name] Agent
[Brief description of what this agent does]
"""

import anthropic
import sqlite3
import config
import json
from datetime import datetime

class [AgentName]Agent:
    """
    [Detailed description]
    
    Responsibilities:
    - [What it does]
    - [What it collects]
    - [What it validates]
    """
    
    def __init__(self, api_key, db_path=None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.db_path = db_path or config.DATABASE_PATH
        self.model = config.CLAUDE_MODEL
        
    def execute_task(self, parameters=None):
        """
        Main execution method
        
        Args:
            parameters: Dict with task-specific parameters
        
        Returns:
            Dict with results and metadata
        """
        print(f"Starting {self.__class__.__name__}...")
        
        # Step 1: Collect data
        data = self._collect_data(parameters)
        
        # Step 2: Validate
        validated = self._validate_data(data)
        
        # Step 3: Store
        self._store_results(validated)
        
        # Step 4: Return summary
        return {
            'status': 'completed',
            'items_collected': len(validated),
            'requires_review': self._check_review_needed(validated)
        }
    
    def _collect_data(self, parameters):
        """Implement data collection logic"""
        # Your code here
        pass
    
    def _validate_data(self, data):
        """Implement validation logic"""
        # Your code here
        pass
    
    def _store_results(self, data):
        """Store results in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Your SQL here
        
        conn.commit()
        conn.close()
    
    def _check_review_needed(self, data):
        """Determine if human review needed"""
        # Check confidence scores, data quality, etc.
        return False

# Command line usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent_name.py <API_KEY>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    agent = [AgentName]Agent(api_key)
    results = agent.execute_task()
    
    print(f"\nResults: {json.dumps(results, indent=2)}")
```

### Example: Copy terminal_discovery_agent.py

The `terminal_discovery_agent.py` is your working example. When building a new agent:

1. Copy `terminal_discovery_agent.py`
2. Rename it (e.g., `pipeline_tariff_agent.py`)
3. Change the class name
4. Update the methods for your specific task
5. Keep the same structure

---

## 💾 Working with the Database

### Connect to Database

```python
import config
import sqlite3

conn = sqlite3.connect(config.DATABASE_PATH)
cursor = conn.cursor()
```

### Insert Data

```python
# Insert a terminal
cursor.execute("""
    INSERT INTO terminals (
        terminal_id, terminal_name, state, city, irs_tcn
    ) VALUES (?, ?, ?, ?, ?)
""", (
    terminal_id,
    terminal_name,
    state,
    city,
    tcn
))

conn.commit()
```

### Query Data

```python
# Get all active terminals
terminals = cursor.execute("""
    SELECT * FROM v_active_terminals
""").fetchall()

for terminal in terminals:
    print(f"{terminal[1]} - {terminal[3]}, {terminal[4]}")
```

### Update Data

```python
# Update terminal operator
cursor.execute("""
    UPDATE terminals
    SET operator = ?, updated_at = ?
    WHERE terminal_id = ?
""", (new_operator, datetime.now(), terminal_id))

conn.commit()
```

### Always Close Connection

```python
# At the end of your function
conn.close()

# OR use context manager (better)
with sqlite3.connect(config.DATABASE_PATH) as conn:
    cursor = conn.cursor()
    # Do work
    # Auto-commits and closes
```

---

## 📄 Processing PDFs

### Extract Text from PDF

```python
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF"""
    text = ""
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    return text
```

### Extract Tables from PDF

```python
import pdfplumber

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF"""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            all_tables.extend(tables)
    
    return all_tables
```

### Use Claude to Parse PDF Content

```python
import config
import anthropic

def parse_tariff_with_claude(pdf_text, api_key):
    """Use Claude to extract structured data from PDF text"""
    
    client = anthropic.Anthropic(api_key=api_key)
    
    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": f"""Extract tariff rates from this PDF text.
            
Return JSON format:
{{
    "origin": "...",
    "destination": "...",
    "rate_per_gallon": 0.00,
    "effective_date": "YYYY-MM-DD"
}}

PDF Text:
{pdf_text[:10000]}"""
        }]
    )
    
    # Parse the response
    import json
    return json.loads(response.content[0].text)
```

---

## 🎛️ Using the Orchestrator

### Run from Command Line

```bash
# Check status
python orchestrator.py --api-key YOUR_KEY status

# Run daily tasks
python orchestrator.py --api-key YOUR_KEY daily

# Run weekly tasks
python orchestrator.py --api-key YOUR_KEY weekly

# View review queue
python orchestrator.py --api-key YOUR_KEY review

# Process specific agent type
python orchestrator.py --api-key YOUR_KEY process --agent-type terminal_discovery
```

### Create Tasks Programmatically

```python
from orchestrator import SupplyChainOrchestrator

orchestrator = SupplyChainOrchestrator(api_key)

# Create a task
task_id = orchestrator.create_task(
    agent_type='pipeline_tariff',
    description='Update Colonial Pipeline tariffs',
    parameters={'pipeline': 'Colonial'},
    priority=8
)

# Process tasks
orchestrator.process_task_queue(max_tasks=5)
```

---

## 🔄 Common Code Patterns

### Pattern 1: Generate Unique IDs

```python
import hashlib
from datetime import datetime

def generate_id(prefix, *components):
    """Generate unique ID from components"""
    # Combine components
    combined = "_".join(str(c) for c in components)
    
    # Create hash
    hash_val = hashlib.md5(combined.encode()).hexdigest()[:8]
    
    # Format: PREFIX_HASH_TIMESTAMP
    timestamp = datetime.now().strftime('%Y%m%d')
    return f"{prefix}_{hash_val}_{timestamp}"

# Example
terminal_id = generate_id("TERM", state, city, tcn)
# Result: TERM_a1b2c3d4_20260210
```

### Pattern 2: Quality Scoring

```python
def calculate_quality_score(data, required_fields):
    """Calculate data quality score (0-1)"""
    score = 1.0
    
    # Check required fields
    for field in required_fields:
        if not data.get(field):
            score -= 0.2
    
    # Bonus for optional enrichment
    if data.get('latitude') and data.get('longitude'):
        score += 0.1
    
    return max(0.0, min(1.0, score))  # Clamp between 0-1
```

### Pattern 3: Confidence Assessment

```python
import config

def assess_confidence(data, issues):
    """Determine confidence level"""
    if len(issues) == 0:
        return 'high', 0.95
    elif len(issues) <= 2:
        return 'medium', 0.75
    else:
        return 'low', 0.40

def requires_review(confidence_score):
    """Check if human review needed based on config"""
    return confidence_score < config.MIN_CONFIDENCE_SCORE
```

### Pattern 4: Error Handling

```python
def safe_api_call(func, *args, max_retries=3, **kwargs):
    """Retry API calls with exponential backoff"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise  # Final attempt, raise the error
            
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Retrying in {wait_time}s...")
            time.sleep(wait_time)
```

---

## ✅ Testing Your Code

### Quick Test

```python
# At the bottom of your agent file
if __name__ == "__main__":
    # Test mode
    print("Testing mode...")
    
    agent = MyAgent(api_key="test-key")
    
    # Test individual methods
    test_data = {"name": "Test Terminal", "state": "TX"}
    validated = agent._validate_data(test_data)
    
    print(f"Validation result: {validated}")
```

### Test with Sample Data

```python
# Create test fixtures
TEST_TERMINAL = {
    'name': 'Test Terminal',
    'city': 'Houston',
    'state': 'TX',
    'tcn': '12-3456789'
}

def test_terminal_validation():
    agent = TerminalDiscoveryAgent("test-key")
    result = agent._validate_terminals([TEST_TERMINAL])
    assert result[0]['confidence'] == 'high'
    print("✓ Test passed")
```

---

## 🐛 Troubleshooting

### Common Issues

#### Can't Find config Module
```python
# Error: ModuleNotFoundError: No module named 'config'

# Fix: Make sure you're in the right directory
import os
print(os.getcwd())  # Should be .../supply-chain-mapping

# OR add to Python path
import sys
sys.path.append(r"C:\Users\jalex\supply-chain\supply-chain-mapping")
import config
```

#### Database Locked Error
```python
# Error: sqlite3.OperationalError: database is locked

# Fix: Close other connections
conn.close()

# OR use timeout
conn = sqlite3.connect(config.DATABASE_PATH, timeout=10.0)
```

#### API Rate Limits
```python
# Error: RateLimitError

# Fix: Add delays between calls
import time

for item in items:
    process_item(item)
    time.sleep(1)  # 1 second between calls
```

#### File Path Issues on Windows
```python
# Use raw strings or forward slashes
path = r"C:\Users\jalex\file.txt"  # Raw string
# OR
path = "C:/Users/jalex/file.txt"   # Forward slashes work on Windows!

# Better: Use os.path.join
import os
path = os.path.join("C:", "Users", "jalex", "file.txt")
```

---

## 📝 Quick Reference Commands

### Start New Session
```bash
cd C:\Users\jalex\supply-chain\supply-chain-mapping
```

### Run Tests
```bash
python config.py                    # Test config
python create_database.py          # Recreate database
python agent_name.py YOUR_API_KEY  # Test specific agent
```

### Check Status
```bash
python orchestrator.py --api-key YOUR_KEY status
```

### Database Queries
```bash
# Open database in command line
sqlite3 supply_chain.db

# Common queries
SELECT COUNT(*) FROM terminals;
SELECT * FROM v_review_queue;
SELECT * FROM agent_tasks ORDER BY created_at DESC LIMIT 10;

# Exit
.quit
```

---

## 💡 Best Practices

### Code Style
- ✅ Use config.py for all paths and settings
- ✅ Add docstrings to all functions
- ✅ Use meaningful variable names
- ✅ Keep functions short and focused
- ✅ Handle errors gracefully

### Database
- ✅ Always use parameterized queries (prevents SQL injection)
- ✅ Close connections when done
- ✅ Use transactions for multiple inserts
- ✅ Add indexes for frequently queried fields

### Documentation
- ✅ Update PROJECT_STATE.md after major changes
- ✅ Comment complex logic
- ✅ Keep this DEVELOPMENT_GUIDE.md current
- ✅ Add examples for new patterns

---

## 🔄 Updating This Guide

When you discover a new pattern or solution:

1. Open this file (DEVELOPMENT_GUIDE.md)
2. Add it to the appropriate section
3. Include a code example
4. Commit to GitHub
5. Now it's saved forever!

**This guide grows with your project!**

---

## 📚 Additional Resources

**Project Documentation:**
- PROJECT_STATE.md - Current status and roadmap
- README.md - Overview and setup
- agent_driven_framework.md - Complete architecture
- BEGINNERS_GUIDE.md - Non-technical user guide

**External Resources:**
- Anthropic API Docs: https://docs.anthropic.com
- SQLite Tutorial: https://www.sqlitetutorial.net
- Python PDF Processing: https://pdfplumber.readthedocs.io

---

**Last Updated:** February 10, 2026  
**Maintained By:** jalex  
**Questions?** Check PROJECT_STATE.md or start new Claude session with this file uploaded
