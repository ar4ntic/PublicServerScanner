"""Database operations for workers"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor, Json

logger = logging.getLogger(__name__)


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        dbname=os.getenv('DB_NAME', 'publicscanner'),
        cursor_factory=RealDictCursor
    )


def update_scan_status(scan_id: str, status: str, completed_at: Optional[datetime] = None):
    """Update scan job status"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                if completed_at:
                    cur.execute(
                        """
                        UPDATE scan_jobs
                        SET status = %s, completed_at = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (status, completed_at, scan_id)
                    )
                elif status == 'running':
                    cur.execute(
                        """
                        UPDATE scan_jobs
                        SET status = %s, started_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (status, scan_id)
                    )
                else:
                    cur.execute(
                        """
                        UPDATE scan_jobs
                        SET status = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (status, scan_id)
                    )
                conn.commit()
                logger.info(f"Updated scan {scan_id} status to {status}")
    except Exception as e:
        logger.error(f"Failed to update scan status: {e}")
        raise


def update_scan_progress(scan_id: str, progress: int):
    """Update scan progress percentage"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE scan_jobs
                    SET progress = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (progress, scan_id)
                )
                conn.commit()
                logger.debug(f"Updated scan {scan_id} progress to {progress}%")
    except Exception as e:
        logger.error(f"Failed to update scan progress: {e}")


def store_scan_result(
    scan_id: str,
    check_type: str,
    status: str,
    data: Dict[str, Any],
    findings: int = 0,
    severity: str = 'info'
):
    """Store scan check result"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO scan_results
                    (scan_id, check_type, status, data, findings, severity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (scan_id, check_type, status, Json(data), findings, severity)
                )
                conn.commit()
                logger.info(f"Stored {check_type} result for scan {scan_id}")
    except Exception as e:
        logger.error(f"Failed to store scan result: {e}")
        raise


def get_scan_config(scan_id: str) -> Optional[Dict[str, Any]]:
    """Get scan configuration"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT config FROM scan_jobs WHERE id = %s
                    """,
                    (scan_id,)
                )
                result = cur.fetchone()
                return result['config'] if result else None
    except Exception as e:
        logger.error(f"Failed to get scan config: {e}")
        return None
