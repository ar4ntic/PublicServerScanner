#!/usr/bin/env python3
"""
Public Server Scanner Tool - Main Execution Script

This script serves as the main entry point for running security scans on target servers.
It provides both command-line and GUI interfaces using the refactored package structure.

Usage:
    python StartScan.py [--target example.com] [--checks ping port_scan] [--gui] [--headless]
"""

import sys
import logging

# Configure basic logging for standalone use
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function."""
    try:
        # Import the CLI module to handle command-line arguments
        from app.cli import parse_args, main as cli_main
        
        # Just call the main function from cli.py
        return cli_main()
        
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("This could indicate that installation is incomplete or the package structure is incorrect.")
        print("\nERROR: Failed to import the required modules.")
        print("Make sure all files are in the correct directories and run the installer first:")
        print("   python Install.py")
        return 1
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        print(f"\nAn unexpected error occurred: {e}")
        print("Check the logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())