#!/usr/bin/env python3
"""
Installer module for the Public Server Scanner Tool.

This module handles creating the per-user installation directory structure,
setting up virtual environments, and downloading wordlists.
"""

import os
import sys
import shutil
import subprocess
import logging
import json
import venv
import platform
from pathlib import Path

from app.constants import (
    APP_DIR,
    VENV_DIR,
    WORDLISTS_DIR,
    LOGS_DIR,
    CONFIG_PATH,
    SECLISTS_REPO_URL
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Installer")

def setup_directory_structure(config=None):
    """
    Create the per-user directory structure for the application.
    
    Args:
        config (dict, optional): Configuration dictionary with custom paths.
    
    Returns:
        bool: True if setup was successful, False otherwise.
    """
    try:
        # Create main app directory
        APP_DIR.mkdir(exist_ok=True)
        logger.info(f"Created application directory: {APP_DIR}")
        
        # Create subdirectories
        VENV_DIR.mkdir(exist_ok=True)
        WORDLISTS_DIR.mkdir(exist_ok=True)
        LOGS_DIR.mkdir(exist_ok=True)
        
        # Create default config if it doesn't exist
        if not CONFIG_PATH.exists():
            default_config = {
                "wordlists": {
                    "dirb_common": str(WORDLISTS_DIR / "common.txt"),
                    "seclists_common": str(WORDLISTS_DIR / "SecLists" / "Discovery" / "Web-Content" / "common.txt"),
                    "seclists_big": str(WORDLISTS_DIR / "SecLists" / "Discovery" / "Web-Content" / "big.txt"),
                    "selected": "default",
                    "custom_path": "",
                },
                "nmap": {
                    "tcp_options": "-sS -Pn -p-",
                    "service_options": "-sV -sC -p22,80,443",
                    "udp_options": "-sU --top-ports 100"
                },
                "timeout": 3600,
                "scan_threads": 1,
                "advanced_mode": False
            }
            
            with open(CONFIG_PATH, 'w') as f:
                json.dump(default_config, f, indent=4)
            logger.info(f"Created default configuration at: {CONFIG_PATH}")
        
        logger.info("Per-user directory structure setup complete")
        return True
    except Exception as e:
        logger.error(f"Error creating directory structure: {e}")
        return False

def setup_virtual_environment(no_venv=False):
    """
    Create and configure a virtual environment for the application.
    
    Args:
        no_venv (bool): If True, skip virtual environment creation.
    
    Returns:
        bool: True if setup was successful or skipped, False otherwise.
    """
    if no_venv:
        logger.info("Skipping virtual environment setup (--no-venv flag)")
        return True
    
    # Check if we're already in a virtual environment
    if sys.prefix != sys.base_prefix:
        logger.info(f"Already in a virtual environment: {sys.prefix}")
        return True
    
    try:
        logger.info(f"Creating virtual environment in {VENV_DIR}")
        venv.create(VENV_DIR, with_pip=True)
        
        # Get the path to the Python executable in the virtual environment
        if platform.system() == "Windows":
            venv_python = VENV_DIR / "Scripts" / "python.exe"
            activate_script = VENV_DIR / "Scripts" / "activate"
        else:
            venv_python = VENV_DIR / "bin" / "python"
            activate_script = VENV_DIR / "bin" / "activate"
        
        # Verify the Python executable exists
        if not venv_python.exists():
            logger.error(f"Virtual environment Python not found at: {venv_python}")
            return False
        
        # Install required packages in the virtual environment
        logger.info("Installing required packages in the virtual environment")
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "gitpython"],
            check=True
        )
        
        logger.info(f"Virtual environment created at: {VENV_DIR}")
        logger.info(f"To activate, run: source {activate_script}")
        return True
    except Exception as e:
        logger.error(f"Failed to set up virtual environment: {e}")
        return False

def download_wordlists(skip_wordlists=False):
    """
    Download wordlists for use with the Public Server Scanner tool.
    
    Args:
        skip_wordlists (bool): If True, skip downloading wordlists.
    
    Returns:
        bool: True if download was successful or skipped, False otherwise.
    """
    if skip_wordlists:
        logger.info("Skipping wordlists download (--skip-wordlists flag)")
        return create_default_wordlist()
    
    try:
        # Check if git is available
        if not shutil.which("git"):
            logger.error("Git is not installed. Cannot download SecLists.")
            return create_default_wordlist()
        
        seclists_dir = WORDLISTS_DIR / "SecLists"
        
        if seclists_dir.exists():
            logger.info("Updating existing SecLists repository...")
            try:
                subprocess.run(
                    ["git", "-C", str(seclists_dir), "pull"],
                    check=True
                )
                logger.info("SecLists updated successfully")
                return True
            except subprocess.CalledProcessError:
                logger.warning("Failed to update SecLists. Will try a fresh clone.")
                shutil.rmtree(seclists_dir, ignore_errors=True)
        
        # Clone with sparse checkout for selected directories
        logger.info(f"Cloning SecLists from {SECLISTS_REPO_URL}")
        
        # Initialize the repository
        seclists_dir.mkdir(exist_ok=True)
        subprocess.run(["git", "init"], cwd=str(seclists_dir), check=True)
        subprocess.run(
            ["git", "remote", "add", "origin", SECLISTS_REPO_URL],
            cwd=str(seclists_dir),
            check=True
        )
        
        # Set up sparse checkout for Discovery/Web-Content and Fuzzing directories
        subprocess.run(
            ["git", "config", "core.sparseCheckout", "true"],
            cwd=str(seclists_dir),
            check=True
        )
        
        sparse_file = seclists_dir / ".git" / "info" / "sparse-checkout"
        sparse_file.parent.mkdir(exist_ok=True)
        
        with open(sparse_file, "w") as f:
            f.write("README.md\n")
            f.write("LICENSE\n")
            f.write("Discovery/Web-Content/**\n")
            f.write("Fuzzing/**\n")
        
        # Pull only the specified directories
        subprocess.run(
            ["git", "pull", "--depth=1", "origin", "master"],
            cwd=str(seclists_dir),
            check=True
        )
        
        logger.info("SecLists repository cloned successfully with selected directories")
        return True
    except Exception as e:
        logger.error(f"Error downloading wordlists: {e}")
        return create_default_wordlist()

def create_default_wordlist():
    """
    Create a minimal default wordlist if SecLists download fails.
    
    Returns:
        bool: True if creation was successful, False otherwise.
    """
    try:
        wordlist_path = WORDLISTS_DIR / "common.txt"
        
        # Common web directories and files for the minimal wordlist
        common_paths = [
            "admin", "login", "wp-admin", "dashboard", "images", "img",
            "css", "js", "api", "uploads", "config", "backup", "dev",
            "test", "webmail", "mail", "static", "media", "docs", "files",
            "assets", "includes", "lib", "scripts", "cgi-bin", "temp", "data",
            "logs", "admin.php", "index.php", "wp-login.php", "default", "home"
        ]
        
        with open(wordlist_path, "w") as f:
            f.write("\n".join(common_paths))
        
        logger.info(f"Created default wordlist at {wordlist_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating default wordlist: {e}")
        return False

def check_required_tools():
    """
    Check if the required external tools are installed.
    
    Returns:
        list: A list of missing tools, empty if all tools are installed.
    """
    from app.constants import REQUIRED_TOOLS
    
    missing_tools = []
    for tool in REQUIRED_TOOLS:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        logger.warning(f"Missing tools: {', '.join(missing_tools)}")
    else:
        logger.info("All required tools are installed")
    
    return missing_tools

def run_installation(no_venv=False, skip_wordlists=False):
    """
    Run the complete installation process.
    
    Args:
        no_venv (bool): If True, skip virtual environment creation.
        skip_wordlists (bool): If True, skip wordlists download.
    
    Returns:
        bool: True if installation was successful, False otherwise.
    """
    success = True
    
    # Step 1: Create directory structure
    logger.info("Setting up per-user directory structure")
    if not setup_directory_structure():
        logger.error("Failed to set up directory structure")
        success = False
    
    # Step 2: Set up virtual environment
    if success and not setup_virtual_environment(no_venv):
        logger.error("Failed to set up virtual environment")
        success = False
    
    # Step 3: Download wordlists
    if success and not download_wordlists(skip_wordlists):
        logger.warning("Failed to download wordlists, using minimal wordlist")
        # We continue anyway since we created a minimal wordlist
    
    # Step 4: Check required tools
    missing_tools = check_required_tools()
    if missing_tools:
        logger.warning(f"Some required tools are missing: {', '.join(missing_tools)}")
        logger.warning("The application may not function correctly without these tools")
    
    return success

if __name__ == "__main__":
    # This script shouldn't be run directly; use Install.py instead
    logger.warning("This module is not meant to be run directly. Please use Install.py instead.")
    sys.exit(1)