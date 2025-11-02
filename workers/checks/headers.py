"""HTTP security headers check module"""
import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Security headers to check
SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'X-XSS-Protection',
    'Referrer-Policy',
    'Permissions-Policy',
]


def headers_check(target: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check HTTP security headers

    Args:
        target: Target hostname or IP
        config: Scan configuration

    Returns:
        Dictionary with check results
    """
    logger.info(f"Checking HTTP headers for {target}")

    try:
        # Add https:// if not present
        if not target.startswith(('http://', 'https://')):
            target = f"https://{target}"

        # Use curl to fetch headers
        command = ['curl', '-I', '-s', '-L', '--max-time', '10', target]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            return {
                'status': 'failed',
                'data': {'error': 'Failed to fetch headers'},
                'findings': 0,
                'severity': 'info'
            }

        headers = {}
        missing_headers = []

        # Parse headers
        for line in result.stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()

        # Check for security headers
        for header in SECURITY_HEADERS:
            if header not in headers:
                missing_headers.append(header)

        findings_count = len(missing_headers)
        if findings_count >= 5:
            severity = 'high'
        elif findings_count >= 3:
            severity = 'medium'
        elif findings_count > 0:
            severity = 'low'
        else:
            severity = 'info'

        return {
            'status': 'success',
            'data': {
                'headers_present': headers,
                'missing_headers': missing_headers,
                'server': headers.get('Server', 'unknown')
            },
            'findings': findings_count,
            'severity': severity
        }

    except subprocess.TimeoutExpired:
        logger.error(f"Headers check timed out for {target}")
        return {
            'status': 'failed',
            'data': {'error': 'Request timed out'},
            'findings': 0,
            'severity': 'info'
        }
    except Exception as e:
        logger.error(f"Headers check failed for {target}: {e}")
        return {
            'status': 'failed',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }
