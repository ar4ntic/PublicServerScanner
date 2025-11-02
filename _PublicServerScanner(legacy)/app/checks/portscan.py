#!/usr/bin/env python3
"""
Port scanning module for the Public Server Scanner Tool.

This module provides functions to scan for open ports and identify services.
"""

import os
import logging
import subprocess
from pathlib import Path

from app.utils import run_command
from app.config import Config

logger = logging.getLogger(__name__)

def port_scan(target: str, output_dir: str) -> bool:
    """
    Run a comprehensive port scan on the target.
    This includes both TCP and UDP scans with service detection.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Starting port scan on target: {target}")
    
    # Load configuration for nmap options
    config = Config()
    
    # Full TCP port scan
    tcp_success = tcp_port_scan(target, output_dir, config.get("nmap.tcp_options"))
    
    # Service version detection
    service_success = service_version_scan(target, output_dir, config.get("nmap.service_options"))
    
    # UDP port scan (optional as it's slower)
    udp_success = udp_port_scan(target, output_dir, config.get("nmap.udp_options"))
    
    return tcp_success and service_success  # UDP scan is optional for success

def tcp_port_scan(target: str, output_dir: str, options: str = "-sS -Pn -p-") -> bool:
    """
    Run a TCP port scan using nmap.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        options (str): Nmap TCP scan options
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Running TCP port scan on {target}")
    output_file = os.path.join(output_dir, "tcp_port_scan.txt")
    return run_command(f"nmap {options} {target}", output_file)

def service_version_scan(target: str, output_dir: str, options: str = "-sV -sC -p22,80,443") -> bool:
    """
    Run a service version scan using nmap.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        options (str): Nmap service scan options
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Running service version scan on {target}")
    output_file = os.path.join(output_dir, "service_version_scan.txt")
    return run_command(f"nmap {options} {target}", output_file)

def udp_port_scan(target: str, output_dir: str, options: str = "-sU --top-ports 100") -> bool:
    """
    Run a UDP port scan using nmap.
    
    Args:
        target (str): Target hostname or IP address
        output_dir (str): Directory to save output file
        options (str): Nmap UDP scan options
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Running UDP port scan on {target}")
    output_file = os.path.join(output_dir, "udp_port_scan.txt")
    return run_command(f"nmap {options} {target}", output_file)