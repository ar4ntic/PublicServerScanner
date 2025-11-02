#!/usr/bin/env python3
"""
Constants and default values for the Public Server Scanner Tool.

This module defines all constants used throughout the application,
particularly focusing on paths for the per-user installation directory.
"""

import os
from pathlib import Path

# Application info
APP_NAME = "Public Server Scanner Tool"
APP_VERSION = "1.1"
APP_AUTHOR = "Arantic Digital"
APP_YEAR = "2025"

# Per-user installation paths
HOME_DIR = Path.home()
APP_DIR = HOME_DIR / ".PublicServerScanner"  # Main app directory in user's home
VENV_DIR = APP_DIR / "venv"                # Virtual environment
WORDLISTS_DIR = APP_DIR / "wordlists"      # Directory for wordlists
LOGS_DIR = APP_DIR / "logs"                # Directory for log files
CONFIG_PATH = APP_DIR / "config.json"      # User configuration file

# Default configuration file name
DEFAULT_CONFIG_FILE = "config.json"

# Required external tools
REQUIRED_TOOLS = ["nmap", "nikto", "sslscan", "gobuster", "dig", "openssl", "curl"]

# SecLists repository information
SECLISTS_REPO_URL = "https://github.com/danielmiessler/SecLists.git"
SECLISTS_DIR = WORDLISTS_DIR / "SecLists"
SECLISTS_GOBUSTER_DIR = SECLISTS_DIR / "Discovery" / "Web-Content"
DEFAULT_WORDLIST = WORDLISTS_DIR / "common.txt"

# Default timeouts
DEFAULT_COMMAND_TIMEOUT = 3600  # 1 hour timeout for commands