#!/usr/bin/env python3
"""
Terminal Discovery Agent
Automated discovery of terminals with IRS TCNs using Claude API
"""

import anthropic
import sqlite3
import json
from datetime import datetime
import re
import hashlib

class TerminalDiscoveryAgent:
    """
    Discovers and validates terminals with IRS Terminal Control Numbers
    Uses Claude with web search to find and extract terminal data
    """
    
    def __init__(self, api_key, db_path='supply_chain.db'):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.db_path = db_path
        self.model = "claude-sonnet-4-20250514"
        
    def discover_terminals(self, force_refresh=False):
        """
        Main discovery workflow
        
        Args:
            force_refresh: If True, re-downloads IRS data even if recent version exists
        
        Returns:
            dict: Results summary with new/updated terminals
        """
        print("🔍 Starting Terminal Discovery Agent...")
        
        # Step 1: Find and download IRS Publication 510
        print("  → Searching for IRS Publication 510...")
        pub_510_data = self._find_and_parse_irs_pub_510()
        
        if not pub_510_data:
            print("  ❌ Could not retrieve IRS Publication 510")
            return {'status': 'failed', 'error': 'Could not retrieve IRS data'}
        
        # Step 2: Extract terminal listings
        print(f"  → Extracting terminal listings...")
        terminals = pub_510_data.get('terminals', [])
        print(f"  ✓ Found {len(terminals)} terminals in IRS publication")
        
        # Step 3: Validate and enhance data
        print("  → Validating terminal data...")
        validated_terminals = self._validate_terminals(terminals)
        
        # Step 4: Compare with database and identify changes
        print("  → Comparing with existing database...")
        new_terminals, updated_terminals = self._identify_changes(validated_terminals)
        
        # Step 5: Store in database
        print("  → Updating database...")
        self._store_terminals(new_terminals, updated_terminals)
        
        results = {
            'status': 'completed',
            'total_found': len(terminals),
            'new_terminals': len(new_terminals),
            'updated_terminals': len(updated_terminals),
            'terminals_requiring_review': len([t for t in validated_terminals 
                                             if t.get('confidence') == 'low']),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"\n✅ Discovery complete!")
        print(f"   New terminals: {results['new_terminals']}")
        print(f"   Updated terminals: {results['updated_terminals']}")
        print(f"   Require review: {results['terminals_requiring_review']}")
        
        return results
    
    def _find_and_parse_irs_pub_510(self):
        """
        Use Claude with web search to find and parse IRS Publication 510
        """
        
        # Create a task to find and parse the publication
        message = """I need to find all terminals with IRS Terminal Control Numbers (TCNs) 
        from IRS Publication 510 (Excise Taxes).
        
        Please:
        1. Search for the current version of IRS Publication 510
        2. Look for the section on "Terminal Control Numbers" or "Registered Terminal Operators"
        3. Extract ALL terminal listings that include:
           - Terminal name
           - Terminal operator/owner
           - Location (city and state)
           - Terminal Control Number (TCN) in format XX-XXXXXXX
        
        Return the data as a JSON object with this structure:
        {
            "publication_date": "YYYY-MM-DD",
            "source_url": "URL of the IRS publication",
            "terminals": [
                {
                    "name": "Terminal Name",
                    "operator": "Company Name",
                    "city": "City",
                    "state": "ST",
                    "tcn": "XX-XXXXXXX",
                    "full_address": "Complete address if available"
                }
            ]
        }
        
        Important: Extract ALL terminals, not just a sample. If the list is very long,
        continue searching through all pages/sections of the publication.
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,  # Large response needed for full terminal list
                messages=[{
                    "role": "user",
                    "content": message
                }]
            )
            
            # Extract the response text
            response_text = response.content[0].text
            
            # Try to find JSON in the response
            json_match = re.search(r'\{[\s\S]*"terminals"[\s\S]*\}', response_text)
            if json_match:
                data = json.loads(json_match.group())
                return data
            else:
                print("  ⚠️  Could not parse JSON from response")
                return None
                
        except Exception as e:
            print(f"  ❌ Error in IRS publication search: {str(e)}")
            return None
    
    def _validate_terminals(self, terminals):
        """
        Validate extracted terminal data
        
        Checks:
        - TCN format correctness
        - Required fields present
        - Data quality indicators
        """
        validated = []
        
        for terminal in terminals:
            issues = []
            
            # Check TCN format (XX-XXXXXXX where X is digit)
            tcn = terminal.get('tcn', '')
            if not re.match(r'^\d{2}-\d{7}$', tcn):
                issues.append('Invalid TCN format')
            
            # Check required fields
            required_fields = ['name', 'state', 'tcn']
            for field in required_fields:
                if not terminal.get(field):
                    issues.append(f'Missing {field}')
            
            # Validate state code
            state = terminal.get('state', '')
            if len(state) != 2 or not state.isalpha():
                issues.append('Invalid state code')
            
            # Assign confidence level
            if len(issues) == 0:
                confidence = 'high'
            elif len(issues) <= 2:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            terminal['confidence'] = confidence
            terminal['validation_issues'] = issues
            terminal['validated_at'] = datetime.now().isoformat()
            
            validated.append(terminal)
        
        return validated
    
    def _identify_changes(self, validated_terminals):
        """
        Compare validated terminals against database
        Identify new terminals and updates to existing ones
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get existing terminals
        existing = cursor.execute("""
            SELECT terminal_id, irs_tcn, terminal_name, operator, city, state
            FROM terminals
        """).fetchall()
        
        existing_tcns = {row[1]: row for row in existing}
        
        new_terminals = []
        updated_terminals = []
        
        for terminal in validated_terminals:
            tcn = terminal.get('tcn')
            
            if tcn not in existing_tcns:
                # New terminal
                new_terminals.append(terminal)
            else:
                # Check if any data has changed
                existing_data = existing_tcns[tcn]
                if (terminal.get('name') != existing_data[2] or
                    terminal.get('operator') != existing_data[3] or
                    terminal.get('city') != existing_data[4] or
                    terminal.get('state') != existing_data[5]):
                    updated_terminals.append(terminal)
        
        conn.close()
        return new_terminals, updated_terminals
    
    def _store_terminals(self, new_terminals, updated_terminals):
        """
        Store new and updated terminals in database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for terminal in new_terminals:
            terminal_id = self._generate_terminal_id(terminal)
            
            cursor.execute("""
                INSERT INTO terminals (
                    terminal_id, terminal_name, irs_tcn, state, city,
                    operator, effective_date, data_quality_score,
                    created_by, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                terminal_id,
                terminal.get('name'),
                terminal.get('tcn'),
                terminal.get('state'),
                terminal.get('city'),
                terminal.get('operator'),
                datetime.now().date(),
                self._calculate_quality_score(terminal),
                'terminal_discovery_agent',
                datetime.now()
            ))
            
            # Log quality check
            self._log_quality_check(cursor, 'terminal', terminal_id, terminal)
        
        for terminal in updated_terminals:
            cursor.execute("""
                UPDATE terminals
                SET terminal_name = ?,
                    operator = ?,
                    city = ?,
                    state = ?,
                    updated_at = ?,
                    data_quality_score = ?
                WHERE irs_tcn = ?
            """, (
                terminal.get('name'),
                terminal.get('operator'),
                terminal.get('city'),
                terminal.get('state'),
                datetime.now(),
                self._calculate_quality_score(terminal),
                terminal.get('tcn')
            ))
            
            # Get terminal_id for logging
            terminal_id = cursor.execute(
                "SELECT terminal_id FROM terminals WHERE irs_tcn = ?",
                (terminal.get('tcn'),)
            ).fetchone()[0]
            
            self._log_quality_check(cursor, 'terminal', terminal_id, terminal)
        
        conn.commit()
        conn.close()
    
    def _generate_terminal_id(self, terminal):
        """Generate unique terminal ID"""
        # Format: ST## where ST is state and ## is hash-based number
        state = terminal.get('state', 'XX')
        tcn = terminal.get('tcn', '')
        
        # Use hash of TCN to generate consistent ID
        hash_val = int(hashlib.md5(tcn.encode()).hexdigest()[:4], 16)
        terminal_num = str(hash_val % 10000).zfill(4)
        
        return f"{state}{terminal_num}"
    
    def _calculate_quality_score(self, terminal):
        """Calculate data quality score (0-1)"""
        score = 1.0
        
        # Deduct for missing fields
        if not terminal.get('operator'):
            score -= 0.1
        if not terminal.get('city'):
            score -= 0.1
        if not terminal.get('full_address'):
            score -= 0.05
        
        # Deduct for validation issues
        issues = terminal.get('validation_issues', [])
        score -= len(issues) * 0.15
        
        return max(0.0, score)
    
    def _log_quality_check(self, cursor, record_type, record_id, terminal):
        """Log quality check results"""
        log_id = f"QC_{record_id}_{datetime.now().timestamp()}"
        
        result = 'Pass' if terminal['confidence'] == 'high' else 'Warning'
        details = json.dumps({
            'confidence': terminal['confidence'],
            'issues': terminal.get('validation_issues', []),
            'quality_score': self._calculate_quality_score(terminal)
        })
        
        cursor.execute("""
            INSERT INTO data_quality_log (
                log_id, record_type, record_id, quality_check,
                check_result, check_details, agent_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            log_id, record_type, record_id, 'terminal_validation',
            result, details, 'terminal_discovery_agent'
        ))
    
    def create_discovery_task(self):
        """
        Create a task in the agent_tasks table for this discovery run
        Returns task_id for tracking
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        task_id = f"TERM_DISC_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        cursor.execute("""
            INSERT INTO agent_tasks (
                task_id, agent_type, task_description,
                priority, status, assigned_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            task_id,
            'terminal_discovery',
            'Discover terminals from IRS Publication 510',
            8,  # High priority
            'In Progress',
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        return task_id
    
    def complete_task(self, task_id, results, requires_review=False):
        """Mark task as complete"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE agent_tasks
            SET status = 'Completed',
                completed_timestamp = ?,
                result_summary = ?,
                result_data = ?,
                requires_human_review = ?
            WHERE task_id = ?
        """, (
            datetime.now(),
            f"Found {results['new_terminals']} new, {results['updated_terminals']} updated",
            json.dumps(results),
            requires_review,
            task_id
        ))
        
        conn.commit()
        conn.close()

def run_discovery(api_key):
    """
    Convenience function to run terminal discovery
    """
    agent = TerminalDiscoveryAgent(api_key)
    
    # Create task
    task_id = agent.create_discovery_task()
    print(f"📋 Created task: {task_id}\n")
    
    try:
        # Run discovery
        results = agent.discover_terminals()
        
        # Check if human review needed
        requires_review = results.get('terminals_requiring_review', 0) > 0
        
        # Complete task
        agent.complete_task(task_id, results, requires_review)
        
        if requires_review:
            print(f"\n⚠️  Some terminals require human review")
            print(f"   Check the review queue in the database")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Discovery failed: {str(e)}")
        # Mark task as failed
        conn = sqlite3.connect(agent.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE agent_tasks
            SET status = 'Failed',
                error_message = ?
            WHERE task_id = ?
        """, (str(e), task_id))
        conn.commit()
        conn.close()
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python terminal_discovery_agent.py <ANTHROPIC_API_KEY>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    results = run_discovery(api_key)
    
    print(f"\n📊 Final Results:")
    print(json.dumps(results, indent=2))
