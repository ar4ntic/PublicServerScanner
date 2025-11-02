#!/usr/bin/env python3
"""
DNS enumeration module for the Public Server Scanner Tool.

This module provides functions to perform DNS enumeration on target domains.
"""

import os
import logging
from pathlib import Path

from app.utils import run_command

logger = logging.getLogger(__name__)

def dns_enumeration(target: str, output_dir: str) -> bool:
    """
    Run DNS enumeration using dig.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Starting DNS enumeration for {target}")
    
    # Remove protocol prefix if present
    target = target.replace("http://", "").replace("https://", "")
    
    # Remove path and query parameters
    if "/" in target:
        target = target.split("/")[0]
        
    output_file = os.path.join(output_dir, "dns_enumeration.txt")
    
    # Combine multiple DNS queries into a single report
    commands = [
        f"echo '# Basic DNS lookup' > {output_file}",
        f"dig {target} >> {output_file}",
        f"echo '\n# DNS A records' >> {output_file}",
        f"dig A {target} >> {output_file}",
        f"echo '\n# DNS MX records' >> {output_file}",
        f"dig MX {target} >> {output_file}",
        f"echo '\n# DNS NS records' >> {output_file}",
        f"dig NS {target} >> {output_file}",
        f"echo '\n# DNS TXT records' >> {output_file}",
        f"dig TXT {target} >> {output_file}",
        f"echo '\n# Zone transfer attempt' >> {output_file}",
        f"dig AXFR {target} 2>/dev/null >> {output_file} || echo 'Zone transfer refused or failed' >> {output_file}"
    ]
    
    # Execute all commands
    combined_cmd = " && ".join(commands)
    return run_command(combined_cmd, output_file)