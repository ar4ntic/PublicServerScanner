"""DNS enumeration check module"""
import subprocess
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

DNS_RECORD_TYPES = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']


def dns_check(target: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform DNS enumeration

    Args:
        target: Target hostname or IP
        config: Scan configuration

    Returns:
        Dictionary with check results
    """
    logger.info(f"Performing DNS enumeration for {target}")

    try:
        # Remove protocol if present
        target = target.replace('https://', '').replace('http://', '').split('/')[0]

        records = {}
        findings_count = 0

        # Query each record type
        for record_type in DNS_RECORD_TYPES:
            try:
                command = ['dig', '+short', target, record_type]
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0 and result.stdout.strip():
                    record_values = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                    if record_values:
                        records[record_type] = record_values
                        findings_count += len(record_values)

            except subprocess.TimeoutExpired:
                logger.warning(f"DNS query for {record_type} timed out")
            except Exception as e:
                logger.warning(f"DNS query for {record_type} failed: {e}")

        # Test for zone transfer vulnerability
        zone_transfer_vulnerable = False
        try:
            command = ['dig', 'axfr', f"@{target}", target]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and 'Transfer failed' not in result.stdout:
                zone_transfer_vulnerable = True
                findings_count += 1

        except Exception as e:
            logger.warning(f"Zone transfer test failed: {e}")

        severity = 'high' if zone_transfer_vulnerable else 'info'

        return {
            'status': 'success',
            'data': {
                'records': records,
                'zone_transfer_vulnerable': zone_transfer_vulnerable,
                'total_records': findings_count
            },
            'findings': findings_count,
            'severity': severity
        }

    except Exception as e:
        logger.error(f"DNS check failed for {target}: {e}")
        return {
            'status': 'failed',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }
