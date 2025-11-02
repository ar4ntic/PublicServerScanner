#!/usr/bin/env python3
"""
Command-line interface for the Public Server Scanner Tool.

This module parses command-line arguments and calls the main functionality
in core.py to run security scans.
"""

import argparse
import logging
import sys
from typing import List, Optional

from app.core import run
from app.constants import APP_NAME, APP_VERSION, APP_YEAR, APP_AUTHOR
from app.installer import run_installation

# Initialize logger
logger = logging.getLogger(__name__)

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args (List[str], optional): Command-line arguments. If None, sys.argv is used.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{APP_VERSION} - A comprehensive security scanning tool for public-facing servers."
    )
    
    parser.add_argument("--target", "-t", help="Target hostname or IP address")
    parser.add_argument(
        "--checks", "-c", 
        nargs="+", 
        help="Specific checks to run (ping, port_scan, bruteforce, dns, cert, headers)"
    )
    parser.add_argument(
        "--gui", "-g", 
        action="store_true", 
        help="Run with GUI progress display"
    )
    parser.add_argument(
        "--headless", 
        action="store_true", 
        help="Force headless mode (no GUI)"
    )
    parser.add_argument(
        "--version", "-v", 
        action="store_true", 
        help="Show version information"
    )
    parser.add_argument(
        "--install", "-i", 
        action="store_true", 
        help="Run the installer before starting the scan"
    )
    parser.add_argument(
        "--no-venv", 
        action="store_true", 
        help="Skip virtual environment creation during installation"
    )
    parser.add_argument(
        "--skip-wordlists", 
        action="store_true", 
        help="Skip downloading wordlists during installation"
    )
    
    return parser.parse_args(args)

def show_version():
    """Display the version information."""
    print(f"{APP_NAME} version {APP_VERSION}")
    print(f"© {APP_YEAR} {APP_AUTHOR}")

def main():
    """Main entry point for the CLI application."""
    # Parse command-line arguments
    args = parse_args()
    
    # Show version if requested
    if args.version:
        show_version()
        return 0
    
    # Run the installer if requested
    if args.install:
        success = run_installation(
            no_venv=args.no_venv,
            skip_wordlists=args.skip_wordlists
        )
        if not success:
            logger.error("Installation failed. Please check the logs for details.")
            return 1
        logger.info("Installation completed successfully.")
    
    # Force headless mode if requested
    if args.headless:
        args.gui = False
    
    # Run the security scan
    success = run(args)
    
    # Return exit code based on success
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())