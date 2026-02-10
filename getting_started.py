#!/usr/bin/env python3
"""
Getting Started Example - Supply Chain Mapping Project
Run this script to see the agent-driven system in action
"""

import os
import sys

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def main():
    print_section("🚀 SUPPLY CHAIN MAPPING PROJECT - GETTING STARTED")
    
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("\nOr pass it as an argument:")
        print("  python getting_started.py YOUR_API_KEY")
        
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print(f"\n✓ Using API key from command line")
        else:
            sys.exit(1)
    else:
        print(f"✓ Found ANTHROPIC_API_KEY in environment")
    
    # Step 1: Create database
    print_section("STEP 1: Create Database")
    print("Creating SQLite database with complete schema...")
    
    try:
        from setup_database import create_database, seed_initial_data
        conn = create_database('supply_chain.db')
        seed_initial_data(conn)
        conn.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        sys.exit(1)
    
    # Step 2: Test Terminal Discovery Agent
    print_section("STEP 2: Test Terminal Discovery Agent")
    print("Running terminal discovery to find terminals with IRS TCNs...")
    print("(This will make API calls and may take 30-60 seconds)\n")
    
    try:
        from terminal_discovery_agent import run_discovery
        results = run_discovery(api_key)
        
        print("\n📊 Results:")
        print(f"  Total terminals found: {results.get('total_found', 0)}")
        print(f"  New terminals added: {results.get('new_terminals', 0)}")
        print(f"  Terminals updated: {results.get('updated_terminals', 0)}")
        print(f"  Requiring review: {results.get('terminals_requiring_review', 0)}")
        
    except Exception as e:
        print(f"⚠️  Discovery agent error: {e}")
        print("This is expected if Claude cannot access IRS publications")
        print("In production, the agent would retry or flag for manual intervention")
    
    # Step 3: Demonstrate Orchestrator
    print_section("STEP 3: Demonstrate Orchestrator")
    print("The orchestrator coordinates all agents and manages the task queue...")
    
    try:
        from orchestrator import SupplyChainOrchestrator
        
        orchestrator = SupplyChainOrchestrator(api_key, 'supply_chain.db')
        
        # Create some example tasks
        print("\n➕ Creating example tasks:")
        
        task1 = orchestrator.create_task(
            agent_type='pipeline_tariff',
            description='Check FERC for new Colonial Pipeline tariffs',
            priority=8
        )
        print(f"  ✓ Created: {task1}")
        
        task2 = orchestrator.create_task(
            agent_type='rail_rate',
            description='Update Union Pacific ethanol rates',
            priority=7
        )
        print(f"  ✓ Created: {task2}")
        
        # Show status
        print("\n📊 Current Status:")
        orchestrator.print_status_report()
        
    except Exception as e:
        print(f"❌ Error with orchestrator: {e}")
        sys.exit(1)
    
    # Step 4: Show Database Contents
    print_section("STEP 4: Explore the Database")
    print("Here's how to interact with the database:\n")
    
    print("Using Python:")
    print("""
    import sqlite3
    conn = sqlite3.connect('supply_chain.db')
    cursor = conn.cursor()
    
    # View active terminals
    terminals = cursor.execute("SELECT * FROM v_active_terminals").fetchall()
    print(f"Active terminals: {len(terminals)}")
    
    # View review queue
    reviews = cursor.execute("SELECT * FROM v_review_queue").fetchall()
    print(f"Items needing review: {len(reviews)}")
    """)
    
    print("\nUsing SQLite CLI:")
    print("""
    sqlite3 supply_chain.db
    
    -- View tables
    .tables
    
    -- View active terminals
    SELECT * FROM v_active_terminals;
    
    -- View task status
    SELECT agent_type, status, COUNT(*) 
    FROM agent_tasks 
    GROUP BY agent_type, status;
    
    -- Exit
    .quit
    """)
    
    # Step 5: Next Steps
    print_section("STEP 5: Next Steps")
    
    print("""
Ready to build your supply chain mapping system! Here's what to do next:

1. 📖 Read the Documentation
   - agent_driven_framework.md - Complete technical guide
   - README.md - Quick reference and usage guide

2. 🔧 Implement Additional Agents
   - Pipeline Tariff Agent - Collect FERC tariffs
   - Rail Rate Agent - Track railroad rates  
   - Terminal Information Agent - Gather operational details
   (See agent_driven_framework.md for templates)

3. ⏰ Set Up Scheduling
   - Use cron or systemd for automated runs
   - Start with weekly runs, move to daily as confidence grows
   (See README.md for setup instructions)

4. 📊 Monitor Performance
   - Track automation rate (target: 80-90%)
   - Monitor data quality scores
   - Review exception queue weekly
   
5. 🔄 Iterate and Improve
   - Refine agent prompts based on results
   - Adjust human review thresholds
   - Add new data sources as needed

📚 Key Files Created:
   - setup_database.py - Database initialization
   - terminal_discovery_agent.py - First working agent
   - orchestrator.py - Task coordination system
   - agent_driven_framework.md - Complete documentation
   - README.md - Quick reference guide

🎯 Success Metrics to Track:
   - Automation rate: % tasks without human intervention
   - Data quality score: Completeness + accuracy  
   - Human review time: Target <15 hours/week
   - Coverage: % of IRS terminals mapped

💰 Expected Costs:
   - Claude API: ~$4-6K/year
   - Human resources: 0.25-0.5 FTE (vs 1.5-2 FTE manual)
   - Total efficiency gain: 70-85% reduction

🚦 Getting Help:
   - Review agent_driven_framework.md for detailed architecture
   - Check README.md troubleshooting section
   - Examine orchestrator.py for workflow examples

Happy mapping! 🗺️
""")

if __name__ == "__main__":
    main()
