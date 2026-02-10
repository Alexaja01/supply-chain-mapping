#!/usr/bin/env python3
"""
Supply Chain Mapping Orchestrator
Central coordinator for all agent activities
"""

import anthropic
import sqlite3
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Optional

class SupplyChainOrchestrator:
    """
    Master orchestrator that coordinates all agent activities
    Manages task scheduling, execution, and human review workflows
    """
    
    def __init__(self, api_key: str, db_path: str = 'supply_chain.db'):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.db_path = db_path
        self.model = "claude-sonnet-4-20250514"
        
    # ============================================================================
    # TASK CREATION & SCHEDULING
    # ============================================================================
    
    def create_task(self, agent_type: str, description: str, 
                   parameters: Optional[Dict] = None, priority: int = 5) -> str:
        """
        Create a new task for an agent
        
        Args:
            agent_type: Type of agent (e.g., 'terminal_discovery')
            description: Human-readable task description
            parameters: JSON-serializable dict of task parameters
            priority: 1-10, higher = more urgent
        
        Returns:
            task_id: Unique identifier for this task
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        task_id = f"{agent_type.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        cursor.execute("""
            INSERT INTO agent_tasks (
                task_id, agent_type, task_description, task_parameters,
                priority, status, assigned_timestamp
            ) VALUES (?, ?, ?, ?, ?, 'Pending', ?)
        """, (
            task_id,
            agent_type,
            description,
            json.dumps(parameters) if parameters else None,
            priority,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        return task_id
    
    # ============================================================================
    # SCHEDULED WORKFLOWS
    # ============================================================================
    
    def schedule_daily_tasks(self):
        """
        Schedule routine daily tasks
        Run this every morning or via cron
        """
        print("\n" + "="*80)
        print(f"📅 DAILY WORKFLOW - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        tasks_created = []
        
        # 1. Check for new FERC tariff filings
        task_id = self.create_task(
            agent_type='pipeline_tariff',
            description='Check FERC eTariff for new pipeline tariff filings from last 24 hours',
            parameters={'lookback_hours': 24, 'auto_download': True},
            priority=8
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        # 2. Monitor for ownership changes
        task_id = self.create_task(
            agent_type='ownership_tracking',
            description='Search for terminal/pipeline M&A announcements from last 24 hours',
            parameters={'sources': ['sec_edgar', 'news', 'press_releases']},
            priority=7
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        # 3. Quality assurance spot check
        task_id = self.create_task(
            agent_type='quality_assurance',
            description='Run quality checks on 50 random terminal records',
            parameters={'sample_size': 50, 'check_types': ['completeness', 'accuracy']},
            priority=6
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        print(f"\n📋 Created {len(tasks_created)} daily tasks")
        return tasks_created
    
    def schedule_weekly_tasks(self):
        """
        Schedule routine weekly tasks
        Run this every Monday morning
        """
        print("\n" + "="*80)
        print(f"📅 WEEKLY WORKFLOW - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        tasks_created = []
        
        # 1. Terminal discovery (IRS Pub 510 check)
        task_id = self.create_task(
            agent_type='terminal_discovery',
            description='Check IRS Publication 510 for new terminals',
            parameters={'force_refresh': False},
            priority=8
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        # 2. Rail rate updates
        task_id = self.create_task(
            agent_type='rail_rate',
            description='Check Class I railroad websites for rate updates',
            parameters={'railroads': ['UP', 'BNSF', 'NS', 'CSX', 'CN', 'CP']},
            priority=7
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        # 3. Data normalization sweep
        task_id = self.create_task(
            agent_type='data_normalization',
            description='Normalize and standardize data from last week',
            parameters={'lookback_days': 7},
            priority=6
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        print(f"\n📋 Created {len(tasks_created)} weekly tasks")
        return tasks_created
    
    def schedule_monthly_tasks(self):
        """
        Schedule routine monthly tasks
        Run this on the 1st of each month
        """
        print("\n" + "="*80)
        print(f"📅 MONTHLY WORKFLOW - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*80)
        
        tasks_created = []
        
        # 1. Terminal information update
        task_id = self.create_task(
            agent_type='terminal_information',
            description='Update operational details for all terminals added >30 days ago',
            parameters={'update_fields': ['capacity', 'operator', 'products_handled']},
            priority=9
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        # 2. Refinery linkage audit
        task_id = self.create_task(
            agent_type='refinery_linkage',
            description='Verify refinery connections and product slates from EIA data',
            parameters={'data_source': 'eia'},
            priority=8
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        # 3. Comprehensive linkage validation
        task_id = self.create_task(
            agent_type='linkage_validation',
            description='Validate all terminal->pipeline->refinery connections',
            parameters={'fix_orphans': True},
            priority=7
        )
        tasks_created.append(task_id)
        print(f"✓ Created: {task_id}")
        
        print(f"\n📋 Created {len(tasks_created)} monthly tasks")
        return tasks_created
    
    # ============================================================================
    # TASK EXECUTION
    # ============================================================================
    
    def process_task_queue(self, max_tasks: int = 10, agent_type: Optional[str] = None):
        """
        Process pending tasks from the queue
        
        Args:
            max_tasks: Maximum number of tasks to process
            agent_type: If specified, only process tasks for this agent type
        
        Returns:
            List of task results
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query
        query = """
            SELECT task_id, agent_type, task_description, task_parameters
            FROM agent_tasks
            WHERE status = 'Pending'
        """
        params = []
        
        if agent_type:
            query += " AND agent_type = ?"
            params.append(agent_type)
        
        query += """
            ORDER BY priority DESC, assigned_timestamp ASC
            LIMIT ?
        """
        params.append(max_tasks)
        
        tasks = cursor.execute(query, params).fetchall()
        conn.close()
        
        if not tasks:
            print("📭 No pending tasks in queue")
            return []
        
        print(f"\n🔄 Processing {len(tasks)} tasks...")
        results = []
        
        for task_id, agent_type, description, params_json in tasks:
            print(f"\n  → {task_id}")
            print(f"    {description}")
            
            try:
                result = self._execute_task(task_id, agent_type, description, params_json)
                results.append(result)
                
                if result.get('requires_review'):
                    print(f"    ⚠️  Requires human review")
                else:
                    print(f"    ✓ Completed")
                    
            except Exception as e:
                print(f"    ❌ Failed: {str(e)}")
                self._mark_task_failed(task_id, str(e))
        
        # Generate review summary if needed
        review_items = [r for r in results if r.get('requires_review')]
        if review_items:
            self._generate_review_report(review_items)
        
        return results
    
    def _execute_task(self, task_id: str, agent_type: str, 
                     description: str, params_json: Optional[str]) -> Dict:
        """
        Execute a single task using appropriate agent
        """
        # Mark as in progress
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE agent_tasks
            SET status = 'In Progress', started_timestamp = ?
            WHERE task_id = ?
        """, (datetime.now(), task_id))
        conn.commit()
        conn.close()
        
        # Parse parameters
        parameters = json.loads(params_json) if params_json else {}
        
        # Execute based on agent type
        if agent_type == 'terminal_discovery':
            from terminal_discovery_agent import TerminalDiscoveryAgent
            agent = TerminalDiscoveryAgent(self.client.api_key, self.db_path)
            result = agent.discover_terminals(
                force_refresh=parameters.get('force_refresh', False)
            )
            
        # Add other agent types here as they're implemented
        # elif agent_type == 'pipeline_tariff':
        #     from pipeline_tariff_agent import PipelineTariffAgent
        #     agent = PipelineTariffAgent(self.client.api_key, self.db_path)
        #     result = agent.collect_tariffs(...)
        
        else:
            # For not-yet-implemented agents, use Claude directly
            result = self._execute_generic_agent(agent_type, description, parameters)
        
        # Assess if human review is needed
        requires_review = self._assess_review_need(result, agent_type)
        
        # Mark as complete
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
            self._summarize_result(result),
            json.dumps(result),
            requires_review,
            task_id
        ))
        conn.commit()
        conn.close()
        
        return {**result, 'requires_review': requires_review}
    
    def _execute_generic_agent(self, agent_type: str, description: str, 
                              parameters: Dict) -> Dict:
        """
        Fallback: Execute task using Claude directly with specialized prompt
        Used for agents not yet implemented as separate classes
        """
        system_prompt = self._get_agent_system_prompt(agent_type)
        
        # Construct user message
        user_message = f"{description}\n\nParameters: {json.dumps(parameters, indent=2)}"
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Parse response
        response_text = response.content[0].text
        
        # Try to extract JSON result
        try:
            json_match = json.loads(response_text)
            return json_match
        except:
            return {
                'status': 'completed',
                'result': response_text,
                'agent_type': agent_type
            }
    
    def _get_agent_system_prompt(self, agent_type: str) -> str:
        """
        Get specialized system prompt for each agent type
        """
        base_prompt = """You are a specialized data collection and processing agent 
        for a refined products supply chain mapping project. Your role is to be 
        thorough, accurate, and autonomous while flagging ambiguous cases for human review.
        
        Always return results in JSON format when possible.
        Flag items needing human review with confidence levels."""
        
        # Agent-specific prompts
        prompts = {
            'pipeline_tariff': base_prompt + """
            
            Your task is to collect pipeline tariffs from FERC filings.
            
            Process:
            1. Search FERC eTariff database for recent filings
            2. Extract rate tables (origin, destination, rate)
            3. Convert all rates to $/gallon
            4. Include effective dates
            
            Return JSON with extracted rates and source documents.
            """,
            
            'rail_rate': base_prompt + """
            
            Your task is to collect rail tariffs, especially for ethanol transport.
            
            Process:
            1. Search Class I railroad websites for rate updates
            2. Access STB (Surface Transportation Board) filings if needed
            3. Extract rates with fuel surcharges
            4. Calculate per-gallon rates from mileage-based pricing
            
            Return JSON with rates and routing information.
            """,
            
            'ownership_tracking': base_prompt + """
            
            Your task is to monitor asset ownership changes.
            
            Process:
            1. Search for M&A announcements involving terminals/pipelines
            2. Check SEC EDGAR for relevant 8-K filings
            3. Identify transaction details: buyer, seller, assets, dates
            
            Return JSON with ownership change details.
            """,
            
            # Add more as needed...
        }
        
        return prompts.get(agent_type, base_prompt)
    
    def _assess_review_need(self, result: Dict, agent_type: str) -> bool:
        """
        Determine if result needs human review
        """
        # Check if result explicitly requests review
        if result.get('requires_review'):
            return True
        
        # Check for low confidence items
        if agent_type == 'terminal_discovery':
            low_conf = result.get('terminals_requiring_review', 0)
            return low_conf > 0
        
        # Check for anomalies
        if agent_type == 'pipeline_tariff':
            # Flag unusually high rates for review
            rates = result.get('tariffs', [])
            unusual = [r for r in rates if r.get('rate_per_gallon', 0) > 0.5]
            return len(unusual) > 0
        
        return False
    
    def _summarize_result(self, result: Dict) -> str:
        """Create human-readable summary of result"""
        if 'summary' in result:
            return result['summary']
        
        # Generate summary based on result structure
        status = result.get('status', 'unknown')
        if status == 'completed':
            if 'new_terminals' in result:
                return f"Found {result['new_terminals']} new, {result.get('updated_terminals', 0)} updated terminals"
            elif 'tariffs_collected' in result:
                return f"Collected {result['tariffs_collected']} tariffs"
        
        return str(result)[:200]
    
    def _mark_task_failed(self, task_id: str, error: str):
        """Mark a task as failed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE agent_tasks
            SET status = 'Failed',
                completed_timestamp = ?,
                error_message = ?
            WHERE task_id = ?
        """, (datetime.now(), error, task_id))
        conn.commit()
        conn.close()
    
    # ============================================================================
    # HUMAN REVIEW MANAGEMENT
    # ============================================================================
    
    def _generate_review_report(self, review_items: List[Dict]):
        """
        Generate report of items needing human review
        """
        print(f"\n" + "="*80)
        print(f"⚠️  HUMAN REVIEW REQUIRED - {len(review_items)} items")
        print("="*80)
        
        for i, item in enumerate(review_items, 1):
            print(f"\n{i}. Agent: {item.get('agent_type', 'unknown')}")
            print(f"   Reason: {item.get('review_reason', 'Quality check needed')}")
            print(f"   Details: {self._summarize_result(item)[:100]}...")
        
        print(f"\n💡 Access review queue: SELECT * FROM v_review_queue")
    
    def get_review_queue(self) -> List[Dict]:
        """
        Get all tasks awaiting human review
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tasks = cursor.execute("""
            SELECT task_id, agent_type, task_description, 
                   completed_timestamp, result_summary
            FROM v_review_queue
        """).fetchall()
        
        conn.close()
        
        return [
            {
                'task_id': t[0],
                'agent_type': t[1],
                'description': t[2],
                'completed': t[3],
                'summary': t[4]
            }
            for t in tasks
        ]
    
    # ============================================================================
    # REPORTING
    # ============================================================================
    
    def generate_status_report(self) -> Dict:
        """
        Generate comprehensive status report
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Task statistics
        task_stats = cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM agent_tasks
            GROUP BY status
        """).fetchall()
        
        # Data statistics
        terminal_count = cursor.execute("""
            SELECT COUNT(*) FROM v_active_terminals
        """).fetchone()[0]
        
        pipeline_count = cursor.execute("""
            SELECT COUNT(*) FROM pipelines
            WHERE end_date IS NULL OR end_date > date('now')
        """).fetchone()[0]
        
        tariff_count = cursor.execute("""
            SELECT COUNT(*) FROM v_active_pipeline_tariffs
        """).fetchone()[0]
        
        # Review queue
        review_count = cursor.execute("""
            SELECT COUNT(*) FROM v_review_queue
        """).fetchone()[0]
        
        conn.close()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'tasks': {status: count for status, count in task_stats},
            'data': {
                'terminals': terminal_count,
                'pipelines': pipeline_count,
                'tariffs': tariff_count
            },
            'review_queue': review_count
        }
        
        return report
    
    def print_status_report(self):
        """Print formatted status report"""
        report = self.generate_status_report()
        
        print("\n" + "="*80)
        print(f"📊 SUPPLY CHAIN MAPPING PROJECT STATUS")
        print(f"   Generated: {report['timestamp']}")
        print("="*80)
        
        print(f"\n📋 Tasks:")
        for status, count in report['tasks'].items():
            print(f"   {status}: {count}")
        
        print(f"\n📁 Data Coverage:")
        print(f"   Terminals: {report['data']['terminals']}")
        print(f"   Pipelines: {report['data']['pipelines']}")
        print(f"   Tariffs: {report['data']['tariffs']}")
        
        if report['review_queue'] > 0:
            print(f"\n⚠️  Items in review queue: {report['review_queue']}")
        
        print("="*80)

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main CLI entry point"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Supply Chain Mapping Orchestrator')
    parser.add_argument('--api-key', required=True, help='Anthropic API key')
    parser.add_argument('--db', default='supply_chain.db', help='Database path')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Schedule commands
    subparsers.add_parser('daily', help='Run daily tasks')
    subparsers.add_parser('weekly', help='Run weekly tasks')
    subparsers.add_parser('monthly', help='Run monthly tasks')
    
    # Process commands
    process_parser = subparsers.add_parser('process', help='Process task queue')
    process_parser.add_argument('--max-tasks', type=int, default=10)
    process_parser.add_argument('--agent-type', help='Only process specific agent type')
    
    # Status commands
    subparsers.add_parser('status', help='Show status report')
    subparsers.add_parser('review', help='Show review queue')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    orchestrator = SupplyChainOrchestrator(args.api_key, args.db)
    
    if args.command == 'daily':
        orchestrator.schedule_daily_tasks()
        orchestrator.process_task_queue()
        
    elif args.command == 'weekly':
        orchestrator.schedule_weekly_tasks()
        orchestrator.process_task_queue()
        
    elif args.command == 'monthly':
        orchestrator.schedule_monthly_tasks()
        orchestrator.process_task_queue()
        
    elif args.command == 'process':
        orchestrator.process_task_queue(
            max_tasks=args.max_tasks,
            agent_type=args.agent_type
        )
        
    elif args.command == 'status':
        orchestrator.print_status_report()
        
    elif args.command == 'review':
        queue = orchestrator.get_review_queue()
        print(f"\n📋 Review Queue ({len(queue)} items):\n")
        for item in queue:
            print(f"  {item['task_id']}")
            print(f"    {item['description']}")
            print(f"    {item['summary']}\n")

if __name__ == "__main__":
    main()
