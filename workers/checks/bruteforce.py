"""Directory brute-force check module"""
import subprocess
import logging
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)


def bruteforce_check(target: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform directory/file brute-forcing using gobuster

    Args:
        target: Target hostname or IP
        config: Scan configuration

    Returns:
        Dictionary with check results
    """
    logger.info(f"Performing directory brute-force on {target}")

    try:
        # Add https:// if not present
        if not target.startswith(('http://', 'https://')):
            target = f"https://{target}"

        # Use a default wordlist or custom from config
        wordlist = config.get('custom_wordlist', '/usr/share/wordlists/dirb/common.txt')

        # Check if wordlist exists
        if not os.path.exists(wordlist):
            logger.warning(f"Wordlist not found: {wordlist}, using minimal list")
            # Create a minimal wordlist in memory
            wordlist = '/tmp/minimal_wordlist.txt'
            with open(wordlist, 'w') as f:
                f.write('\n'.join([
                    'admin', 'api', 'backup', 'config', 'dashboard',
                    'login', 'test', 'upload', '.git', '.env'
                ]))

        # Run gobuster
        command = [
            'gobuster', 'dir',
            '-u', target,
            '-w', wordlist,
            '-t', '10',  # 10 threads
            '-q',  # Quiet mode
            '--no-error',
            '--timeout', '30s'
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )

        # Parse gobuster output
        found_dirs = []
        for line in result.stdout.split('\n'):
            if line.strip() and not line.startswith('='):
                # Extract URL and status code
                parts = line.split()
                if len(parts) >= 2:
                    found_dirs.append({
                        'path': parts[0],
                        'status': parts[1] if len(parts) > 1 else 'unknown'
                    })

        findings_count = len(found_dirs)
        if findings_count > 20:
            severity = 'medium'
        elif findings_count > 10:
            severity = 'low'
        else:
            severity = 'info'

        return {
            'status': 'success',
            'data': {
                'directories_found': found_dirs,
                'total_found': findings_count,
                'wordlist_used': os.path.basename(wordlist)
            },
            'findings': findings_count,
            'severity': severity
        }

    except subprocess.TimeoutExpired:
        logger.error(f"Directory brute-force timed out for {target}")
        return {
            'status': 'failed',
            'data': {'error': 'Brute-force scan timed out'},
            'findings': 0,
            'severity': 'info'
        }
    except FileNotFoundError:
        logger.error("gobuster not found - please install gobuster")
        return {
            'status': 'failed',
            'data': {'error': 'gobuster not installed'},
            'findings': 0,
            'severity': 'info'
        }
    except Exception as e:
        logger.error(f"Directory brute-force failed for {target}: {e}")
        return {
            'status': 'failed',
            'data': {'error': str(e)},
            'findings': 0,
            'severity': 'info'
        }
