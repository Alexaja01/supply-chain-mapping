#!/usr/bin/env python3
"""
Terminal Capture Agent — IRS Publication 510
Stage 1 of the asset agent pipeline: Capture → Validate → Enrich

Design constraints (per PROJECT_STATE.md):
  - Writes to terminal_capture_staging, never directly to terminals
  - Uses uuid.uuid4() for all primary keys
  - Passes web_search tool explicitly in all Claude API calls needing live data
"""

import json
import os
import re
import sqlite3
import uuid
from datetime import datetime

import anthropic

import config


class TerminalCaptureAgent:
    """
    Captures terminal records from IRS Publication 510 into terminal_capture_staging.

    Every terminal found is written to the staging table with a confidence score
    and any conflict flags.  Promotion to the terminals table is handled downstream
    by terminal_validate_agent.py.
    """

    def __init__(self, api_key, db_path=config.DATABASE_PATH):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.db_path = db_path

    # =========================================================================
    # PRIMARY METHOD
    # =========================================================================

    def capture_from_irs_510(self):
        """
        Main capture workflow.

        Returns:
            dict: {
                "status": "completed",
                "batch_id": "<uuid>",
                "total_captured": N,
                "new_terminals": N,
                "conflicts_found": N,
                "low_confidence": N,
                "timestamp": "<iso>"
            }
        """
        print("Starting Terminal Capture Agent — IRS Publication 510...")

        batch_id = str(uuid.uuid4())
        task_id = self._create_capture_task()
        self._start_batch(batch_id)

        total_captured = 0
        new_terminals = 0
        conflicts_found = 0
        low_confidence = 0

        try:
            print("  Fetching IRS Publication 510 terminal data via web search...")
            terminals = self._fetch_irs_510_terminals()

            if not terminals:
                print("  No terminals returned — check Claude response above.")
            else:
                print(f"  Returned {len(terminals)} terminal records. Writing to staging...")

                conn = sqlite3.connect(self.db_path)
                try:
                    for terminal in terminals:
                        confidence = self._score_confidence(terminal)
                        conflict_flags = self._detect_conflicts(conn, terminal)
                        self._write_to_staging(
                            conn, terminal, confidence, conflict_flags, batch_id
                        )

                        total_captured += 1
                        if conflict_flags:
                            conflicts_found += 1
                        else:
                            new_terminals += 1
                        if confidence < config.STAGING_REVIEW_THRESHOLD:
                            low_confidence += 1

                    conn.commit()
                finally:
                    conn.close()

                print(f"  Staged {total_captured} terminals.")
                print(
                    f"    New: {new_terminals}  |  "
                    f"Conflicts: {conflicts_found}  |  "
                    f"Low confidence: {low_confidence}"
                )

            self._complete_batch(batch_id, total_captured, total_captured)

            results = {
                "status": "completed",
                "batch_id": batch_id,
                "total_captured": total_captured,
                "new_terminals": new_terminals,
                "conflicts_found": conflicts_found,
                "low_confidence": low_confidence,
                "timestamp": datetime.now().isoformat(),
            }
            self._complete_task(task_id, results)
            return results

        except Exception as exc:
            print(f"  Capture failed: {exc}")
            self._fail_batch(batch_id, str(exc))
            self._fail_task(task_id, str(exc))
            raise

    # =========================================================================
    # FETCH — Claude + web_search
    # =========================================================================

    def _fetch_irs_510_terminals(self):
        """
        Locate, download, and parse the IRS TCN Directory.

        Flow:
          1. Claude + web_search  → find the current download URL on irs.gov
          2. urllib               → download the file (CSV or Excel) to a temp path
          3. csv / openpyxl       → parse rows into terminal dicts
        """
        print("  Searching for IRS TCN Directory download URL...")
        url = self._find_tcn_directory_url()
        if not url:
            print("  Could not locate TCN Directory download URL.")
            return []

        print(f"  TCN Directory URL: {url}")
        local_path = self._download_tcn_file(url)
        if not local_path:
            return []

        try:
            terminals = self._parse_tcn_file(local_path)
            print(f"  Parsed {len(terminals)} terminal records.")
            return terminals
        finally:
            try:
                os.unlink(local_path)
            except OSError:
                pass

    def _find_tcn_directory_url(self):
        """
        Use Claude + web_search to locate the current TCN Directory download URL
        at irs.gov/businesses/small-businesses-self-employed/terminal-control-number-tcn-directory.

        Returns the URL string, or None if not found.
        """
        prompt = (
            "Visit https://www.irs.gov/businesses/small-businesses-self-employed/"
            "terminal-control-number-tcn-directory and find the direct download link "
            "for the TCN Directory file. It is typically a CSV or Excel (.xlsx) file "
            "hosted under irs.gov/pub/.\n\n"
            "Return ONLY the direct download URL as a single line of plain text. "
            "No explanation, no JSON, no markdown."
        )

        response = self.client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=500,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text
        response_text = response_text.strip()

        # Prefer a URL that ends with a known file extension
        match = re.search(
            r'https?://\S+\.(?:csv|xlsx|xls)\b', response_text, re.IGNORECASE
        )
        if match:
            return match.group().rstrip(".,)")

        # Fallback: any irs.gov/pub/ path (file extension may be absent from URL)
        match = re.search(
            r'https?://(?:www\.)?irs\.gov/pub/\S+', response_text, re.IGNORECASE
        )
        if match:
            return match.group().rstrip(".,)")

        # Last resort: first URL in the response
        match = re.search(r'https?://\S+', response_text)
        if match:
            return match.group().rstrip(".,)")

        print(f"  No URL found in Claude response: {response_text[:200]}")
        return None

    def _download_tcn_file(self, url):
        """
        Download the TCN Directory file to a temporary path.

        Returns the local file path, or None on failure.
        """
        import tempfile
        import urllib.request

        lower_url = url.lower()
        suffix = ".xlsx" if ".xlsx" in lower_url else ".xls" if ".xls" in lower_url else ".csv"

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.close()

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; supply-chain-agent/1.0)"},
            )
            print(f"  Downloading TCN Directory ({suffix})...")
            with urllib.request.urlopen(req, timeout=60) as resp:
                with open(tmp.name, "wb") as fh:
                    fh.write(resp.read())
            return tmp.name
        except Exception as exc:
            print(f"  Download failed: {exc}")
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
            return None

    def _parse_tcn_file(self, path):
        """Dispatch to CSV or Excel parser based on file extension."""
        if path.lower().endswith(".csv"):
            return self._parse_tcn_csv(path)
        return self._parse_tcn_excel(path)

    def _parse_tcn_csv(self, path):
        """Parse a CSV TCN Directory into a list of terminal dicts."""
        import csv

        for encoding in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                terminals = []
                with open(path, newline="", encoding=encoding) as fh:
                    for row in csv.DictReader(fh):
                        t = self._normalize_tcn_row(row)
                        if t is not None:
                            terminals.append(t)
                print(f"  Parsed CSV: {len(terminals)} records (encoding: {encoding})")
                return terminals
            except UnicodeDecodeError:
                continue
            except Exception as exc:
                print(f"  CSV parse error: {exc}")
                return []

        print("  Could not decode CSV with any supported encoding.")
        return []

    def _parse_tcn_excel(self, path):
        """Parse an Excel (.xlsx / .xls) TCN Directory into a list of terminal dicts."""
        try:
            import openpyxl
        except ImportError:
            print("  openpyxl is required for Excel files: pip install openpyxl")
            return []

        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            ws = wb.active
            rows = list(ws.rows)
            if not rows:
                return []

            headers = [str(cell.value or "").strip() for cell in rows[0]]
            terminals = []
            for row in rows[1:]:
                values = [str(cell.value or "").strip() for cell in row]
                t = self._normalize_tcn_row(dict(zip(headers, values)))
                if t is not None:
                    terminals.append(t)

            print(f"  Parsed Excel: {len(terminals)} records")
            return terminals
        except Exception as exc:
            print(f"  Excel parse error: {exc}")
            return []

    def _normalize_tcn_row(self, row):
        """
        Map an IRS TCN Directory row (any column naming convention) to our
        standard terminal dict.  Returns None for blank rows.

        IRS column names vary by publication year; we match case-insensitively
        against known aliases for each field.
        """
        lc = {k.lower().strip(): str(v or "").strip() for k, v in row.items()}

        def pick(*candidates):
            for c in candidates:
                v = lc.get(c, "")
                if v:
                    return v
            return ""

        tcn      = pick("tcn", "terminal control number", "terminal_control_number",
                        "control number", "control_number")
        name     = pick("terminal name", "terminal_name", "name",
                        "facility name", "facility_name", "terminal")
        operator = pick("operator", "operator name", "operator_name",
                        "company", "company name", "company_name", "registrant")
        city     = pick("city")
        state    = pick("state", "state code", "state_code", "st")
        address  = pick("address", "street address", "street_address",
                        "street", "address1", "addr")
        county   = pick("county")
        owner    = pick("owner", "owner name", "owner_name")
        zip_code = pick("zip", "zip code", "zip_code", "zipcode",
                        "postal code", "postal_code")

        if not any([tcn, name, operator]):
            return None  # skip blank / header-only rows

        return {
            "tcn":      tcn,
            "name":     name,
            "operator": operator,
            "city":     city,
            "state":    state,
            "address":  address,
            "county":   county,
            "owner":    owner,
            "zip":      zip_code,
        }

    # =========================================================================
    # CONFIDENCE SCORING
    # =========================================================================

    def _score_confidence(self, terminal):
        """
        Score field completeness on a 0.0–1.0 scale.

        Deductions:
          -0.20  raw_tcn missing or does not match config.TCN_PATTERN
          -0.15  raw_name missing
          -0.10  raw_state missing or not in config.STATE_CODES
          -0.10  raw_city missing
          -0.10  raw_operator missing
          Minimum: 0.0
        """
        score = 1.0

        tcn = (terminal.get("tcn") or "").strip()
        if not tcn or not re.match(config.TCN_PATTERN, tcn):
            score -= 0.20

        if not (terminal.get("name") or "").strip():
            score -= 0.15

        state = (terminal.get("state") or "").strip().upper()
        if not state or state not in config.STATE_CODES:
            score -= 0.10

        if not (terminal.get("city") or "").strip():
            score -= 0.10

        if not (terminal.get("operator") or "").strip():
            score -= 0.10

        return max(0.0, round(score, 4))

    # =========================================================================
    # CONFLICT DETECTION
    # =========================================================================

    def _detect_conflicts(self, conn, terminal):
        """
        Check whether the TCN already exists in the terminals table.

        Returns:
            list[dict]: Conflict flag dicts, empty if no conflict.
                        Example flag:
                        {
                            "type": "existing_tcn",
                            "terminal_id": "<id>",
                            "existing_name": "<name>"
                        }
        """
        flags = []
        tcn = (terminal.get("tcn") or "").strip()
        if not tcn:
            return flags

        row = conn.execute(
            "SELECT terminal_id, terminal_name FROM terminals WHERE irs_tcn = ?",
            (tcn,),
        ).fetchone()

        if row:
            flags.append(
                {
                    "type": "existing_tcn",
                    "terminal_id": row[0],
                    "existing_name": row[1],
                }
            )

        return flags

    # =========================================================================
    # STAGING WRITE
    # =========================================================================

    def _write_to_staging(self, conn, terminal, confidence, conflict_flags, batch_id):
        """
        Insert one terminal record into terminal_capture_staging.

        Records are NEVER skipped — conflict flags travel with the record so
        the validation agent can resolve them.
        """
        conn.execute(
            f"""
            INSERT INTO {config.ASSET_STAGING_TABLE} (
                staging_id,
                capture_source,
                raw_tcn,
                raw_name,
                raw_city,
                raw_state,
                raw_county,
                raw_operator,
                raw_owner,
                raw_address,
                raw_data,
                capture_timestamp,
                confidence_score,
                conflict_flags,
                status,
                batch_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),                               # staging_id
                config.CAPTURE_SOURCES[0],                      # "IRS_510"
                _clean(terminal.get("tcn")),                    # raw_tcn
                _clean(terminal.get("name")),                   # raw_name
                _clean(terminal.get("city")),                   # raw_city
                _upper(terminal.get("state")),                  # raw_state
                _clean(terminal.get("county")),                 # raw_county
                _clean(terminal.get("operator")),               # raw_operator
                _clean(terminal.get("owner")),                  # raw_owner
                _clean(terminal.get("address")),                # raw_address
                json.dumps(terminal),                           # raw_data (full blob)
                datetime.now().isoformat(),                     # capture_timestamp
                confidence,                                     # confidence_score
                json.dumps(conflict_flags),                     # conflict_flags
                "pending",                                      # status
                batch_id,                                       # batch_id
            ),
        )

    # =========================================================================
    # BATCH TRACKING
    # =========================================================================

    def _start_batch(self, batch_id):
        """Insert a new batch record with status 'In Progress'."""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                INSERT INTO batches (
                    batch_id, batch_type, batch_status, started_at
                ) VALUES (?, ?, ?, ?)
                """,
                (batch_id, "IRS_510_CAPTURE", "In Progress", datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

    def _complete_batch(self, batch_id, records_processed, records_succeeded):
        """Update the batch record to 'Completed'."""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                UPDATE batches
                SET batch_status      = 'Completed',
                    records_processed = ?,
                    records_succeeded = ?,
                    completed_at      = ?
                WHERE batch_id = ?
                """,
                (
                    records_processed,
                    records_succeeded,
                    datetime.now().isoformat(),
                    batch_id,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def _fail_batch(self, batch_id, error_message):
        """Update the batch record to 'Failed'."""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                UPDATE batches
                SET batch_status  = 'Failed',
                    error_message = ?,
                    completed_at  = ?
                WHERE batch_id = ?
                """,
                (error_message, datetime.now().isoformat(), batch_id),
            )
            conn.commit()
        finally:
            conn.close()

    # =========================================================================
    # TASK TRACKING
    # =========================================================================

    def _create_capture_task(self):
        """
        Insert a task into agent_tasks and return its task_id.
        Mirrors the pattern from terminal_discovery_agent.create_discovery_task()
        but uses uuid.uuid4() instead of a timestamp-based ID.
        """
        task_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                INSERT INTO agent_tasks (
                    task_id,
                    agent_type,
                    task_description,
                    priority,
                    status,
                    assigned_timestamp,
                    started_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    "terminal_capture",
                    "Capture terminals from IRS Publication 510 into staging table",
                    config.PRIORITY_HIGH,
                    "In Progress",
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return task_id

    def _complete_task(self, task_id, results):
        """Mark the task as Completed with a summary and result payload."""
        requires_review = results.get("low_confidence", 0) > 0
        summary = (
            f"Captured {results['total_captured']} terminals — "
            f"{results['new_terminals']} new, "
            f"{results['conflicts_found']} conflicts, "
            f"{results['low_confidence']} below confidence threshold "
            f"({config.STAGING_REVIEW_THRESHOLD})"
        )

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                UPDATE agent_tasks
                SET status               = 'Completed',
                    completed_timestamp  = ?,
                    result_summary       = ?,
                    result_data          = ?,
                    requires_human_review = ?
                WHERE task_id = ?
                """,
                (
                    datetime.now().isoformat(),
                    summary,
                    json.dumps(results),
                    1 if requires_review else 0,
                    task_id,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def _fail_task(self, task_id, error_message):
        """Mark the task as Failed."""
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                UPDATE agent_tasks
                SET status              = 'Failed',
                    completed_timestamp = ?,
                    error_message       = ?
                WHERE task_id = ?
                """,
                (datetime.now().isoformat(), error_message, task_id),
            )
            conn.commit()
        finally:
            conn.close()


# =============================================================================
# PRIVATE HELPERS
# =============================================================================

def _clean(value):
    """Strip whitespace from a string field; return None if empty."""
    if value is None:
        return None
    stripped = str(value).strip()
    return stripped if stripped else None


def _upper(value):
    """Strip and uppercase a string field (for state codes); return None if empty."""
    if value is None:
        return None
    stripped = str(value).strip().upper()
    return stripped if stripped else None


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys

    api_key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Usage: python terminal_capture_agent.py <ANTHROPIC_API_KEY>")
        sys.exit(1)

    agent = TerminalCaptureAgent(api_key)
    results = agent.capture_from_irs_510()
    print(json.dumps(results, indent=2))
