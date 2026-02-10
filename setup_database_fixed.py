#!/usr/bin/env python3
"""
Database Setup Script for Supply Chain Mapping Project
Creates all necessary tables for agent-driven data collection
"""

import sqlite3
from datetime import datetime

def create_database(db_path='supply_chain.db'):
    """Create database and all tables"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
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
    
    # Rail Connections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rail_connections (
        rail_connection_id TEXT PRIMARY KEY,
        railroad_name TEXT NOT NULL,
        terminal_id TEXT REFERENCES terminals(terminal_id),
        siding_location TEXT,
        latitude REAL,
        longitude REAL,
        capacity_cars INTEGER,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Marine Facilities
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marine_facilities (
        dock_id TEXT PRIMARY KEY,
        facility_name TEXT NOT NULL,
        terminal_id TEXT REFERENCES terminals(terminal_id),
        waterway TEXT,
        vessel_types TEXT,
        draft_depth_feet REAL,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Refineries
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
        product_slate TEXT,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Terminal-Pipeline Links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_pipeline_links (
        link_id TEXT PRIMARY KEY,
        terminal_id TEXT REFERENCES terminals(terminal_id),
        pipeline_id TEXT REFERENCES pipelines(pipeline_id),
        connection_type TEXT,
        product_types TEXT,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Pipeline-Refinery Links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_refinery_links (
        link_id TEXT PRIMARY KEY,
        pipeline_id TEXT REFERENCES pipelines(pipeline_id),
        refinery_id TEXT REFERENCES refineries(refinery_id),
        connection_point TEXT,
        connection_type TEXT,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Pipeline Tariffs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_tariffs (
        tariff_id TEXT PRIMARY KEY,
        pipeline_id TEXT REFERENCES pipelines(pipeline_id),
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        origin_county TEXT,
        destination_county TEXT,
        product_type TEXT,
        rate_per_gallon REAL,
        rate_basis TEXT,
        rate_original REAL,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        ferc_tariff_number TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Terminal Rates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_rates (
        rate_id TEXT PRIMARY KEY,
        terminal_id TEXT REFERENCES terminals(terminal_id),
        rate_type TEXT,
        product_type TEXT,
        rate_per_gallon REAL,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Rail Rates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rail_rates (
        rate_id TEXT PRIMARY KEY,
        railroad_name TEXT NOT NULL,
        origin TEXT,
        destination TEXT,
        product_type TEXT,
        rate_per_gallon REAL,
        distance_miles REAL,
        fuel_surcharge REAL,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        stb_filing_number TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Ownership Changes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ownership_changes (
        change_id TEXT PRIMARY KEY,
        asset_type TEXT NOT NULL,
        asset_id TEXT NOT NULL,
        previous_owner TEXT,
        new_owner TEXT,
        transaction_date DATE,
        transaction_type TEXT,
        transaction_value REAL,
        source_document TEXT,
        notes TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Agent Task Queue
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
    
    # Data Quality Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_quality_log (
        log_id TEXT PRIMARY KEY,
        record_type TEXT NOT NULL,
        record_id TEXT NOT NULL,
        quality_check TEXT,
        check_result TEXT,
        check_details TEXT,
        check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        agent_name TEXT
    )
    """)
    
    # Agent Performance Metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_metrics (
        metric_id TEXT PRIMARY KEY,
        agent_type TEXT NOT NULL,
        metric_date DATE,
        tasks_completed INTEGER,
        tasks_failed INTEGER,
        avg_execution_time_seconds REAL,
        human_review_rate REAL,
        data_quality_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Source Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS source_documents (
        document_id TEXT PRIMARY KEY,
        document_type TEXT,
        document_name TEXT,
        source_url TEXT,
        local_path TEXT,
        publication_date DATE,
        effective_date DATE,
        downloaded_timestamp TIMESTAMP,
        checksum TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_terminals_state ON terminals(state)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_terminals_city ON terminals(state, city)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_terminals_tcn ON terminals(irs_tcn)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON agent_tasks(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON agent_tasks(priority, status)")
    
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
    print(f"✅ Database created successfully at: {db_path}")
    
    return conn

def seed_initial_data(conn):
    """Add some initial reference data"""
    print("\n📋 Initial setup complete!")
    print("🚀 Ready to start agent-driven data collection!")

if __name__ == "__main__":
    conn = create_database()
    seed_initial_data(conn)
    conn.close()
