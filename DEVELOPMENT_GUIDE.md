# DEVELOPMENT GUIDE - Supply Chain Mapping Project

**Quick Reference:** Common patterns, code snippets, and how-tos for this project

Last Updated: February 11, 2026

---

## 📚 TABLE OF CONTENTS

1. [What Changed Today - 53 Table Schema](#what-changed-today)
2. [How to Use config.py](#how-to-use-configpy)
3. [Understanding the New Schema](#understanding-the-new-schema)
4. [Working with Normalized Costing Data](#working-with-normalized-costing-data)
5. [Creating a New Agent](#creating-a-new-agent)
6. [Working with the Database](#working-with-the-database)
7. [Processing PDFs](#processing-pdfs)
8. [Using the Orchestrator](#using-the-orchestrator)
9. [Common Code Patterns](#common-code-patterns)
10. [Testing Your Code](#testing-your-code)
11. [Troubleshooting](#troubleshooting)

---

## 🆕 WHAT CHANGED TODAY (Feb 11, 2026)

### Major Schema Evolution: 16 → 53 Tables

**Yesterday (Feb 10):**
- Simple 16-table structure
- Flat `transportation_costs` table with combined adders only
- No product hierarchy, no line item breakdown

**Today (Feb 11):**
- **53 tables** with complete normalized data model
- Captures full **Costing → Shipping → BCS → Tenant** workflow
- Multi-tenant architecture with alias framework
- Proper temporal tracking (start_date/end_date)
- Production parity with old PostgreSQL system

### Impact on Your Code

**If you have existing agent code, you'll need to update:**

❌ **OLD WAY (16-table schema):**
```python
# Insert combined adder only
cursor.execute("""
    INSERT INTO transportation_costs (
        terminal_id, product_type, combined_adder, effective_date
    ) VALUES (?, ?, ?, ?)
""", (terminal_id, 'E10', 0.1234, '2024-01-01'))
```

✅ **NEW WAY (53-table schema):**
```python
# 1. Create shipping period
period_id = create_shipping_period(terminal_id, '2024-01-01', '2024-12-31')

# 2. Insert individual costing components
for component in ['tariff', 'facilities_charge', 'throughput', 'tvm']:
    cursor.execute("""
        INSERT INTO costing (
            terminal_id, product_category_id, costing_item_id,
            costing_value, shipping_period_id, start_date, end_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (terminal_id, product_cat_id, costing_item_id,
          component_value, period_id, '2024-01-01', '2024-12-31'))

# 3. Generate shipping line items (aggregates costing)
create_shipping_line_items(period_id)
```

**Don't worry!** This guide shows you exactly how to work with the new structure.

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

---

## 🗂️ Understanding the New Schema

### The 9 Tiers of Tables

The 53 tables are organized into logical groups:

#### **TIER 1: Reference Data (5 tables)**
These are lookup tables pre-seeded with values:
- `product_categories` - GAS, ETH, DSL
- `products` - Clear Gas, E10, E15, E85, Diesel
- `line_item_types` - Tariff, Facilities Charge, RIN, CARB, etc.
- `costing_items` - Detailed cost components
- `price_days` - Prior Day, Same Day, etc.

```python
# Get product category ID for gasoline
cursor.execute("""
    SELECT product_category_id 
    FROM product_categories 
    WHERE product_category_code = 'GAS'
""")
gas_category_id = cursor.fetchone()[0]
```

#### **TIER 2: Assets (5 tables)**
Physical infrastructure:
- `terminals` - 227 terminals (from yesterday)
- `terminal_markets` - Market groupings
- `pipelines` - Pipeline infrastructure
- `refineries` - Refinery locations
- `railroads` - Railroad carriers

#### **TIER 3: Relationships (7 tables)**
How assets connect:
- `terminal_products` - Which products at which terminals
- `terminal_pipeline_links` - Terminals connected to pipelines
- `pipeline_refinery_links` - Pipelines connected to refineries
- `rail_connections` - Rail sidings
- `marine_facilities` - Docks
- `shipping_paths` - Origin → destination routes
- `terminal_path_links` - Terminals on paths

#### **TIER 4: Costing System (10 tables)**
The heart of the system - where costs are calculated:

```
shipping_periods          ← Time periods for cost data
    ↓
costing                  ← Individual cost components
    ↓
(tariff components from:)
    pipeline_tariffs
    tariff_library
    tariff_costs
    tariff_path_links
    terminal_rates
    rail_rates
    ↓
spot_markets             ← Pricing locations
spot_market_location_links
```

**Key Concept:** Instead of storing one `combined_adder` per terminal/product, we now store individual components (tariff, facilities, throughput, etc.) that can be summed.

#### **TIER 5: Shipping Line Items (3 tables)**
Aggregated costs ready for publishing:
- `shipping_setup` - Configuration
- `shipping_line_items` - Final shipping costs by product
- `spot_indices` - Pricing indices

#### **TIER 6: BCS System (5 tables)**
Buying Cost Sheets for publishing to users:
- `bcs_types` - Shipping, Contract, etc.
- `bcs_period_statuses` - Draft, In Progress, Final
- `bcs` - Buying cost sheets
- `bcs_periods` - Time periods
- `bcs_line_items` - BCS details

#### **TIER 7: Multi-Tenant (6 tables)**
Cross-tenant ID mapping:
- `alias_types` - EN Master UUID, Tenant UUID, etc.
- `terminal_aliases`, `product_aliases`, `index_aliases`, etc.

#### **TIER 8: Error Tracking (6 tables)**
ETL error logging:
- `batches` - ETL batch tracking
- `terminal_alias_errors`, `product_alias_errors`, etc.

#### **TIER 9: Management (6 tables)**
Agent orchestration (from yesterday):
- `agent_tasks`, `data_quality_log`, `agent_metrics`, etc.

---

## 💰 Working with Normalized Costing Data

### The Costing Workflow

**OLD WAY (flat structure):**
```
Terminal + Product → Combined Adder ($0.1234/gal)
```

**NEW WAY (normalized structure):**
```
Terminal + Product Category → Shipping Period
    ↓
Multiple Costing Records:
    - Tariff:              $0.0450/gal
    - Facilities Charge:   $0.0150/gal
    - Throughput:          $0.0100/gal
    - TVM:                 $0.0034/gal
    - Basis:              -$0.0100/gal
    - Line Loss:           $0.0200/gal
    - Margin:              $0.0300/gal
    - Fuel Surcharge:      $0.0100/gal
    ↓
Sum = Combined Adder: $0.1234/gal
```

### Pattern 1: Create Shipping Period

```python
def create_shipping_period(terminal_id, start_date, end_date):
    """Create a shipping period for costing data"""
    
    period_id = generate_id("PERIOD", terminal_id, start_date)
    
    cursor.execute("""
        INSERT INTO shipping_periods (
            shipping_period_id, terminal_id, start_date, end_date,
            created_at, updated_at
        ) VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (period_id, terminal_id, start_date, end_date))
    
    return period_id
```

### Pattern 2: Insert Costing Components

```python
def insert_costing_component(terminal_id, product_category_id, 
                             costing_item_name, value, 
                             shipping_period_id, start_date, end_date):
    """Insert a single costing component"""
    
    # Get costing_item_id from name
    cursor.execute("""
        SELECT costing_item_id 
        FROM costing_items 
        WHERE costing_item_name = ?
    """, (costing_item_name,))
    costing_item_id = cursor.fetchone()[0]
    
    # Generate unique ID
    costing_id = generate_id("COST", terminal_id, product_category_id, 
                            costing_item_name)
    
    # Insert
    cursor.execute("""
        INSERT INTO costing (
            costing_id, terminal_id, product_category_id, 
            costing_item_id, costing_value, shipping_period_id,
            start_date, end_date, created_by, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (costing_id, terminal_id, product_category_id, costing_item_id,
          value, shipping_period_id, start_date, end_date, 'system'))
    
    return costing_id
```

### Pattern 3: Calculate Combined Adder

```python
def calculate_combined_adder(terminal_id, product_category_id, 
                             shipping_period_id):
    """Sum all costing components to get combined adder"""
    
    cursor.execute("""
        SELECT SUM(costing_value)
        FROM costing
        WHERE terminal_id = ?
          AND product_category_id = ?
          AND shipping_period_id = ?
    """, (terminal_id, product_category_id, shipping_period_id))
    
    result = cursor.fetchone()
    return result[0] if result[0] else 0.0
```

### Pattern 4: Create Shipping Line Items

```python
def create_shipping_line_items(shipping_period_id):
    """
    Generate shipping line items from costing data
    
    Creates line items for each product based on:
    - Base product costs (from costing table)
    - Line item types (Tariff, RIN, CARB, Combined Adder)
    - Spot indices (for pricing)
    """
    
    # Get all products for this terminal's period
    cursor.execute("""
        SELECT DISTINCT 
            c.terminal_id,
            tp.product_id,
            c.product_category_id,
            sp.start_date,
            sp.end_date
        FROM costing c
        JOIN shipping_periods sp USING (shipping_period_id)
        JOIN terminal_products tp ON c.terminal_id = tp.terminal_id
        JOIN products p ON tp.product_id = p.product_id
        WHERE c.shipping_period_id = ?
          AND p.product_category_id = c.product_category_id
    """, (shipping_period_id,))
    
    for row in cursor.fetchall():
        terminal_id, product_id, product_cat_id, start_date, end_date = row
        
        # Get combined adder for this product
        combined = calculate_combined_adder(terminal_id, product_cat_id, 
                                           shipping_period_id)
        
        # Create Combined Adder line item
        cursor.execute("""
            SELECT line_item_type_id 
            FROM line_item_types 
            WHERE line_item_type_name = 'Combined Adder'
        """)
        combined_adder_type_id = cursor.fetchone()[0]
        
        line_item_id = generate_id("LINE", shipping_period_id, product_id, 
                                   "combined")
        
        cursor.execute("""
            INSERT INTO shipping_line_items (
                shipping_line_item_id, shipping_period_id, product_id,
                line_item_type_id, line_item_adder, line_item_percent,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, (line_item_id, shipping_period_id, product_id,
              combined_adder_type_id, combined, 1.0))
        
        # Create other line item types (RIN, CARB, etc.) as needed
        # ... additional logic here
```

### Pattern 5: Query Current Costs

```python
def get_current_costs(terminal_id, product_id, as_of_date=None):
    """
    Get current costing breakdown for a terminal + product
    
    Returns dict with:
        - terminal_name
        - product_code
        - costing_components: list of {item_name, value}
        - combined_adder
        - period_start, period_end
    """
    
    if as_of_date is None:
        as_of_date = 'CURRENT_DATE'
    
    # Get costing breakdown
    cursor.execute("""
        SELECT 
            t.terminal_name,
            p.product_code,
            ci.costing_item_name,
            c.costing_value,
            sp.start_date,
            sp.end_date
        FROM costing c
        JOIN terminals t USING (terminal_id)
        JOIN products p ON p.product_category_id = c.product_category_id
        JOIN costing_items ci USING (costing_item_id)
        JOIN shipping_periods sp USING (shipping_period_id)
        WHERE c.terminal_id = ?
          AND p.product_id = ?
          AND c.start_date <= ?
          AND c.end_date >= ?
        ORDER BY ci.costing_item_name
    """, (terminal_id, product_id, as_of_date, as_of_date))
    
    rows = cursor.fetchall()
    
    if not rows:
        return None
    
    result = {
        'terminal_name': rows[0][0],
        'product_code': rows[0][1],
        'period_start': rows[0][4],
        'period_end': rows[0][5],
        'costing_components': [],
        'combined_adder': 0.0
    }
    
    for row in rows:
        item_name = row[2]
        value = row[3]
        
        result['costing_components'].append({
            'item_name': item_name,
            'value': value
        })
        result['combined_adder'] += value
    
    return result
```

---

## 🤖 Creating a New Agent

### Template for New Agent (Updated for 53-table schema)

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
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Step 1: Collect data
            data = self._collect_data(cursor, parameters)
            
            # Step 2: Validate
            validated = self._validate_data(data)
            
            # Step 3: Store
            self._store_results(cursor, validated)
            
            # Step 4: Commit
            conn.commit()
            
            # Step 5: Return summary
            return {
                'status': 'completed',
                'items_collected': len(validated),
                'requires_review': self._check_review_needed(validated)
            }
        
        except Exception as e:
            conn.rollback()
            return {
                'status': 'failed',
                'error': str(e)
            }
        finally:
            conn.close()
    
    def _collect_data(self, cursor, parameters):
        """Implement data collection logic"""
        # Your code here
        pass
    
    def _validate_data(self, data):
        """Implement validation logic"""
        # Your code here
        pass
    
    def _store_results(self, cursor, data):
        """Store results in database"""
        # Use patterns from this guide
        pass
    
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

---

## 💾 Working with the Database

### Connect to Database

```python
import config
import sqlite3

conn = sqlite3.connect(config.DATABASE_PATH)
cursor = conn.cursor()
```

### Common Queries for New Schema

#### Get Product Category ID
```python
def get_product_category_id(product_category_code):
    """Get product_category_id from code (GAS, ETH, DSL)"""
    cursor.execute("""
        SELECT product_category_id 
        FROM product_categories 
        WHERE product_category_code = ?
    """, (product_category_code,))
    return cursor.fetchone()[0]
```

#### Get Product ID
```python
def get_product_id(product_code):
    """Get product_id from code (CLEAR, E10, E15, etc.)"""
    cursor.execute("""
        SELECT product_id 
        FROM products 
        WHERE product_code = ?
    """, (product_code,))
    return cursor.fetchone()[0]
```

#### Get Costing Item ID
```python
def get_costing_item_id(item_name):
    """Get costing_item_id from name (tariff, facilities_charge, etc.)"""
    cursor.execute("""
        SELECT costing_item_id 
        FROM costing_items 
        WHERE costing_item_name = ?
    """, (item_name,))
    return cursor.fetchone()[0]
```

#### Get Line Item Type ID
```python
def get_line_item_type_id(type_name):
    """Get line_item_type_id from name (Tariff, RIN, Combined Adder, etc.)"""
    cursor.execute("""
        SELECT line_item_type_id 
        FROM line_item_types 
        WHERE line_item_type_name = ?
    """, (type_name,))
    return cursor.fetchone()[0]
```

### Insert Data with Foreign Keys

```python
# Example: Insert a terminal product
terminal_id = "TERM_12345"
product_id = get_product_id('E10')

cursor.execute("""
    INSERT INTO terminal_products (
        terminal_product_id, terminal_id, product_id, 
        shipping_status, created_at, updated_at
    ) VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
""", (
    generate_id("TERMPROD", terminal_id, product_id),
    terminal_id,
    product_id,
    1  # shipping_status = 1 (active)
))
```

### Query with Views

The schema includes helpful views:

```python
# Get all active terminals
cursor.execute("SELECT * FROM v_active_terminals")
terminals = cursor.fetchall()

# Get current shipping costs
cursor.execute("""
    SELECT * FROM v_current_shipping 
    WHERE terminal_id = ?
""", (terminal_id,))

# Get items needing review
cursor.execute("SELECT * FROM v_review_queue")
review_items = cursor.fetchall()
```

### Always Use Transactions

```python
# Use context manager (automatic commit/rollback)
with sqlite3.connect(config.DATABASE_PATH) as conn:
    cursor = conn.cursor()
    
    # Do multiple operations
    cursor.execute("INSERT INTO ...")
    cursor.execute("UPDATE ...")
    
    # Auto-commits if no errors
    # Auto-rolls back if exception
```

---

## 📄 Processing PDFs

(This section unchanged from yesterday - still relevant)

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

(This section unchanged from yesterday)

### Run from Command Line

```bash
# Check status
python orchestrator.py --api-key YOUR_KEY status

# Run daily tasks
python orchestrator.py --api-key YOUR_KEY daily

# Run weekly tasks
python orchestrator.py --api-key YOUR_KEY weekly
```

---

## 📐 Common Code Patterns

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

# Examples
terminal_id = generate_id("TERM", state, city, tcn)
period_id = generate_id("PERIOD", terminal_id, start_date)
costing_id = generate_id("COST", terminal_id, product_cat, item_name)
```

### Pattern 2: Lookup Reference Data

```python
# Cache reference lookups (don't query repeatedly)
_product_category_cache = {}

def get_product_category_id(code):
    """Get product category ID with caching"""
    if code not in _product_category_cache:
        cursor.execute("""
            SELECT product_category_id 
            FROM product_categories 
            WHERE product_category_code = ?
        """, (code,))
        _product_category_cache[code] = cursor.fetchone()[0]
    
    return _product_category_cache[code]
```

### Pattern 3: Bulk Insert with Transaction

```python
def bulk_insert_costing(costing_records):
    """Insert multiple costing records efficiently"""
    
    with sqlite3.connect(config.DATABASE_PATH) as conn:
        cursor = conn.cursor()
        
        cursor.executemany("""
            INSERT INTO costing (
                costing_id, terminal_id, product_category_id,
                costing_item_id, costing_value, shipping_period_id,
                start_date, end_date, created_by, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """, costing_records)
        
        # Auto-commits on success
    
    print(f"Inserted {len(costing_records)} costing records")
```

### Pattern 4: Error Handling with Logging

```python
def safe_insert_with_logging(cursor, table_name, record):
    """Insert record with error logging"""
    try:
        # Attempt insert
        cursor.execute(f"INSERT INTO {table_name} (...) VALUES (...)", record)
        return True
    
    except sqlite3.IntegrityError as e:
        # Log FK violation or constraint error
        cursor.execute("""
            INSERT INTO data_quality_log (
                entity_type, entity_id, issue_type, 
                issue_description, created_at
            ) VALUES (?, ?, ?, ?, datetime('now'))
        """, (table_name, record[0], 'integrity_error', str(e)))
        
        return False
```

---

## ✅ Testing Your Code

### Quick Test

```python
# At the bottom of your agent file
if __name__ == "__main__":
    # Test mode
    print("Testing mode...")
    
    # Connect to test database
    conn = sqlite3.connect(':memory:')  # In-memory for testing
    cursor = conn.cursor()
    
    # Create schema
    with open('create_database.py') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    # Test your functions
    agent = MyAgent(api_key="test-key")
    result = agent.execute_task()
    
    print(f"Test result: {result}")
    
    conn.close()
```

### Validate Data Integrity

```python
def validate_costing_integrity(cursor):
    """Check that costing data is internally consistent"""
    
    issues = []
    
    # Check 1: All costing records have valid shipping_period_id
    cursor.execute("""
        SELECT COUNT(*) 
        FROM costing c
        LEFT JOIN shipping_periods sp USING (shipping_period_id)
        WHERE sp.shipping_period_id IS NULL
    """)
    orphaned_costs = cursor.fetchone()[0]
    if orphaned_costs > 0:
        issues.append(f"{orphaned_costs} costing records with invalid shipping_period_id")
    
    # Check 2: All costing dates within shipping period dates
    cursor.execute("""
        SELECT COUNT(*)
        FROM costing c
        JOIN shipping_periods sp USING (shipping_period_id)
        WHERE c.start_date < sp.start_date 
           OR c.end_date > sp.end_date
    """)
    date_mismatches = cursor.fetchone()[0]
    if date_mismatches > 0:
        issues.append(f"{date_mismatches} costing records with dates outside shipping period")
    
    # Check 3: Combined adders match sum of components
    cursor.execute("""
        SELECT 
            sli.shipping_line_item_id,
            sli.line_item_adder AS stated_combined,
            SUM(c.costing_value) AS calculated_combined
        FROM shipping_line_items sli
        JOIN shipping_periods sp USING (shipping_period_id)
        JOIN costing c ON sp.shipping_period_id = c.shipping_period_id
        JOIN products p ON sli.product_id = p.product_id
        WHERE c.product_category_id = p.product_category_id
          AND sli.line_item_type_id = (
              SELECT line_item_type_id 
              FROM line_item_types 
              WHERE line_item_type_name = 'Combined Adder'
          )
        GROUP BY sli.shipping_line_item_id, sli.line_item_adder
        HAVING ABS(sli.line_item_adder - SUM(c.costing_value)) > 0.001
    """)
    adder_mismatches = cursor.fetchall()
    if adder_mismatches:
        issues.append(f"{len(adder_mismatches)} combined adders don't match component sums")
    
    return issues
```

---

## 🛠 Troubleshooting

### Common Issues with New Schema

#### Issue: Foreign Key Constraint Failed

```python
# Error: FOREIGN KEY constraint failed

# Cause: Trying to insert a record with invalid FK
cursor.execute("""
    INSERT INTO costing (
        terminal_id, product_category_id, costing_item_id, ...
    ) VALUES (?, ?, ?, ...)
""", (terminal_id, product_cat_id, costing_item_id, ...))

# Solution: Check that referenced IDs exist
cursor.execute("SELECT 1 FROM terminals WHERE terminal_id = ?", (terminal_id,))
if not cursor.fetchone():
    print(f"Terminal {terminal_id} doesn't exist!")
```

#### Issue: Can't Find Reference Data

```python
# Error: TypeError: 'NoneType' object is not subscriptable

# Cause: Reference lookup returned None
cursor.execute("""
    SELECT product_category_id 
    FROM product_categories 
    WHERE product_category_code = ?
""", ('GASOLINE',))  # Wrong code! Should be 'GAS'
product_cat_id = cursor.fetchone()[0]  # ← Fails here

# Solution: Check spelling and use proper codes
cursor.execute("""
    SELECT product_category_id 
    FROM product_categories 
    WHERE product_category_code = ?
""", ('GAS',))  # ✅ Correct
result = cursor.fetchone()
if result:
    product_cat_id = result[0]
else:
    raise ValueError(f"Unknown product category: GASOLINE")
```

#### Issue: Dates Don't Match

```python
# Problem: Costing dates outside shipping period dates

# Check date alignment
cursor.execute("""
    SELECT 
        c.costing_id,
        c.start_date AS costing_start,
        c.end_date AS costing_end,
        sp.start_date AS period_start,
        sp.end_date AS period_end
    FROM costing c
    JOIN shipping_periods sp USING (shipping_period_id)
    WHERE c.start_date < sp.start_date 
       OR c.end_date > sp.end_date
""")

# Fix: Ensure costing dates align with period dates
period_start = '2024-01-01'
period_end = '2024-12-31'

cursor.execute("""
    INSERT INTO costing (
        ..., start_date, end_date
    ) VALUES (?, ?, ?, ..., ?, ?)
""", (..., period_start, period_end))  # ✅ Use period dates
```

#### Issue: Combined Adder Doesn't Match Sum

```python
# Problem: shipping_line_items.line_item_adder ≠ SUM(costing.costing_value)

# Verify calculation
cursor.execute("""
    SELECT 
        terminal_id,
        product_id,
        SUM(c.costing_value) AS calculated_total
    FROM costing c
    JOIN shipping_periods sp USING (shipping_period_id)
    JOIN products p ON c.product_category_id = p.product_category_id
    WHERE shipping_period_id = ?
      AND p.product_id = ?
    GROUP BY terminal_id, product_id
""", (period_id, product_id))

calculated = cursor.fetchone()[2]

# Compare to shipping_line_items
cursor.execute("""
    SELECT line_item_adder
    FROM shipping_line_items
    WHERE shipping_period_id = ?
      AND product_id = ?
      AND line_item_type_id = (
          SELECT line_item_type_id 
          FROM line_item_types 
          WHERE line_item_type_name = 'Combined Adder'
      )
""", (period_id, product_id))

stored = cursor.fetchone()[0]

if abs(calculated - stored) > 0.001:
    print(f"Mismatch: calculated={calculated}, stored={stored}")
```

---

## 📚 Quick Reference Commands

### Check Schema Version
```bash
# Open database
sqlite3 supply_chain.db

# Count tables
SELECT COUNT(*) FROM sqlite_master WHERE type='table';
# Should return 53

# Check for new tables
SELECT name FROM sqlite_master 
WHERE type='table' 
AND name LIKE 'product%' 
OR name LIKE 'costing%';

.quit
```

### Validate Data Migration

```bash
# Check old data still present
sqlite3 supply_chain.db "SELECT COUNT(*) FROM terminals"
# Should return 227

# Check new structure
sqlite3 supply_chain.db "SELECT COUNT(*) FROM product_categories"
# Should return 3 (GAS, ETH, DSL)

sqlite3 supply_chain.db "SELECT COUNT(*) FROM products"
# Should return 5 (Clear, E10, E15, E85, Diesel)
```

---

## 💡 Best Practices for New Schema

### 1. Always Use Shipping Periods

❌ **DON'T** insert costing data without a shipping period:
```python
cursor.execute("""
    INSERT INTO costing (terminal_id, product_category_id, ...) 
    VALUES (?, ?, ...)
""")
```

✅ **DO** create shipping period first:
```python
# Create period
period_id = create_shipping_period(terminal_id, start_date, end_date)

# Then insert costing linked to period
cursor.execute("""
    INSERT INTO costing (
        terminal_id, product_category_id, shipping_period_id, ...
    ) VALUES (?, ?, ?, ...)
""", (terminal_id, product_cat_id, period_id, ...))
```

### 2. Use Reference Tables

❌ **DON'T** hardcode IDs:
```python
product_category_id = "48ea557d-1b8b-4eb6-9337-dba4b41981d3"  # What is this?
```

✅ **DO** look up by code:
```python
product_category_id = get_product_category_id('GAS')  # Clear!
```

### 3. Validate FK Relationships

❌ **DON'T** assume IDs exist:
```python
cursor.execute("INSERT INTO costing (...) VALUES (...)")
# Might fail with FK constraint error
```

✅ **DO** validate first:
```python
# Check terminal exists
cursor.execute("SELECT 1 FROM terminals WHERE terminal_id = ?", (terminal_id,))
if not cursor.fetchone():
    raise ValueError(f"Terminal {terminal_id} not found")

# Now safe to insert
cursor.execute("INSERT INTO costing (...) VALUES (...)")
```

### 4. Use Transactions

❌ **DON'T** commit after every insert:
```python
for record in records:
    cursor.execute("INSERT ...")
    conn.commit()  # Slow!
```

✅ **DO** batch in transactions:
```python
with sqlite3.connect(config.DATABASE_PATH) as conn:
    cursor = conn.cursor()
    for record in records:
        cursor.execute("INSERT ...")
    # Single commit at end
```

---

## 🔄 Migration Helper Functions

When updating agents from old schema to new:

### Convert Flat Cost to Normalized

```python
def migrate_transportation_cost_to_costing(transport_cost_record):
    """
    Convert old transportation_costs record to new costing records
    
    Args:
        transport_cost_record: Dict with fields from transportation_costs table
    
    Returns:
        List of costing records to insert
    """
    
    # Extract fields
    terminal_id = transport_cost_record['terminal_id']
    product_type = transport_cost_record['product_type']  # 'Clear Gas', 'E10', etc.
    effective_date = transport_cost_record['effective_date']
    end_date = transport_cost_record.get('end_date', '2024-12-31')
    
    # Get product category (GAS or ETH)
    if product_type in ['Clear Gas', 'E10', 'E15', 'E85']:
        product_cat_code = 'GAS'
    else:
        product_cat_code = 'ETH'
    
    product_cat_id = get_product_category_id(product_cat_code)
    
    # Create shipping period
    period_id = create_shipping_period(terminal_id, effective_date, end_date)
    
    # Map old fields to new costing items
    costing_records = []
    
    cost_mappings = {
        'tariff_cost': 'tariff',
        'tvm_cost': 'tvm',
        'basis_cost': 'basis',
        'fuel_surcharge': 'fuel_surcharge',
        'transload_cost': 'transloading',
        'truck_freight': 'truck_freight',
        'line_loss': 'line_loss',
        'margin': 'margin'
    }
    
    for old_field, costing_item_name in cost_mappings.items():
        value = transport_cost_record.get(old_field, 0.0)
        if value != 0.0:
            costing_records.append({
                'costing_id': generate_id("COST", terminal_id, product_cat_id, 
                                         costing_item_name),
                'terminal_id': terminal_id,
                'product_category_id': product_cat_id,
                'costing_item_id': get_costing_item_id(costing_item_name),
                'costing_value': value,
                'shipping_period_id': period_id,
                'start_date': effective_date,
                'end_date': end_date,
                'created_by': 'migration',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
    
    return costing_records
```

---

## 📖 Additional Resources

**Updated Documentation:**
- PROJECT_STATE.md - Current status (updated today!)
- README.md - Overview (needs update for 53 tables)
- BEGINNERS_GUIDE.md - Non-technical guide
- HOW_TO_PRESERVE_AND_ITERATE.md - Long-term maintenance

**To Be Created:**
- ER_DIAGRAM.md - Visual schema reference
- COSTING_METHODOLOGY.md - Detailed workflow
- MULTI_TENANT_GUIDE.md - Alias framework

**External Resources:**
- Anthropic API Docs: https://docs.anthropic.com
- SQLite Tutorial: https://www.sqlitetutorial.net
- Python PDF Processing: https://pdfplumber.readthedocs.io

---

**Last Updated:** February 11, 2026  
**Major Changes:** Complete rewrite for 53-table normalized schema  
**Next Update:** After data migration completed

**Questions?** Upload this file + PROJECT_STATE.md to Claude for help!
