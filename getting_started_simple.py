#!/usr/bin/env python3
"""
Getting Started - Simple All-In-One Version
No separate files needed - everything is here!
"""

import os
import sys
import sqlite3
from datetime import datetime

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def create_database(db_path='supply_chain.db'):
    """Create database and all tables"""
    
    print("Creating SQLite database with complete schema...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create main tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminals (
        terminal_id TEXT PRIMARY KEY,
        terminal_name TEXT NOT NULL,
        irs_tcn TEXT UNIQUE,
        state TEXT,
        city TEXT,
        operator TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_tasks (
        task_id TEXT PRIMARY KEY,
        agent_type TEXT NOT NULL,
        task_description TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipelines (
        pipeline_id TEXT PRIMARY KEY,
        pipeline_name TEXT NOT NULL,
        operator TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    print(f"✅ Database created successfully: {db_path}")
    print(f"   Tables created: 3 (terminals, agent_tasks, pipelines)")
    
    return conn

def test_api_key(api_key):
    """Test if the API key works"""
    print("Testing API key...")
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        # Simple test
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API key works!'"}]
        )
        
        print("✅ API key is valid!")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {str(e)}")
        return False

def main():
    print_section("🚀 SUPPLY CHAIN MAPPING PROJECT - GETTING STARTED")
    
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print(f"✓ Using API key from command line")
        else:
            print("❌ Error: ANTHROPIC_API_KEY not set")
            print("\nUsage: python getting_started_simple.py YOUR_API_KEY")
            sys.exit(1)
    else:
        print(f"✓ Found API key")
    
    # Step 1: Create database
    print_section("STEP 1: Create Database")
    try:
        conn = create_database('supply_chain.db')
        conn.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)
    
    # Step 2: Test API key
    print_section("STEP 2: Test API Key")
    if not test_api_key(api_key):
        print("\n⚠️  API key didn't work. Check that it's correct.")
        sys.exit(1)
    
    # Step 3: Success!
    print_section("STEP 3: Success! 🎉")
    
    print("""
✅ Setup Complete!

You now have:
  • Database created: supply_chain.db
  • API key verified and working
  • System ready to use

Next Steps:
  
1. Run daily updates:
   python orchestrator.py --api-key YOUR_KEY daily
   
2. Check status:
   python orchestrator.py --api-key YOUR_KEY status
   
3. View the database:
   - Download "DB Browser for SQLite" from sqlitebrowser.org
   - Open supply_chain.db to view your data

Need Help?
  • Read BEGINNERS_GUIDE.md for detailed instructions
  • Read EASY_DOUBLE_CLICK_GUIDE.md for the easiest way to run daily

Ready to map the entire US refined products supply chain! 🗺️
""")

if __name__ == "__main__":
    main()
