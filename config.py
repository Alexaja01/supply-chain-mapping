"""
Configuration file for Supply Chain Mapping Project
Contains all paths, settings, and constants
"""

import os

# =============================================================================
# BASE PATHS
# =============================================================================

# Project root - where your GitHub repo is
PROJECT_ROOT = r"C:\Users\jalex\supply-chain\supply-chain-mapping"

# Parent directory - contains both repo and tariff library
PARENT_DIR = r"C:\Users\jalex\supply-chain"

# =============================================================================
# DATA PATHS
# =============================================================================

# Database
DATABASE_PATH = os.path.join(PROJECT_ROOT, "supply_chain.db")

# Tariff library (local folder with all PDFs)
TARIFF_LIBRARY = os.path.join(PARENT_DIR, "tariff_library")
PIPELINE_TARIFFS = os.path.join(TARIFF_LIBRARY, "pipelines")
RAIL_TARIFFS = os.path.join(TARIFF_LIBRARY, "railroads")
TERMINAL_TARIFFS = os.path.join(TARIFF_LIBRARY, "terminals")

# Reference materials (in GitHub repo)
REFERENCE_DIR = os.path.join(PROJECT_ROOT, "reference")
SAMPLE_TARIFFS = os.path.join(REFERENCE_DIR, "sample_tariffs")
EXCEL_REFERENCE = os.path.join(REFERENCE_DIR, "excel")

# Output directory for generated reports/files
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

# =============================================================================
# API SETTINGS
# =============================================================================

# Claude API
CLAUDE_MODEL = "claude-sonnet-4-20250514"
DEFAULT_MAX_TOKENS = 8000

# =============================================================================
# AGENT SETTINGS
# =============================================================================

# Quality thresholds
MIN_CONFIDENCE_SCORE = 0.7  # Minimum confidence to auto-accept
HIGH_CONFIDENCE_SCORE = 0.9  # High confidence, no review needed

# Task priorities (1-10, higher = more urgent)
PRIORITY_CRITICAL = 10
PRIORITY_HIGH = 8
PRIORITY_MEDIUM = 5
PRIORITY_LOW = 3

# =============================================================================
# DATA VALIDATION
# =============================================================================

# Expected data formats
TCN_PATTERN = r'^\d{2}-\d{7}$'  # Format: XX-XXXXXXX
STATE_CODES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
               'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
               'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
               'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
               'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def ensure_directories_exist():
    """Create necessary directories if they don't exist"""
    dirs_to_create = [
        OUTPUT_DIR,
        TARIFF_LIBRARY,
        PIPELINE_TARIFFS,
        RAIL_TARIFFS,
        TERMINAL_TARIFFS,
        SAMPLE_TARIFFS,
        EXCEL_REFERENCE
    ]
    
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
    
    print("✓ All directories verified/created")

def get_tariff_path(operator_type, operator_name):
    """
    Get the path to a specific operator's tariff folder
    
    Args:
        operator_type: 'pipeline', 'railroad', or 'terminal'
        operator_name: Name of the operator (e.g., 'Colonial', 'UP')
    
    Returns:
        Full path to the operator's tariff folder
    """
    base_paths = {
        'pipeline': PIPELINE_TARIFFS,
        'railroad': RAIL_TARIFFS,
        'terminal': TERMINAL_TARIFFS
    }
    
    if operator_type not in base_paths:
        raise ValueError(f"Invalid operator_type: {operator_type}")
    
    return os.path.join(base_paths[operator_type], operator_name)

# =============================================================================
# INITIALIZATION
# =============================================================================

if __name__ == "__main__":
    # Test the configuration
    print("Configuration Test")
    print("=" * 80)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Database: {DATABASE_PATH}")
    print(f"Tariff Library: {TARIFF_LIBRARY}")
    print(f"Sample Tariffs: {SAMPLE_TARIFFS}")
    print("\nCreating directories...")
    ensure_directories_exist()
    print("\n✅ Configuration loaded successfully!")