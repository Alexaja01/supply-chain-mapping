C:\users\jalex\appdata\roaming\claude\local agent mode sessions\858510ab c23b 42a8 a42f 002840c47728\3d9c0f35 6441 47e2 a04e 6d92621bfc51\local 693dc6cf 7c3c 4cf1 a13c d6b38f96f328\outputs\create database · PY
#!/usr/bin/env python3
"""
Complete Database Setup - Supply Chain Mapping System
=====================================================
Creates ALL tables, views, indexes, and seed data.

Schema based on gap analysis comparing original EN PostgreSQL system
against simplified SQLite implementation. Includes:

  MASTER DATA (8 tables)
  - product_categories, products, terminals, pipelines, refineries,
    rail_connections, marine_facilities, terminal_products

  CONFIGURATION (4 tables)
  - line_item_types, costing_items, shipping_setup, price_days

  LINKAGE (5 tables)
  - terminal_pipeline_links, pipeline_refinery_links,
    shipping_paths, terminal_path_links, tariff_path_links

  COSTING (7 tables)
  - pipeline_tariffs, tariff_libraries, tariff_costs,
    terminal_rates, transportation_costs, rail_rates, costing

  SHIPPING (2 tables)
  - shipping_periods, shipping_line_items

  SPOT MARKET (3 tables)
  - spot_markets, index_components, spot_indices

  BUYING COST SHEETS (5 tables)
  - bcs_types, bcs_period_statuses, bcs, bcs_periods, bcs_line_items

  ALIAS / MULTI-TENANT (7 tables)
  - alias_types, terminal_aliases, product_aliases,
    line_item_type_aliases, index_aliases, price_day_aliases

  MANAGEMENT (5 tables)
  - agent_tasks, data_quality_log, agent_metrics,
    ownership_changes, source_documents

  ALIAS ERROR TRACKING (5 tables)
  - terminal_alias_errors, product_alias_errors,
    line_item_type_alias_errors, index_alias_errors,
    price_day_alias_errors

  ETL TRACKING (2 tables)
  - batches, shipping_tracking

Total: ~52 tables, 5+ views, seed data
"""

import sqlite3
from datetime import datetime
import uuid


def generate_id():
    """Generate a UUID for primary keys"""
    return str(uuid.uuid4())


def create_complete_database(db_path='supply_chain.db'):
    """Create database with ALL tables, views, indexes, and seed data"""

    print("\n" + "=" * 80)
    print("  CREATING COMPLETE SUPPLY CHAIN DATABASE")
    print("  Full Schema with Multi-Tenant Support")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA journal_mode = WAL")

    # ========================================================================
    # MASTER DATA TABLES
    # ========================================================================

    print("\n--- MASTER DATA TABLES ---")

    # 1. Product Categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_categories (
        category_id TEXT PRIMARY KEY,
        category_code TEXT NOT NULL UNIQUE,
        category_name TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ product_categories")

    # 2. Products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_code TEXT NOT NULL UNIQUE,
        product_name TEXT NOT NULL,
        product_category_id TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_category_id) REFERENCES product_categories(category_id)
    )
    """)
    print("  ✓ products")

    # 3. Terminals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminals (
        terminal_id TEXT PRIMARY KEY,
        terminal_name TEXT NOT NULL,
        terminal_code TEXT,
        irs_tcn TEXT UNIQUE,
        tcn4 TEXT,
        state TEXT,
        city TEXT,
        county TEXT,
        market TEXT,
        terminal_market_id TEXT,
        region TEXT,
        latitude REAL,
        longitude REAL,
        operator TEXT,
        owner TEXT,
        capacity_bpd INTEGER,
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
    print("  ✓ terminals")

    # 4. Terminal Products (bridge: which terminals handle which products)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_products (
        terminal_product_id TEXT PRIMARY KEY,
        terminal_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        shipping_status INTEGER DEFAULT 0,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        UNIQUE (terminal_id, product_id)
    )
    """)
    print("  ✓ terminal_products")

    # 5. Pipelines
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipelines (
        pipeline_id TEXT PRIMARY KEY,
        pipeline_name TEXT NOT NULL,
        operator TEXT,
        owner TEXT,
        pipeline_type TEXT,
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
    print("  ✓ pipelines")

    # 6. Refineries
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
    print("  ✓ refineries")

    # 7. Rail Connections
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
    print("  ✓ rail_connections")

    # 8. Marine Facilities
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
    print("  ✓ marine_facilities")

    # ========================================================================
    # CONFIGURATION TABLES
    # ========================================================================

    print("\n--- CONFIGURATION TABLES ---")

    # 9. Line Item Types (RIN, CARB 1, CARB 2, Line Space, Ethanol, Combined Adder, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS line_item_types (
        line_item_type_id TEXT PRIMARY KEY,
        line_item_type_name TEXT NOT NULL UNIQUE,
        display_order INTEGER,
        shipping_status INTEGER DEFAULT 1,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ line_item_types")

    # 10. Costing Items (tariff, facilities_charge, throughput, TVM, basis, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS costing_items (
        costing_item_id TEXT PRIMARY KEY,
        costing_item_name TEXT NOT NULL UNIQUE,
        costing_item_description TEXT,
        shipping_status INTEGER DEFAULT 1,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ costing_items")

    # 11. Price Days (Prior Day, Spot, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_days (
        price_day_id TEXT PRIMARY KEY,
        price_day_name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ price_days")

    # 12. Shipping Setup (configures which terminal_product combos support which line_item_types)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipping_setup (
        shipping_setup_id TEXT PRIMARY KEY,
        terminal_product_id TEXT NOT NULL,
        line_item_type_id TEXT NOT NULL,
        base_product_id TEXT,
        line_item_percent REAL DEFAULT 1.0,
        index_id TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_product_id) REFERENCES terminal_products(terminal_product_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id),
        FOREIGN KEY (base_product_id) REFERENCES products(product_id)
    )
    """)
    print("  ✓ shipping_setup")

    # ========================================================================
    # LINKAGE TABLES
    # ========================================================================

    print("\n--- LINKAGE TABLES ---")

    # 13. Terminal-Pipeline Links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_pipeline_links (
        link_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        pipeline_id TEXT,
        connection_type TEXT,
        direction TEXT,
        capacity_bpd INTEGER,
        is_published BOOLEAN DEFAULT 0,
        is_included BOOLEAN DEFAULT 1,
        effective_date DATE,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(pipeline_id)
    )
    """)
    print("  ✓ terminal_pipeline_links")

    # 14. Pipeline-Refinery Links
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
    print("  ✓ pipeline_refinery_links")

    # 15. Shipping Paths (multi-leg transportation routes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipping_paths (
        shipping_path_id TEXT PRIMARY KEY,
        shipping_path_name TEXT,
        shipping_path_origin_id TEXT,
        shipping_path_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ shipping_paths")

    # 16. Terminal-Path Links (terminal + product_category -> shipping_path)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_path_links (
        terminal_path_link_id TEXT PRIMARY KEY,
        terminal_id TEXT NOT NULL,
        product_category_id TEXT NOT NULL,
        shipping_path_id TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (product_category_id) REFERENCES product_categories(category_id),
        FOREIGN KEY (shipping_path_id) REFERENCES shipping_paths(shipping_path_id),
        UNIQUE (terminal_id, product_category_id, shipping_path_id)
    )
    """)
    print("  ✓ terminal_path_links")

    # 17. Tariff-Path Links (shipping_path -> tariff)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tariff_path_links (
        tariff_path_link_id TEXT PRIMARY KEY,
        shipping_path_id TEXT NOT NULL,
        tariff_id TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (shipping_path_id) REFERENCES shipping_paths(shipping_path_id),
        FOREIGN KEY (tariff_id) REFERENCES pipeline_tariffs(tariff_id)
    )
    """)
    print("  ✓ tariff_path_links")

    # ========================================================================
    # COSTING TABLES
    # ========================================================================

    print("\n--- COSTING TABLES ---")

    # 18. Tariff Libraries (versioned tariff document collections)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tariff_libraries (
        tariff_library_id TEXT PRIMARY KEY,
        tariff_library_code TEXT NOT NULL,
        tariff_library_name TEXT,
        tariff_start_date DATE,
        tariff_end_date DATE,
        source_document TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ tariff_libraries")

    # 19. Pipeline Tariffs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_tariffs (
        tariff_id TEXT PRIMARY KEY,
        pipeline_id TEXT,
        pipeline_name TEXT,
        tariff_code TEXT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        origin_county TEXT,
        destination_county TEXT,
        product_type TEXT,
        rate_per_gallon REAL,
        rate_basis TEXT,
        miles INTEGER,
        tariff_library_name TEXT,
        tariff_library_id TEXT,
        shipping_period_id TEXT,
        line_item_type_id TEXT,
        spot_index_id TEXT,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        ferc_tariff_number TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pipeline_id) REFERENCES pipelines(pipeline_id),
        FOREIGN KEY (tariff_library_id) REFERENCES tariff_libraries(tariff_library_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id)
    )
    """)
    print("  ✓ pipeline_tariffs")

    # 20. Tariff Costs (per-tariff-library cost values - enables versioning)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tariff_costs (
        tariff_cost_id TEXT PRIMARY KEY,
        tariff_id TEXT NOT NULL,
        tariff_library_id TEXT NOT NULL,
        tariff_value REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (tariff_id) REFERENCES pipeline_tariffs(tariff_id),
        FOREIGN KEY (tariff_library_id) REFERENCES tariff_libraries(tariff_library_id)
    )
    """)
    print("  ✓ tariff_costs")

    # 21. Terminal Rates
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_rates (
        rate_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        product_type TEXT,
        facilities_charge REAL,
        throughput_rate REAL,
        terminaling_estimate REAL,
        additive REAL,
        rate_basis TEXT,
        shipping_period_id TEXT,
        line_item_type_id TEXT,
        spot_index_id TEXT,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id)
    )
    """)
    print("  ✓ terminal_rates")

    # 22. Transportation Costs (aggregated - kept for backward compatibility)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transportation_costs (
        transport_cost_id TEXT PRIMARY KEY,
        terminal_id TEXT,
        product_type TEXT,
        tariff_cost REAL,
        tvm_cost REAL,
        basis_cost REAL,
        fuel_surcharge REAL,
        transload_cost REAL,
        truck_freight REAL,
        line_loss REAL,
        margin REAL,
        transportation_estimate REAL,
        combined_adder REAL,
        shipping_period_id TEXT,
        line_item_type_id TEXT,
        spot_index_id TEXT,
        effective_date DATE,
        end_date DATE,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id)
    )
    """)
    print("  ✓ transportation_costs")

    # 23. Rail Rates
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
        shipping_period_id TEXT,
        line_item_type_id TEXT,
        rail_connection_id TEXT,
        effective_date DATE,
        end_date DATE,
        source_document TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rail_connection_id) REFERENCES rail_connections(connection_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id)
    )
    """)
    print("  ✓ rail_rates")

    # 24. Costing (time-bound costing records: terminal + product_category + costing_item)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS costing (
        costing_id TEXT PRIMARY KEY,
        terminal_id TEXT NOT NULL,
        product_category_id TEXT NOT NULL,
        costing_item_id TEXT NOT NULL,
        costing_value REAL,
        start_date DATE NOT NULL,
        end_date DATE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        FOREIGN KEY (product_category_id) REFERENCES product_categories(category_id),
        FOREIGN KEY (costing_item_id) REFERENCES costing_items(costing_item_id)
    )
    """)
    print("  ✓ costing")

    # ========================================================================
    # SHIPPING TABLES
    # ========================================================================

    print("\n--- SHIPPING TABLES ---")

    # 25. Shipping Periods (time-bound pricing periods per terminal)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipping_periods (
        shipping_period_id TEXT PRIMARY KEY,
        terminal_id TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        period_status TEXT DEFAULT 'Active',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id)
    )
    """)
    print("  ✓ shipping_periods")

    # 26. Shipping Line Items (per-period cost decomposition by product + line item type)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipping_line_items (
        shipping_line_item_id TEXT PRIMARY KEY,
        shipping_period_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        line_item_type_id TEXT NOT NULL,
        base_product_id TEXT,
        line_item_adder REAL,
        line_item_percent REAL DEFAULT 1.0,
        spot_index_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (shipping_period_id) REFERENCES shipping_periods(shipping_period_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id),
        FOREIGN KEY (base_product_id) REFERENCES products(product_id)
    )
    """)
    print("  ✓ shipping_line_items")

    # ========================================================================
    # SPOT MARKET / INDEX TABLES
    # ========================================================================

    print("\n--- SPOT MARKET / INDEX TABLES ---")

    # 27. Spot Markets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spot_markets (
        spot_market_id TEXT PRIMARY KEY,
        spot_market_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ spot_markets")

    # 28. Spot Market Location Links
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spot_market_location_links (
        link_id TEXT PRIMARY KEY,
        transportation_location_link_id TEXT,
        spot_market_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (spot_market_id) REFERENCES spot_markets(spot_market_id)
    )
    """)
    print("  ✓ spot_market_location_links")

    # 29. Index Components
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS index_components (
        index_component_id TEXT PRIMARY KEY,
        index_component_code TEXT NOT NULL UNIQUE,
        index_component_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ index_components")

    # 30. Spot Indices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spot_indices (
        spot_index_id TEXT PRIMARY KEY,
        spot_index_code TEXT NOT NULL,
        spot_market_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        index_component_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (spot_market_id) REFERENCES spot_markets(spot_market_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (index_component_id) REFERENCES index_components(index_component_id)
    )
    """)
    print("  ✓ spot_indices")

    # ========================================================================
    # BUYING COST SHEET (BCS) TABLES
    # ========================================================================

    print("\n--- BUYING COST SHEET (BCS) TABLES ---")

    # 31. BCS Types
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bcs_types (
        bcs_type_id TEXT PRIMARY KEY,
        bcs_type_name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ bcs_types")

    # 32. BCS Period Statuses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bcs_period_statuses (
        bcs_period_status_id TEXT PRIMARY KEY,
        bcs_period_status_name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ bcs_period_statuses")

    # 33. BCS (master buying cost sheets)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bcs (
        bcs_id TEXT PRIMARY KEY,
        bcs_code TEXT NOT NULL UNIQUE,
        bcs_name TEXT NOT NULL,
        bcs_type_id TEXT NOT NULL,
        primary_terminal_alias TEXT,
        terminal_alias_type_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (bcs_type_id) REFERENCES bcs_types(bcs_type_id)
    )
    """)
    print("  ✓ bcs")

    # 34. BCS Periods (time-bound BCS instances)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bcs_periods (
        bcs_period_id TEXT PRIMARY KEY,
        bcs_id TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        bcs_period_status_id TEXT NOT NULL,
        bcs_period_status_override INTEGER DEFAULT 0,
        cwg_status_id TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (bcs_id) REFERENCES bcs(bcs_id),
        FOREIGN KEY (bcs_period_status_id) REFERENCES bcs_period_statuses(bcs_period_status_id)
    )
    """)
    print("  ✓ bcs_periods")

    # 35. BCS Line Items (detailed line items with alias references)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bcs_line_items (
        bcs_line_item_id TEXT PRIMARY KEY,
        bcs_period_id TEXT NOT NULL,
        product_alias TEXT,
        product_alias_type_code TEXT,
        line_item_type_alias TEXT,
        lit_alias_type_code TEXT,
        index_alias TEXT,
        index_alias_type_code TEXT,
        price_day_alias TEXT,
        price_day_alias_type_code TEXT,
        line_item_adder REAL,
        line_item_percent REAL DEFAULT 1.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (bcs_period_id) REFERENCES bcs_periods(bcs_period_id)
    )
    """)
    print("  ✓ bcs_line_items")

    # ========================================================================
    # ALIAS / MULTI-TENANT TABLES
    # ========================================================================

    print("\n--- ALIAS / MULTI-TENANT TABLES ---")

    # 36. Alias Types
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alias_types (
        alias_type_id TEXT PRIMARY KEY,
        alias_type_code TEXT NOT NULL UNIQUE,
        alias_type_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ alias_types")

    # 37. Terminal Aliases
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminal_aliases (
        terminal_alias_id TEXT PRIMARY KEY,
        terminal_alias_code TEXT NOT NULL,
        alias_type_id TEXT NOT NULL,
        terminal_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alias_type_id) REFERENCES alias_types(alias_type_id),
        FOREIGN KEY (terminal_id) REFERENCES terminals(terminal_id),
        UNIQUE (terminal_alias_code, alias_type_id)
    )
    """)
    print("  ✓ terminal_aliases")

    # 38. Product Aliases
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_aliases (
        product_alias_id TEXT PRIMARY KEY,
        product_alias_code TEXT NOT NULL,
        alias_type_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alias_type_id) REFERENCES alias_types(alias_type_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        UNIQUE (product_alias_code, alias_type_id)
    )
    """)
    print("  ✓ product_aliases")

    # 39. Line Item Type Aliases
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS line_item_type_aliases (
        lit_alias_id TEXT PRIMARY KEY,
        alias_code TEXT NOT NULL,
        alias_type_id TEXT NOT NULL,
        line_item_type_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alias_type_id) REFERENCES alias_types(alias_type_id),
        FOREIGN KEY (line_item_type_id) REFERENCES line_item_types(line_item_type_id),
        UNIQUE (alias_code, alias_type_id)
    )
    """)
    print("  ✓ line_item_type_aliases")

    # 40. Index Aliases
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS index_aliases (
        index_alias_id TEXT PRIMARY KEY,
        alias_code TEXT NOT NULL,
        alias_type_id TEXT NOT NULL,
        spot_index_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alias_type_id) REFERENCES alias_types(alias_type_id),
        FOREIGN KEY (spot_index_id) REFERENCES spot_indices(spot_index_id),
        UNIQUE (alias_code, alias_type_id)
    )
    """)
    print("  ✓ index_aliases")

    # 41. Price Day Aliases
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_day_aliases (
        price_day_alias_id TEXT PRIMARY KEY,
        alias_code TEXT NOT NULL,
        alias_type_id TEXT NOT NULL,
        price_day_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alias_type_id) REFERENCES alias_types(alias_type_id),
        FOREIGN KEY (price_day_id) REFERENCES price_days(price_day_id),
        UNIQUE (alias_code, alias_type_id)
    )
    """)
    print("  ✓ price_day_aliases")

    # ========================================================================
    # MANAGEMENT TABLES
    # ========================================================================

    print("\n--- MANAGEMENT TABLES ---")

    # 42. Agent Tasks
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
    print("  ✓ agent_tasks")

    # 43. Data Quality Log
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
    print("  ✓ data_quality_log")

    # 44. Agent Metrics
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
    print("  ✓ agent_metrics")

    # 45. Ownership Changes
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
    print("  ✓ ownership_changes")

    # 46. Source Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS source_documents (
        document_id TEXT PRIMARY KEY,
        document_type TEXT NOT NULL,
        document_name TEXT,
        document_url TEXT,
        local_path TEXT,
        location_aliases TEXT,
        rate_examples TEXT,
        effective_date DATE,
        retrieved_date DATE,
        hash_checksum TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ source_documents")

    # ========================================================================
    # ALIAS ERROR TRACKING TABLES
    # ========================================================================

    print("\n--- ALIAS ERROR TRACKING TABLES ---")

    # 47-51. Alias Error Tables
    for alias_type in ['terminal', 'product', 'line_item_type', 'index', 'price_day']:
        table_name = f"{alias_type}_alias_errors"
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            error_id TEXT PRIMARY KEY,
            alias_code TEXT NOT NULL,
            alias_type_id TEXT,
            error_message TEXT,
            batch_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alias_type_id) REFERENCES alias_types(alias_type_id)
        )
        """)
        print(f"  ✓ {table_name}")

    # ========================================================================
    # ETL TRACKING TABLES
    # ========================================================================

    print("\n--- ETL TRACKING TABLES ---")

    # 52. Batches
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS batches (
        batch_id TEXT PRIMARY KEY,
        batch_type TEXT,
        batch_status TEXT DEFAULT 'Pending',
        records_processed INTEGER DEFAULT 0,
        records_succeeded INTEGER DEFAULT 0,
        records_failed INTEGER DEFAULT 0,
        error_message TEXT,
        started_at TIMESTAMP,
        completed_at TIMESTAMP,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ batches")

    # 53. Shipping Tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipping_tracking (
        tracking_id TEXT PRIMARY KEY,
        tenant_id TEXT,
        filename TEXT,
        activity_type_name TEXT,
        count INTEGER DEFAULT 0,
        activity_date DATE,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("  ✓ shipping_tracking")

    # ========================================================================
    # INDEXES
    # ========================================================================

    print("\n--- CREATING INDEXES ---")

    indexes = [
        ("idx_terminals_state", "terminals(state)"),
        ("idx_terminals_tcn", "terminals(irs_tcn)"),
        ("idx_terminals_code", "terminals(terminal_code)"),
        ("idx_terminals_market", "terminals(terminal_market_id)"),
        ("idx_terminal_products_terminal", "terminal_products(terminal_id)"),
        ("idx_terminal_products_product", "terminal_products(product_id)"),
        ("idx_products_category", "products(product_category_id)"),
        ("idx_tasks_status", "agent_tasks(status)"),
        ("idx_tasks_agent_type", "agent_tasks(agent_type)"),
        ("idx_tariffs_pipeline", "pipeline_tariffs(pipeline_id)"),
        ("idx_tariffs_library", "pipeline_tariffs(tariff_library_id)"),
        ("idx_transport_costs_terminal", "transportation_costs(terminal_id)"),
        ("idx_costing_terminal_category", "costing(terminal_id, product_category_id)"),
        ("idx_costing_dates", "costing(start_date, end_date)"),
        ("idx_costing_item", "costing(costing_item_id)"),
        ("idx_shipping_periods_terminal", "shipping_periods(terminal_id)"),
        ("idx_shipping_periods_dates", "shipping_periods(start_date, end_date)"),
        ("idx_shipping_line_items_period", "shipping_line_items(shipping_period_id)"),
        ("idx_shipping_line_items_product", "shipping_line_items(product_id)"),
        ("idx_shipping_line_items_lit", "shipping_line_items(line_item_type_id)"),
        ("idx_spot_indices_market", "spot_indices(spot_market_id)"),
        ("idx_spot_indices_product", "spot_indices(product_id)"),
        ("idx_bcs_type", "bcs(bcs_type_id)"),
        ("idx_bcs_periods_bcs", "bcs_periods(bcs_id)"),
        ("idx_bcs_line_items_period", "bcs_line_items(bcs_period_id)"),
        ("idx_terminal_path_links_terminal", "terminal_path_links(terminal_id)"),
        ("idx_terminal_path_links_path", "terminal_path_links(shipping_path_id)"),
        ("idx_tariff_path_links_path", "tariff_path_links(shipping_path_id)"),
        ("idx_tariff_costs_tariff", "tariff_costs(tariff_id)"),
        ("idx_tariff_costs_library", "tariff_costs(tariff_library_id)"),
        ("idx_shipping_setup_tp", "shipping_setup(terminal_product_id)"),
        ("idx_shipping_setup_lit", "shipping_setup(line_item_type_id)"),
    ]

    for idx_name, idx_def in indexes:
        cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
    print(f"  ✓ Created {len(indexes)} indexes")

    # ========================================================================
    # VIEWS
    # ========================================================================

    print("\n--- CREATING VIEWS ---")

    # View 1: Active Terminals
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_terminals AS
    SELECT * FROM terminals
    WHERE (end_date IS NULL OR end_date > date('now'))
    AND (effective_date IS NULL OR effective_date <= date('now'))
    """)
    print("  ✓ v_active_terminals")

    # View 2: Active Pipeline Tariffs
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_pipeline_tariffs AS
    SELECT * FROM pipeline_tariffs
    WHERE (end_date IS NULL OR end_date > date('now'))
    AND (effective_date IS NULL OR effective_date <= date('now'))
    """)
    print("  ✓ v_active_pipeline_tariffs")

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
    print("  ✓ v_review_queue")

    # View 4: Terminal Products with Names
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_terminal_products AS
    SELECT
        tp.terminal_product_id,
        t.terminal_id,
        t.terminal_name,
        t.terminal_code,
        t.state,
        t.city,
        t.market,
        p.product_id,
        p.product_code,
        p.product_name,
        pc.category_code AS product_category_code,
        tp.shipping_status,
        tp.effective_date,
        tp.end_date
    FROM terminal_products tp
    JOIN terminals t ON tp.terminal_id = t.terminal_id
    JOIN products p ON tp.product_id = p.product_id
    JOIN product_categories pc ON p.product_category_id = pc.category_id
    """)
    print("  ✓ v_terminal_products")

    # View 5: Active Shipping Periods with Line Items
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_shipping AS
    SELECT
        sp.shipping_period_id,
        t.terminal_id,
        t.terminal_name,
        t.state,
        t.city,
        sp.start_date,
        sp.end_date,
        sp.period_status,
        sli.shipping_line_item_id,
        p.product_code,
        lit.line_item_type_name,
        sli.line_item_adder,
        sli.line_item_percent,
        si.spot_index_code
    FROM shipping_periods sp
    JOIN terminals t ON sp.terminal_id = t.terminal_id
    LEFT JOIN shipping_line_items sli ON sp.shipping_period_id = sli.shipping_period_id
    LEFT JOIN products p ON sli.product_id = p.product_id
    LEFT JOIN line_item_types lit ON sli.line_item_type_id = lit.line_item_type_id
    LEFT JOIN spot_indices si ON sli.spot_index_id = si.spot_index_id
    WHERE sp.period_status = 'Active'
    AND (sp.end_date IS NULL OR sp.end_date >= date('now'))
    """)
    print("  ✓ v_active_shipping")

    # View 6: BCS with Line Items
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_bcs_detail AS
    SELECT
        b.bcs_id,
        b.bcs_code,
        b.bcs_name,
        bt.bcs_type_name,
        b.primary_terminal_alias,
        bp.bcs_period_id,
        bp.start_date,
        bp.end_date,
        bps.bcs_period_status_name,
        bli.bcs_line_item_id,
        bli.product_alias,
        bli.line_item_type_alias,
        bli.index_alias,
        bli.price_day_alias,
        bli.line_item_adder,
        bli.line_item_percent
    FROM bcs b
    JOIN bcs_types bt ON b.bcs_type_id = bt.bcs_type_id
    LEFT JOIN bcs_periods bp ON b.bcs_id = bp.bcs_id
    LEFT JOIN bcs_period_statuses bps ON bp.bcs_period_status_id = bps.bcs_period_status_id
    LEFT JOIN bcs_line_items bli ON bp.bcs_period_id = bli.bcs_period_id
    """)
    print("  ✓ v_bcs_detail")

    conn.commit()

    # ========================================================================
    # SEED DATA
    # ========================================================================

    print("\n--- SEEDING REFERENCE DATA ---")

    # Product Categories
    categories = [
        (generate_id(), 'GAS', 'Gasoline'),
        (generate_id(), 'ETH', 'Ethanol'),
        (generate_id(), 'DSL', 'Diesel'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO product_categories (category_id, category_code, category_name)
        VALUES (?, ?, ?)
    """, categories)
    print(f"  ✓ Seeded {len(categories)} product categories (GAS, ETH, DSL)")

    # Get category IDs for product seeding
    gas_id = cursor.execute("SELECT category_id FROM product_categories WHERE category_code = 'GAS'").fetchone()[0]
    eth_id = cursor.execute("SELECT category_id FROM product_categories WHERE category_code = 'ETH'").fetchone()[0]

    # Products
    products_data = [
        (generate_id(), 'CLEAR_GAS', 'Clear Gasoline', gas_id),
        (generate_id(), 'E10', 'E10 (10% Ethanol)', gas_id),
        (generate_id(), 'E15', 'E15 (15% Ethanol)', gas_id),
        (generate_id(), 'E85', 'E85 (85% Ethanol)', eth_id),
        (generate_id(), 'ETHANOL', 'Ethanol (Pure)', eth_id),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO products (product_id, product_code, product_name, product_category_id)
        VALUES (?, ?, ?, ?)
    """, products_data)
    print(f"  ✓ Seeded {len(products_data)} products")

    # Line Item Types (from old system: RIN, CARB 1, CARB 2, Line Space, Ethanol, Combined Adder)
    line_item_types_data = [
        (generate_id(), 'Tariff', 1, 1),
        (generate_id(), 'Facilities Charge', 2, 1),
        (generate_id(), 'Throughput', 3, 1),
        (generate_id(), 'Terminaling Estimate', 4, 1),
        (generate_id(), 'Additive', 5, 1),
        (generate_id(), 'Time Value of Money', 6, 1),
        (generate_id(), 'Basis', 7, 1),
        (generate_id(), 'Margin', 8, 1),
        (generate_id(), 'Fuel Surcharge', 9, 1),
        (generate_id(), 'Transloading Estimate', 10, 1),
        (generate_id(), 'Truck Freight Estimate', 11, 1),
        (generate_id(), 'Line Loss', 12, 1),
        (generate_id(), 'RIN', 13, 1),
        (generate_id(), 'CARB 1', 14, 1),
        (generate_id(), 'CARB 2', 15, 1),
        (generate_id(), 'Line Space', 16, 1),
        (generate_id(), 'Ethanol', 17, 1),
        (generate_id(), 'Combined Adder', 99, 1),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO line_item_types (line_item_type_id, line_item_type_name, display_order, shipping_status)
        VALUES (?, ?, ?, ?)
    """, line_item_types_data)
    print(f"  ✓ Seeded {len(line_item_types_data)} line item types")

    # Costing Items
    costing_items_data = [
        (generate_id(), 'tariff', 'Pipeline tariff cost', 1),
        (generate_id(), 'facilities_charge', 'Terminal facilities charge', 1),
        (generate_id(), 'throughput', 'Terminal throughput rate', 1),
        (generate_id(), 'terminaling_estimate', 'Estimated terminaling cost (if not using facilities + throughput)', 1),
        (generate_id(), 'additive', 'Additive cost', 1),
        (generate_id(), 'tvm', 'Time value of money (interest rate)', 1),
        (generate_id(), 'basis', 'Basis offset from market of origin', 1),
        (generate_id(), 'margin', 'Ethanol margin correction', 1),
        (generate_id(), 'fuel_surcharge', 'Ethanol fuel surcharge', 1),
        (generate_id(), 'transloading_estimate', 'Ethanol transloading cost', 1),
        (generate_id(), 'truck_freight_estimate', 'Ethanol truck freight cost', 1),
        (generate_id(), 'line_loss', 'Pipeline line loss', 1),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO costing_items (costing_item_id, costing_item_name, costing_item_description, shipping_status)
        VALUES (?, ?, ?, ?)
    """, costing_items_data)
    print(f"  ✓ Seeded {len(costing_items_data)} costing items")

    # Price Days
    price_days_data = [
        (generate_id(), 'Prior Day'),
        (generate_id(), 'Spot'),
        (generate_id(), 'Same Day'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO price_days (price_day_id, price_day_name)
        VALUES (?, ?)
    """, price_days_data)
    print(f"  ✓ Seeded {len(price_days_data)} price days")

    # BCS Types
    bcs_types_data = [
        (generate_id(), 'Shipping'),
        (generate_id(), 'Contract'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO bcs_types (bcs_type_id, bcs_type_name)
        VALUES (?, ?)
    """, bcs_types_data)
    print(f"  ✓ Seeded {len(bcs_types_data)} BCS types")

    # BCS Period Statuses
    bcs_status_data = [
        (generate_id(), 'In Progress'),
        (generate_id(), 'Approved'),
        (generate_id(), 'Archived'),
        (generate_id(), 'Expired'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO bcs_period_statuses (bcs_period_status_id, bcs_period_status_name)
        VALUES (?, ?)
    """, bcs_status_data)
    print(f"  ✓ Seeded {len(bcs_status_data)} BCS period statuses")

    # Alias Types
    alias_types_data = [
        (generate_id(), 'EN Master UUID', 'EN system master UUID identifiers'),
        (generate_id(), 'BM Code', 'Benchmark system codes'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO alias_types (alias_type_id, alias_type_code, alias_type_description)
        VALUES (?, ?, ?)
    """, alias_types_data)
    print(f"  ✓ Seeded {len(alias_types_data)} alias types")

    # Index Components
    index_components_data = [
        (generate_id(), 'C', 'Component'),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO index_components (index_component_id, index_component_code, index_component_name)
        VALUES (?, ?, ?)
    """, index_components_data)
    print(f"  ✓ Seeded {len(index_components_data)} index components")

    conn.commit()

    # ========================================================================
    # SUMMARY
    # ========================================================================

    # Count tables
    table_count = cursor.execute("""
        SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """).fetchone()[0]

    view_count = cursor.execute("""
        SELECT COUNT(*) FROM sqlite_master WHERE type='view'
    """).fetchone()[0]

    index_count = cursor.execute("""
        SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'
    """).fetchone()[0]

    print("\n" + "=" * 80)
    print("  DATABASE CREATION COMPLETE!")
    print("=" * 80)
    print(f"\n  Tables created: {table_count}")
    print(f"  Views created:  {view_count}")
    print(f"  Indexes created: {index_count}")
    print(f"\n  Database file: {db_path}")

    print("\n  Table Groups:")
    print("    Master Data:      8 tables (terminals, products, pipelines, etc.)")
    print("    Configuration:    4 tables (line_item_types, costing_items, etc.)")
    print("    Linkage:          5 tables (paths, terminal-pipeline links, etc.)")
    print("    Costing:          7 tables (tariffs, rates, costing, etc.)")
    print("    Shipping:         2 tables (periods, line items)")
    print("    Spot Market:      4 tables (markets, indices, components)")
    print("    BCS:              5 tables (buying cost sheets)")
    print("    Alias/Tenant:     7 tables (aliases for multi-tenant)")
    print("    Management:       5 tables (tasks, quality, metrics)")
    print("    Error Tracking:   5 tables (alias errors)")
    print("    ETL:              2 tables (batches, shipping tracking)")

    print("\n  Seed Data:")
    print("    Product Categories: GAS, ETH, DSL")
    print("    Products: Clear Gas, E10, E15, E85, Ethanol")
    print("    Line Item Types: 18 types (Tariff through Combined Adder)")
    print("    Costing Items: 12 items (tariff, facilities, TVM, etc.)")
    print("    Price Days: Prior Day, Spot, Same Day")
    print("    BCS Types: Shipping, Contract")
    print("    BCS Statuses: In Progress, Approved, Archived, Expired")
    print("    Alias Types: EN Master UUID, BM Code")

    print("\n" + "=" * 80)

    return conn


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("  SUPPLY CHAIN MAPPING - COMPLETE DATABASE SETUP")
    print("  Full Schema with Multi-Tenant Support")
    print("=" * 80)

    conn = create_complete_database('supply_chain.db')
    conn.close()

    print("\n  Next steps:")
    print("    1. Import Excel data:  python excel_import_agent.py")
    print("    2. Check status:       python orchestrator.py --api-key YOUR_KEY status")
    print("    3. View data:          Open supply_chain.db in DB Browser for SQLite")
    print("\n" + "=" * 80 + "\n")

