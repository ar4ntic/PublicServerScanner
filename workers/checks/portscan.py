"""Port scanning module using nmap"""
import subprocess
import xml.etree.ElementTree as ET
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def port_scan_check(target: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform port scanning using nmap

    Args:
        target: Target hostname or IP
        config: Scan configuration

    Returns:
        Dictionary with check results
    """
    logger.info(f"Performing port scan on {target}")

    try:
        # Basic nmap command (can be configured later)
        command = [
            'nmap',
            '-p-',  # Scan all ports
            '--open',  # Only show open ports
            '-T4',  # Faster timing
            '-oX', '-',  # XML output to stdout
            target
        ]

        # Execute nmap
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=900  # 15 minutes timeout
        )

        if result.returncode != 0:
            return {
                'status': 'failed',
                'data': {'error': 'nmap scan failed', 'stderr': result.stderr},
                'findings': 0,
                'severity': 'info'
            }

        # Parse XML output
        try:
            root = ET.fromstring(result.stdout)
            ports = []

            for port in root.findall('.//port'):
                state = port.find('state')
                if state is not None and state.get('state') == 'open':
                    port_id = port.get('portid')
                    protocol = port.get('protocol')
                    service = port.find('service')
                    service_name = service.get('name', 'unknown') if service is not None else 'unknown'

                    ports.append({
                        'port': int(port_id),
                        'protocol': protocol,
                        'service': service_name,
                        'state': 'open'
                    })

            # Determine severity based on number of open ports
            findings_count = len(ports)
            if findings_count > 20:
                severity = 'high'
            elif findings_count > 10:
                severity = 'medium'
            else:
                severity = 'low'

            return {
                'status': 'success',
                'data': {
                    'open_ports': ports,
                    'total_open': findings_count,
                    'scan_completed': True
                },
                'findings': findings_count,
                'severity': severity
            }

        except ET.ParseError as e:
            logger.error(f"Failed to parse nmap XML output: {e}")
            return {
                'status': 'failed',
                'data': {'error': 'Failed to parse nmap output'},
                'findings': 0,
                'severity': 'info'
            }

    except subprocess.TimeoutExpired:
        logger.error(f"Port scan timed out for {target}")
        return {
            'status': 'failed',
            'data': {'error': 'Port scan timed out'},
            'findings': 0,
            'severity': 'info'
        }
    except FileNotFoundError:
        logger.error("nmap not found - please install nmap")
        return {
            'status': 'failed',
            'data': {'error': 'nmap not installed'},
            'findings': 0,
            'severity': 'info'
        }
    except Exception as e:
        logger.error(f"Port scan failed for {target}: {e}")
        return {
            'status': 'failed',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }
