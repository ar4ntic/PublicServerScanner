#!/usr/bin/env python3
"""
Utility functions for the Public Server Scanner Tool.

This module provides shared helper functions for subprocess operations,
logging, path handling, and other common operations.
"""

import os
import sys
import re
import logging
import subprocess
import datetime
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

from app.constants import DEFAULT_COMMAND_TIMEOUT, LOGS_DIR, WORDLISTS_DIR

# Configure logging
def setup_logging(log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure application logging with both file and console output.
    
    Args:
        log_file (str, optional): Path to log file. If None, uses a timestamped file in LOGS_DIR.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    if log_file is None:
        # Create a timestamped log file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOGS_DIR / f"security_scan_{timestamp}.log"
        
        # Ensure logs directory exists
        LOGS_DIR.mkdir(exist_ok=True, parents=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("security_scan")

# Subprocess wrappers
def run_command(cmd: str, output_file: str, timeout: int = DEFAULT_COMMAND_TIMEOUT) -> bool:
    """
    Run a shell command and write its output to a file.
    
    Args:
        cmd (str): Command to run
        output_file (str): File to write output to
        timeout (int, optional): Command timeout in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Running command: {cmd}")
        with open(output_file, "w") as f:
            process = subprocess.run(
                cmd,
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
                check=True,
                timeout=timeout
            )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}\n{e}")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout}s: {cmd}")
        return False
    except Exception as e:
        logger.error(f"Error running command: {cmd}\n{e}")
        return False

def run_command_capture_output(cmd: str, timeout: int = DEFAULT_COMMAND_TIMEOUT) -> Tuple[bool, str]:
    """
    Run a command and capture its output as a string.
    
    Args:
        cmd (str): Command to run
        timeout (int, optional): Command timeout in seconds
        
    Returns:
        Tuple[bool, str]: (success, output)
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Running command and capturing output: {cmd}")
        process = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
            timeout=timeout,
            text=True
        )
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        return False, e.stdout if e.stdout else str(e)
    except subprocess.TimeoutExpired as e:
        logger.error(f"Command timed out after {timeout}s: {cmd}")
        return False, str(e)
    except Exception as e:
        logger.error(f"Error running command: {cmd}\n{e}")
        return False, str(e)

# Path handling
def sanitize_target(target: str) -> str:
    """
    Sanitize the target string for use in folder names.
    
    Args:
        target (str): Target hostname or IP address
        
    Returns:
        str: Sanitized target name safe for use in filenames
    """
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', target)

def create_output_dir(target: str) -> Path:
    """
    Create a timestamped output directory for the scan.
    
    Args:
        target (str): Target hostname or IP address
        
    Returns:
        Path: Path to created output directory
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_target = sanitize_target(target)
    output_dir = Path(f"scan_{sanitized_target}_{timestamp}")
    output_dir.mkdir(exist_ok=True, parents=True)
    return output_dir

def get_wordlist_path() -> str:
    """
    Get the appropriate wordlist path based on configuration and availability.
    
    Returns:
        str: Path to an available wordlist file
    """
    from app.config import Config  # Import here to avoid circular imports
    
    logger = logging.getLogger(__name__)
    config = Config()
    
    # Check if we should use SecLists wordlists
    if config.get("wordlists.selected") == "seclists_common":
        wordlist = config.get("wordlists.seclists_common")
    elif config.get("wordlists.selected") == "seclists_big":
        wordlist = config.get("wordlists.seclists_big")
    elif config.get("wordlists.selected") == "custom" and config.get("wordlists.custom_path"):
        wordlist = config.get("wordlists.custom_path")
    else:
        wordlist = config.get("wordlists.dirb_common")
    
    # Check if the selected wordlist exists
    if os.path.exists(wordlist):
        return wordlist
    
    # Try fallback paths
    for path in config.get("wordlists.fallback_wordlists", []):
        # Replace placeholders
        actual_path = path.format(
            user_home=os.path.expanduser("~"),
            script_dir=os.path.dirname(os.path.abspath(__file__))
        )
        if os.path.exists(actual_path):
            return actual_path
    
    # If all else fails, create and use a minimal wordlist
    logger.info("No existing wordlist found, creating a minimal wordlist")
    temp_wordlist = os.path.join(tempfile.gettempdir(), "minimal_wordlist.txt")
    
    # Create a basic wordlist with common web directories
    basic_dirs = [
        "admin", "login", "wp-admin", "dashboard", "images", "img", "css", "js",
        "api", "uploads", "config", "backup", "dev", "test", "webmail", "mail"
    ]
    
    with open(temp_wordlist, "w") as f:
        f.write("\n".join(basic_dirs))
    
    return temp_wordlist