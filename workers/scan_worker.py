#!/usr/bin/env python3
"""
Scan Worker - Polls database for queued scans and executes them
"""
import os
import sys
import time
import json
import psycopg2
from datetime import datetime

# Ensure output is not buffered
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from checks.ping import ping_check
from checks.portscan import port_scan_check
from checks.headers import headers_check
from checks.ssl import ssl_check
from checks.dns import dns_check
from checks.bruteforce import bruteforce_check


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        dbname=os.getenv("DB_NAME", "publicscanner")
    )


def get_queued_scans(conn):
    """Fetch queued scans from database"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, target_id, url, checks, organization_id
            FROM scan_jobs
            WHERE status = 'queued'
            ORDER BY created_at ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        """)
        return cur.fetchone()


def update_scan_status(conn, scan_id, status, progress=None):
    """Update scan status"""
    with conn.cursor() as cur:
        if status == 'running':
            cur.execute("""
                UPDATE scan_jobs
                SET status = %s, progress = %s, started_at = NOW()
                WHERE id = %s
            """, (status, progress or 0, scan_id))
        elif status == 'completed':
            cur.execute("""
                UPDATE scan_jobs
                SET status = %s, progress = 100, completed_at = NOW()
                WHERE id = %s
            """, (status, scan_id))
        elif status == 'failed':
            cur.execute("""
                UPDATE scan_jobs
                SET status = %s, completed_at = NOW()
                WHERE id = %s
            """, (status, scan_id))
        else:
            cur.execute("""
                UPDATE scan_jobs
                SET status = %s, progress = %s
                WHERE id = %s
            """, (status, progress or 0, scan_id))
        conn.commit()


def save_scan_result(conn, scan_id, check_type, status, data, findings, severity):
    """Save scan result to database"""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO scan_results (id, scan_id, check_type, status, data, findings, severity)
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)
        """, (scan_id, check_type, status, json.dumps(data), findings, severity))
        conn.commit()


def execute_check(check_name, target):
    """Execute a specific security check"""
    check_map = {
        'ping': ping_check,
        'portscan': port_scan_check,
        'headers': headers_check,
        'ssl': ssl_check,
        'dns': dns_check,
        'bruteforce': bruteforce_check,
    }

    check_func = check_map.get(check_name)
    if not check_func:
        return {
            'status': 'error',
            'data': {'error': f'Unknown check: {check_name}'},
            'findings': 0,
            'severity': 'info'
        }

    try:
        result = check_func(target, {})
        return result
    except Exception as e:
        return {
            'status': 'error',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }


def process_scan(conn, scan_data):
    """Process a single scan"""
    scan_id, target_id, url, checks, org_id = scan_data

    # Determine target URL
    if url:
        target = url
    else:
        # Fetch target from database
        with conn.cursor() as cur:
            cur.execute("SELECT hostname FROM targets WHERE id = %s", (target_id,))
            result = cur.fetchone()
            if not result:
                print(f"❌ Target not found for scan {scan_id}")
                update_scan_status(conn, scan_id, 'failed')
                return
            target = result[0]

    print(f"🔍 Processing scan {scan_id} for {target}")
    update_scan_status(conn, scan_id, 'running', 0)

    # Execute each check
    total_checks = len(checks)
    for i, check_name in enumerate(checks):
        print(f"  ➤ Running {check_name} check...")

        result = execute_check(check_name, target)

        # Save result
        save_scan_result(
            conn,
            scan_id,
            check_name,
            result.get('status', 'success'),
            result.get('data', {}),
            result.get('findings', 0),
            result.get('severity', 'info')
        )

        # Update progress
        progress = int(((i + 1) / total_checks) * 100)
        update_scan_status(conn, scan_id, 'running', progress)

    # Mark as completed
    update_scan_status(conn, scan_id, 'completed')
    print(f"✅ Scan {scan_id} completed")


def main():
    """Main worker loop"""
    print("🚀 Scan worker started")
    print("📊 Polling database for queued scans...")

    while True:
        try:
            conn = get_db_connection()

            # Check for queued scans
            scan_data = get_queued_scans(conn)

            if scan_data:
                process_scan(conn, scan_data)
            else:
                # No scans, wait before checking again
                time.sleep(5)

            conn.close()

        except KeyboardInterrupt:
            print("\n🛑 Worker stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    main()
