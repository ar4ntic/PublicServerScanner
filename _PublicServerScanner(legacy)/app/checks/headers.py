#!/usr/bin/env python3
"""
HTTP Headers analysis module for the Public Server Scanner Tool.

This module provides functions to analyze HTTP response headers for security issues.
"""

import os
import logging
import re
from pathlib import Path

from app.utils import run_command

logger = logging.getLogger(__name__)

def gather_headers(target: str, output_dir: str) -> bool:
    """
    Fetch and analyze HTTP response headers using curl.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Fetching HTTP headers for {target}")
    
    # Ensure target has correct protocol
    if not (target.startswith("http://") or target.startswith("https://")):
        target = f"http://{target}"
    
    output_file = os.path.join(output_dir, "http_headers.txt")
    
    # Combine multiple header checks into a single report
    commands = [
        f"echo '# HTTP Headers (Default)' > {output_file}",
        f"curl -sSL -D - {target} -o /dev/null >> {output_file} 2>/dev/null || echo 'Failed to retrieve headers' >> {output_file}",
        f"echo '\n# HTTP Headers (with User-Agent)' >> {output_file}",
        f"curl -sSL -D - -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' {target} -o /dev/null >> {output_file} 2>/dev/null",
        f"echo '\n# Security Headers Analysis' >> {output_file}",
        f"echo 'Checking for important security headers:' >> {output_file}",
        f"curl -sSL -D - {target} -o /dev/null 2>/dev/null | grep -iE 'strict-transport-security|content-security-policy|x-xss-protection|x-content-type-options|x-frame-options|referrer-policy' >> {output_file} || echo 'No standard security headers found' >> {output_file}",
        f"echo '\n# Server Information' >> {output_file}",
        f"curl -sSL -D - {target} -o /dev/null 2>/dev/null | grep -i 'server:' >> {output_file} || echo 'No server header found' >> {output_file}"
    ]
    
    # Execute all commands
    combined_cmd = " && ".join(commands)
    return run_command(combined_cmd, output_file)