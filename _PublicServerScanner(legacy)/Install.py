#!/usr/bin/env python3
"""
Public Server Scanner - Installation Script

This script installs and configures all dependencies required by the Public Server Scanner Tool,
setting up the per-user installation directory structure.

Usage:
    python Install.py [--no-venv] [--skip-wordlists]
"""

import argparse
import logging
import sys
from pathlib import Path

# Configure basic logging for standalone use
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("installation.log")
    ]
)
logger = logging.getLogger("Installer")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Public Server Scanner Tool - Installer")
    parser.add_argument("--no-venv", action="store_true", 
                      help="Skip virtual environment creation")
    parser.add_argument("--skip-wordlists", action="store_true", 
                      help="Skip downloading wordlists")
    parser.add_argument("--interactive", "-i", action="store_true", 
                      help="Run in interactive mode with prompts")
    return parser.parse_args()

def main():
    """Main installation function."""
    args = parse_args()
    
    try:
        # Use relative import when run as script
        from app.installer import run_installation
        
        logger.info("Starting Public Server Scanner Tool installation...")
        success = run_installation(
            no_venv=args.no_venv,
            skip_wordlists=args.skip_wordlists
        )
        
        if success:
            logger.info("Installation completed successfully!")
            print("\n" + "=" * 60)
            print("INSTALLATION COMPLETE".center(60))
            print("=" * 60)
            print("\nAll dependencies have been successfully installed!")
            print("\nNext steps:")
            print("1. Run the Public Server Scanner Tool with:")
            print("   python StartScan.py [--target example.com]")
            print("\nIf you encounter any issues, check installation.log for details.")
            print("=" * 60 + "\n")
            return 0
        else:
            logger.error("Installation failed. Please check the logs for details.")
            print("\n" + "=" * 60)
            print("INSTALLATION INCOMPLETE".center(60))
            print("=" * 60)
            print("\nSome components could not be installed automatically.")
            print("Please check installation.log for details and error messages.")
            print("\nTroubleshooting steps:")
            print("1. Ensure you have administrator/sudo privileges")
            print("2. Check your internet connection")
            print("3. Manually install any missing dependencies")
            print("\nAfter resolving issues, try running the installer again:")
            print("   python Install.py")
            print("=" * 60 + "\n")
            return 1
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.error("This could indicate that the package structure is incorrect.")
        print("\nERROR: Failed to import the required modules.")
        print("Make sure all files are in the correct directories.")
        return 1
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        print(f"\nAn unexpected error occurred: {e}")
        print("Check installation.log for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())