"""Celery tasks for security scans"""
import os
import json
import logging
from datetime import datetime
from celery import Task
from celery_app import app
from database import update_scan_status, update_scan_progress, store_scan_result
from checks import (
    ping_check,
    port_scan_check,
    headers_check,
    ssl_check,
    dns_check,
    bruteforce_check,
)

logger = logging.getLogger(__name__)


class ScanTask(Task):
    """Base task class with common functionality"""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        scan_id = kwargs.get('scan_id')
        if scan_id:
            update_scan_status(scan_id, 'failed')
            logger.error(f"Scan {scan_id} failed: {exc}")

    def on_success(self, retval, task_id, args, kwargs):
        """Handle task success"""
        scan_id = kwargs.get('scan_id')
        if scan_id:
            logger.info(f"Scan {scan_id} completed successfully")


@app.task(base=ScanTask, bind=True, name='tasks.execute_scan')
def execute_scan(self, scan_id: str, target: str, checks: list, config: dict):
    """
    Execute a complete security scan

    Args:
        scan_id: UUID of the scan job
        target: Target hostname or IP
        checks: List of checks to run
        config: Scan configuration
    """
    logger.info(f"Starting scan {scan_id} for target {target}")

    try:
        # Update status to running
        update_scan_status(scan_id, 'running')
        update_scan_progress(scan_id, 0)

        total_checks = len(checks)
        completed_checks = 0

        # Execute each check
        check_functions = {
            'ping': ping_check,
            'portscan': port_scan_check,
            'headers': headers_check,
            'ssl': ssl_check,
            'dns': dns_check,
            'bruteforce': bruteforce_check,
        }

        for check_name in checks:
            if check_name not in check_functions:
                logger.warning(f"Unknown check: {check_name}")
                continue

            logger.info(f"Running {check_name} check for {target}")

            try:
                # Execute the check
                result = check_functions[check_name](target, config)

                # Store result in database
                store_scan_result(
                    scan_id=scan_id,
                    check_type=check_name,
                    status='success',
                    data=result.get('data', {}),
                    findings=result.get('findings', 0),
                    severity=result.get('severity', 'info')
                )

                logger.info(f"{check_name} check completed for {target}")

            except Exception as e:
                logger.error(f"{check_name} check failed for {target}: {e}")
                store_scan_result(
                    scan_id=scan_id,
                    check_type=check_name,
                    status='failed',
                    data={'error': str(e)},
                    findings=0,
                    severity='info'
                )

            # Update progress
            completed_checks += 1
            progress = int((completed_checks / total_checks) * 100)
            update_scan_progress(scan_id, progress)

        # Mark scan as completed
        update_scan_status(scan_id, 'completed', datetime.utcnow())
        update_scan_progress(scan_id, 100)

        logger.info(f"Scan {scan_id} completed successfully")

        return {
            'scan_id': scan_id,
            'status': 'completed',
            'checks_completed': completed_checks,
            'checks_total': total_checks
        }

    except Exception as e:
        logger.error(f"Scan {scan_id} failed: {e}")
        update_scan_status(scan_id, 'failed')
        raise


@app.task(name='tasks.test_connection')
def test_connection():
    """Test task to verify Celery is working"""
    return {
        'status': 'ok',
        'message': 'Celery is working!',
        'timestamp': datetime.utcnow().isoformat()
    }


@app.task(name='tasks.cleanup_old_scans')
def cleanup_old_scans():
    """Cleanup old scan data (scheduled task)"""
    logger.info("Running cleanup task")
    # TODO: Implement cleanup logic
    # - Delete scans older than X days
    # - Delete old reports
    # - Clean up temp files
    pass
