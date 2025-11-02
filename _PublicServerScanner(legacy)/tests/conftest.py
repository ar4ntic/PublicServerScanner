"""
Pytest configuration file with shared fixtures.

This module contains pytest fixtures that can be used across test files.
"""

import os
import sys
import json
import shutil
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def temp_home_dir(tmp_path):
    """
    Create a temporary home directory for testing.
    
    This allows us to test the per-user installation functionality without
    modifying the user's actual home directory.
    """
    # Save the original HOME environment variable
    original_home = os.environ.get('HOME')
    
    # Set HOME to the temporary directory
    temp_home = tmp_path / "home"
    temp_home.mkdir()
    os.environ['HOME'] = str(temp_home)
    
    # Return the temp home path for tests to use
    yield temp_home
    
    # Restore the original HOME
    if original_home:
        os.environ['HOME'] = original_home
    else:
        del os.environ['HOME']


@pytest.fixture
def mock_subprocess():
    """
    Mock subprocess calls to simulate command execution.
    """
    with patch('subprocess.run') as mock_run:
        # Configure the mock to return a successful result by default
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Mock command output"
        mock_run.return_value = mock_process
        
        yield mock_run


@pytest.fixture
def sample_config_file(tmp_path):
    """
    Create a sample config.json file for testing.
    """
    config_path = tmp_path / "config.json"
    config_data = {
        "wordlists": {
            "dirb_common": str(tmp_path / "wordlists" / "common.txt"),
            "seclists_common": str(tmp_path / "wordlists" / "SecLists" / "Discovery" / "Web-Content" / "common.txt"),
            "seclists_big": str(tmp_path / "wordlists" / "SecLists" / "Discovery" / "Web-Content" / "big.txt"),
            "selected": "default",
            "custom_path": "",
            "fallback_wordlists": [
                "/usr/share/wordlists/dirb/common.txt",
                str(tmp_path / "wordlists" / "common.txt")
            ]
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
    
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
        
    return config_path


@pytest.fixture
def sample_wordlist(tmp_path):
    """
    Create a sample wordlist file for testing.
    """
    wordlists_dir = tmp_path / "wordlists"
    wordlists_dir.mkdir(exist_ok=True)
    
    wordlist_path = wordlists_dir / "common.txt"
    with open(wordlist_path, 'w') as f:
        f.write("admin\n")
        f.write("login\n")
        f.write("dashboard\n")
        f.write("wp-admin\n")
        f.write("images\n")
        f.write("css\n")
    
    return wordlist_path


@pytest.fixture
def mock_tools_installed():
    """
    Mock the shutil.which function to simulate all tools being installed.
    """
    with patch('shutil.which', return_value='/usr/bin/mock_tool'):
        yield


@pytest.fixture
def mock_command_success():
    """
    Mock the run_command function to always return True (success).
    """
    with patch('app.utils.run_command', return_value=True):
        yield


@pytest.fixture
def mock_command_failure():
    """
    Mock the run_command function to always return False (failure).
    """
    with patch('app.utils.run_command', return_value=False):
        yield


@pytest.fixture
def mock_app_dir(temp_home_dir):
    """
    Create a mock app directory structure under a temporary home directory.
    """
    # Import here to avoid circular imports during test collection
    from app.constants import APP_DIR, VENV_DIR, WORDLISTS_DIR, LOGS_DIR
    
    # Create the main directory structure
    app_dir = temp_home_dir / ".PublicServerScanner"
    app_dir.mkdir(exist_ok=True)
    
    venv_dir = app_dir / "venv"
    venv_dir.mkdir(exist_ok=True)
    
    wordlists_dir = app_dir / "wordlists"
    wordlists_dir.mkdir(exist_ok=True)
    
    logs_dir = app_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Create a sample wordlist
    with open(wordlists_dir / "common.txt", 'w') as f:
        f.write("admin\nlogin\ndashboard\nwp-admin\nimages\ncss\n")
    
    # Create a sample config file
    config_path = app_dir / "config.json"
    config_data = {
        "wordlists": {
            "dirb_common": str(wordlists_dir / "common.txt"),
            "selected": "default"
        },
        "nmap": {
            "tcp_options": "-sS -Pn -p-",
            "service_options": "-sV -sC -p22,80,443",
            "udp_options": "-sU --top-ports 100"
        },
        "timeout": 3600
    }
    
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    
    return {
        "app_dir": app_dir,
        "venv_dir": venv_dir,
        "wordlists_dir": wordlists_dir,
        "logs_dir": logs_dir,
        "config_path": config_path
    }