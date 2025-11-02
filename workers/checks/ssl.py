"""SSL/TLS certificate check module"""
import subprocess
import re
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def ssl_check(target: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check SSL/TLS certificate

    Args:
        target: Target hostname or IP
        config: Scan configuration

    Returns:
        Dictionary with check results
    """
    logger.info(f"Checking SSL/TLS certificate for {target}")

    try:
        # Remove protocol if present
        target = target.replace('https://', '').replace('http://', '').split('/')[0]

        # Use openssl to get certificate info
        command = [
            'openssl', 's_client',
            '-connect', f"{target}:443",
            '-servername', target,
            '-showcerts'
        ]

        # Echo quit to close the connection
        echo_process = subprocess.Popen(['echo', 'Q'], stdout=subprocess.PIPE)
        result = subprocess.run(
            command,
            stdin=echo_process.stdout,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0 and not result.stdout:
            return {
                'status': 'failed',
                'data': {'error': 'Failed to connect to SSL/TLS server'},
                'findings': 1,
                'severity': 'high'
            }

        output = result.stdout

        # Parse certificate information
        cert_data = {}
        findings = []
        severity = 'info'

        # Extract issuer
        issuer_match = re.search(r'issuer=(.+)', output)
        if issuer_match:
            cert_data['issuer'] = issuer_match.group(1).strip()

        # Extract subject
        subject_match = re.search(r'subject=(.+)', output)
        if subject_match:
            cert_data['subject'] = subject_match.group(1).strip()

        # Extract validity dates
        not_before_match = re.search(r'notBefore=(.+)', output)
        not_after_match = re.search(r'notAfter=(.+)', output)

        if not_after_match:
            cert_data['expires'] = not_after_match.group(1).strip()
            # TODO: Calculate days until expiry and add to findings if < 30 days

        # Check for certificate issues
        if 'verify error' in output.lower():
            findings.append('Certificate verification error')
            severity = 'high'
        if 'self signed' in output.lower():
            findings.append('Self-signed certificate')
            severity = 'medium'

        return {
            'status': 'success',
            'data': {
                'certificate': cert_data,
                'issues': findings,
                'has_ssl': True
            },
            'findings': len(findings),
            'severity': severity
        }

    except subprocess.TimeoutExpired:
        logger.error(f"SSL check timed out for {target}")
        return {
            'status': 'failed',
            'data': {'error': 'SSL check timed out'},
            'findings': 0,
            'severity': 'info'
        }
    except Exception as e:
        logger.error(f"SSL check failed for {target}: {e}")
        return {
            'status': 'failed',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }
