#!/usr/bin/env python3
"""
Ping check module for the Public Server Scanner Tool.

This module provides functions to ping targets to verify reachability.
"""

import os
import platform
import logging
from pathlib import Path

from app.utils import run_command

logger = logging.getLogger(__name__)

def ping_target(target: str, output_dir: str) -> bool:
    """
    Ping a target to check if it's reachable.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Pinging target: {target}")
    
    # Different ping command options based on OS
    system = platform.system().lower()
    if system == "windows":
        ping_cmd = f"ping -n 4 {target}"
    elif system == "darwin":  # macOS
        ping_cmd = f"ping -c 4 {target}"
    else:  # Linux and others
        ping_cmd = f"ping -c 4 {target}"
    
    output_file = os.path.join(output_dir, "ping.txt")
    
    # Run the ping command
    return run_command(ping_cmd, output_file)