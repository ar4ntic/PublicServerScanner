#!/usr/bin/env python3
"""
Directory brute force module for the Public Server Scanner Tool.

This module provides functions to discover hidden directories and files
on web servers using wordlists.
"""

import os
import logging
import re
from pathlib import Path

from app.utils import run_command, get_wordlist_path

logger = logging.getLogger(__name__)

def directory_bruteforce(target: str, output_dir: str) -> bool:
    """
    Run a directory brute force scan using gobuster.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Starting directory brute force scan on {target}")
    
    # Get the wordlist path
    wordlist = get_wordlist_path()
    logger.info(f"Using wordlist: {wordlist}")
    
    # Ensure the target has http:// or https:// prefix
    if not (target.startswith("http://") or target.startswith("https://")):
        target = f"http://{target}"
        logger.info(f"Added http:// prefix to target: {target}")
    
    # Output file
    output_file = os.path.join(output_dir, "directory_bruteforce.txt")
    
    # Run gobuster
    cmd = f"gobuster dir -u {target} -w {wordlist}"
    return run_command(cmd, output_file)