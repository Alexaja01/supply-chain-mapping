#!/usr/bin/env python3
"""
Complete Database Setup - Creates all tables and views
Run this once to set up your database properly
"""

import sqlite3
from datetime import datetime

def create_complete_database(db_path='supply_chain.db'):
    """Create database with all tables and views"""
    
    print("Creating complete database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Terminals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminals (
        terminal_id TEXT PRIMARY KEY,
        terminal_name TEXT NOT NULL,
        irs_tcn TEXT UNIQUE,
        state TEXT,
        city TEXT,
        county TEXT,
        latitude REAL,
        longitude REAL,
        operator TEXT,
        owner TEXT,
        capacity_bpd INTEGER,
        products_handled TEXT,
        receiving_methods TEXT,
        effective_date DATE,
        end_date DATE,
        data_quality_score REAL DEFAULT 0.0,
        last_verified TIMESTAMP,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Pipelines
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipelines (
        pipeline_id TEXT PRIMARY KEY,
        pipeline_name TEXT NOT NULL,
        operator TEXT,
        owner TEXT,
        pipeline_type TEXT,
        product_types TEXT,
        origin_point TEXT,
        destination_point TEXT,
        length_miles REAL,
        flow_speed_mph REAL,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Agent Tasks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_tasks (
        task_id TEXT PRIMARY KEY,
        agent_type TEXT NOT NULL,
        task_description TEXT,
        task_parameters TEXT,
        priority INTEGER DEFAULT 5,
        status TEXT DEFAULT 'Pending',
        assigned_timestamp TIMESTAMP,
        started_timestamp TIMESTAMP,
        completed_timestamp TIMESTAMP,
        result_summary TEXT,
        result_data TEXT,
        requires_human_review BOOLEAN DEFAULT 0,
        human_reviewed BOOLEAN DEFAULT 0,
        human_review_notes TEXT,
        error_message TEXT,
        retry_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Pipeline Tariffs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_tariffs (
        tariff_id TEXT PRIMARY KEY,
        pipeline_id TEXT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        product_type TEXT,
        rate_per_gallon REAL,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_terminals_state ON terminals(state)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON agent_tasks(status)")
    
    # Create views
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_terminals AS
    SELECT * FROM terminals
    WHERE (end_date IS NULL OR end_date > date('now'))
    AND (effective_date IS NULL OR effective_date <= date('now'))
    """)
    
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_pipeline_tariffs AS
    SELECT * FROM pipeline_tariffs
    WHERE (end_date IS NULL OR end_date > date('now'))
    AND (effective_date IS NULL OR effective_date <= date('now'))
    """)
    
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_review_queue AS
    SELECT 
        task_id,
        agent_type,
        task_description,
        completed_timestamp,
        result_summary
    FROM agent_tasks
    WHERE requires_human_review = 1 
    AND human_reviewed = 0
    AND status = 'Completed'
    ORDER BY priority DESC, completed_timestamp ASC
    """)
    
    conn.commit()
    
    print(f"✅ Complete database created: {db_path}")
    print(f"   Tables: terminals, pipelines, agent_tasks, pipeline_tariffs")
    print(f"   Views: v_active_terminals, v_active_pipeline_tariffs, v_review_queue")
    
    return conn

if __name__ == "__main__":
    print("\n" + "="*80)
    print("  CREATING COMPLETE SUPPLY CHAIN DATABASE")
    print("="*80 + "\n")
    
    conn = create_complete_database('supply_chain.db')
    conn.close()
    
    print("\n✅ Database setup complete!")
    print("\nYou can now run:")
    print("  python orchestrator.py --api-key YOUR_KEY status")
    print("\n" + "="*80 + "\n")
