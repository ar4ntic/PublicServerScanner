"""Ping/availability check module"""
import subprocess
import platform
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def ping_check(target: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform ping check to verify target availability

    Args:
        target: Target hostname or IP
        config: Scan configuration

    Returns:
        Dictionary with check results
    """
    logger.info(f"Performing ping check on {target}")

    try:
        # Determine the ping command based on OS
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', target]

        # Execute ping command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout

        # Parse ping results
        if result.returncode == 0:
            # Extract response time (platform-specific parsing)
            response_time = None
            packet_loss = 0

            if platform.system().lower() == 'windows':
                time_match = re.search(r'Average = (\d+)ms', output)
                loss_match = re.search(r'\((\d+)% loss\)', output)
            else:
                time_match = re.search(r'avg = ([\d.]+)', output) or \
                           re.search(r'avg/([\d.]+)', output)
                loss_match = re.search(r'(\d+)% packet loss', output)

            if time_match:
                response_time = float(time_match.group(1))
            if loss_match:
                packet_loss = int(loss_match.group(1))

            return {
                'status': 'success',
                'data': {
                    'reachable': True,
                    'response_time_ms': response_time,
                    'packet_loss_percent': packet_loss,
                    'raw_output': output
                },
                'findings': 0,
                'severity': 'info'
            }
        else:
            return {
                'status': 'success',
                'data': {
                    'reachable': False,
                    'error': 'Target is not reachable',
                    'raw_output': output
                },
                'findings': 1,
                'severity': 'high'
            }

    except subprocess.TimeoutExpired:
        logger.error(f"Ping check timed out for {target}")
        return {
            'status': 'failed',
            'data': {'error': 'Ping check timed out'},
            'findings': 1,
            'severity': 'medium'
        }
    except Exception as e:
        logger.error(f"Ping check failed for {target}: {e}")
        return {
            'status': 'failed',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }
