#!/usr/bin/env python3
"""
Complete Database Setup - Creates ALL 15 tables and 3 views
Run this once to set up your database properly
"""

import sqlite3
from datetime import datetime

def create_complete_database(db_path='supply_chain.db'):
    """Create database with ALL tables and views"""
    
    print("\nCreating complete database...")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # ========================================================================
    # ASSET TABLES (5)
    # ========================================================================
    
    print("\nCreating asset tables...")
    
    # 1. Terminals
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
    print("  ✓ Created table: terminals")
    
    # 2. Pipelines
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
    print("  ✓ Created table: pipelines")
    
    # 3. Rail Connections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rail_connections (
        connection_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        railroad_name TEXT NOT NULL,
        siding_name TEXT,
        car_capacity INTEGER,
        loading_unloading TEXT,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id)
    )
    """)
    print("  ✓ Created table: rail_connections")
    
    # 4. Marine Facilities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marine_facilities (
        facility_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        facility_name TEXT NOT NULL,
        dock_type TEXT,
        vessel_capacity TEXT,
        loading_unloading TEXT,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id)
    )
    """)
    print("  ✓ Created table: marine_facilities")
    
    # 5. Refineries
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS refineries (
        refinery_id TEXT PRIMARY KEY,
        refinery_name TEXT NOT NULL,
        operator TEXT,
        owner TEXT,
        state TEXT,
        city TEXT,
        latitude REAL,
        longitude REAL,
        capacity_bpd INTEGER,
        products_produced TEXT,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ Created table: refineries")
    
    # ========================================================================
    # LINKAGE TABLES (2)
    # ========================================================================
    
    print("\nCreating linkage tables...")
    
    # 6. Terminal-Pipeline Links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_pipeline_links (
        link_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        pipeline_id TEXT,
        connection_type TEXT,
        direction TEXT,
        capacity_bpd INTEGER,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(pipeline_id)
    )
    """)
    print("  ✓ Created table: terminal_pipeline_links")
    
    # 7. Pipeline-Refinery Links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_refinery_links (
        link_id TEXT PRIMARY KEY,
        pipeline_id TEXT,
        refinery_id TEXT,
        connection_type TEXT,
        direction TEXT,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(pipeline_id),
        FOREIGN KEY (refinery_id) REFERENCES refineries(refinery_id)
    )
    """)
    print("  ✓ Created table: pipeline_refinery_links")
    
    # ========================================================================
    # COSTING TABLES (3)
    # ========================================================================
    
    print("\nCreating costing tables...")
    
    # 8. Pipeline Tariffs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_tariffs (
        tariff_id TEXT PRIMARY KEY,
        pipeline_id TEXT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        origin_county TEXT,
        destination_county TEXT,
        product_type TEXT,
        rate_per_gallon REAL,
        rate_basis TEXT,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        ferc_tariff_number TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(pipeline_id)
    )
    """)
    print("  ✓ Created table: pipeline_tariffs")
    
    # 9. Terminal Rates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_rates (
        rate_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        product_type TEXT,
        throughput_rate REAL,
        facilities_charge REAL,
        storage_rate REAL,
        rate_basis TEXT,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id)
    )
    """)
    print("  ✓ Created table: terminal_rates")
    
    # 10. Rail Rates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rail_rates (
        rate_id TEXT PRIMARY KEY,
        railroad_name TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        product_type TEXT,
        rate_per_gallon REAL,
        rate_basis TEXT,
        mileage INTEGER,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ Created table: rail_rates")
    
    # ========================================================================
    # MANAGEMENT TABLES (5)
    # ========================================================================
    
    print("\nCreating management tables...")
    
    # 11. Agent Tasks
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
    print("  ✓ Created table: agent_tasks")
    
    # 12. Data Quality Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_quality_log (
        log_id TEXT PRIMARY KEY,
        table_name TEXT NOT NULL,
        record_id TEXT,
        quality_check_type TEXT,
        quality_score REAL,
        issues_found TEXT,
        checked_by TEXT,
        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ Created table: data_quality_log")
    
    # 13. Agent Metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_metrics (
        metric_id TEXT PRIMARY KEY,
        agent_type TEXT NOT NULL,
        tasks_completed INTEGER DEFAULT 0,
        tasks_failed INTEGER DEFAULT 0,
        avg_execution_time REAL,
        human_review_rate REAL,
        data_quality_avg REAL,
        period_start DATE,
        period_end DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ Created table: agent_metrics")
    
    # 14. Ownership Changes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ownership_changes (
        change_id TEXT PRIMARY KEY,
        asset_type TEXT NOT NULL,
        asset_id TEXT NOT NULL,
        previous_owner TEXT,
        new_owner TEXT,
        transaction_date DATE,
        transaction_value REAL,
        source_document TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ Created table: ownership_changes")
    
    # 15. Source Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS source_documents (
        document_id TEXT PRIMARY KEY,
        document_type TEXT NOT NULL,
        document_name TEXT,
        document_url TEXT,
        local_path TEXT,
        effective_date DATE,
        retrieved_date DATE,
        hash_checksum TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ Created table: source_documents")
    
    # ========================================================================
    # INDEXES
    # ========================================================================
    
    print("\nCreating indexes...")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_terminals_state ON terminals(state)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_terminals_tcn ON terminals(irs_tcn)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON agent_tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_agent_type ON agent_tasks(agent_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tariffs_pipeline ON pipeline_tariffs(pipeline_id)")
    print("  ✓ Created indexes")
    
    # ========================================================================
    # VIEWS
    # ========================================================================
    
    print("\nCreating views...")
    
    # View 1: Active Terminals
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_terminals AS
    SELECT * FROM terminals
    WHERE (end_date IS NULL OR end_date > date('now'))
    AND (effective_date IS NULL OR effective_date <= date('now'))
    """)
    print("  ✓ Created view: v_active_terminals")
    
    # View 2: Active Pipeline Tariffs
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_pipeline_tariffs AS
    SELECT * FROM pipeline_tariffs
    WHERE (end_date IS NULL OR end_date > date('now'))
    AND (effective_date IS NULL OR effective_date <= date('now'))
    """)
    print("  ✓ Created view: v_active_pipeline_tariffs")
    
    # View 3: Review Queue
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
    print("  ✓ Created view: v_review_queue")
    
    conn.commit()
    
    print("\n" + "=" * 60)
    print("✅ Complete database created successfully!")
    print("\nDatabase: supply_chain.db")
    print("\nTables created (15):")
    print("  Asset Tables: terminals, pipelines, rail_connections,")
    print("                marine_facilities, refineries")
    print("  Linkage: terminal_pipeline_links, pipeline_refinery_links")
    print("  Costing: pipeline_tariffs, terminal_rates, rail_rates")
    print("  Management: agent_tasks, data_quality_log, agent_metrics,")
    print("              ownership_changes, source_documents")
    print("\nViews created (3):")
    print("  v_active_terminals, v_active_pipeline_tariffs, v_review_queue")
    print("=" * 60)
    
    return conn

if __name__ == "__main__":
    print("\n" + "="*80)
    print("  CREATING COMPLETE SUPPLY CHAIN DATABASE")
    print("  All 15 Tables + 3 Views")
    print("="*80)
    
    conn = create_complete_database('supply_chain.db')
    conn.close()
    
    print("\n✅ Database setup complete!")
    print("\nNext steps:")
    print("  1. Run daily update: python orchestrator.py --api-key YOUR_KEY daily")
    print("  2. Check status: python orchestrator.py --api-key YOUR_KEY status")
    print("  3. Import data or run terminal discovery agent")
    print("\n" + "="*80 + "\n")
