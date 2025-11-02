#!/usr/bin/env python3
"""
Certificate analysis module for the Public Server Scanner Tool.

This module provides functions to analyze SSL/TLS certificates.
"""

import os
import re
import logging
from pathlib import Path

from app.utils import run_command

logger = logging.getLogger(__name__)

def certificate_details(target: str, output_dir: str) -> bool:
    """
    Get SSL/TLS certificate details using openssl.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Getting certificate details for {target}")
    
    # Strip http:// or https:// from the target for openssl
    target = re.sub(r'^https?://', '', target)
    
    # Remove path and query parameters
    if "/" in target:
        target = target.split("/")[0]
    
    # Add default port if not specified
    if ":" not in target:
        target = f"{target}:443"
    
    output_file = os.path.join(output_dir, "certificate_details.txt")
    
    # Combine multiple certificate checks into a single report
    commands = [
        f"echo '# Certificate Details' > {output_file}",
        f"echo | openssl s_client -connect {target} | openssl x509 -noout -text >> {output_file} 2>/dev/null || echo 'Failed to retrieve certificate' >> {output_file}",
        f"echo '\n# Certificate Expiry' >> {output_file}",
        f"echo | openssl s_client -connect {target} | openssl x509 -noout -dates >> {output_file} 2>/dev/null || echo 'Failed to check expiry' >> {output_file}",
        f"echo '\n# Certificate Chain' >> {output_file}",
        f"echo | openssl s_client -connect {target} -showcerts >> {output_file} 2>/dev/null || echo 'Failed to retrieve certificate chain' >> {output_file}"
    ]
    
    # Execute all commands
    combined_cmd = " && ".join(commands)
    return run_command(combined_cmd, output_file)