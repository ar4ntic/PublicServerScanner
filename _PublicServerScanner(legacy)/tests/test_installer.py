#!/usr/bin/env python3
"""
Tests for the installer module.

This file contains tests for the installer.py module, which is responsible
for creating the per-user installation directory structure.
"""

import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.constants import APP_DIR, VENV_DIR, WORDLISTS_DIR, LOGS_DIR, CONFIG_PATH
from app.installer import (
    setup_directory_structure,
    setup_virtual_environment,
    download_wordlists,
    create_default_wordlist,
    check_required_tools,
    run_installation
)


@pytest.mark.unit
@pytest.mark.installer
class TestInstaller:
    """Tests for the installer module functionality."""
    
    def test_setup_directory_structure(self, temp_home_dir):
        """Test that setup_directory_structure creates the expected directories."""
        # Run the directory setup function
        result = setup_directory_structure()
        
        # Verify directories were created
        assert result is True
        assert APP_DIR.exists()
        assert VENV_DIR.exists()
        assert WORDLISTS_DIR.exists()
        assert LOGS_DIR.exists()
        
        # Verify default config was created
        assert CONFIG_PATH.exists()
        
        # Verify config content
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        assert 'wordlists' in config
        assert 'nmap' in config
        assert 'timeout' in config
    
    def test_setup_virtual_environment_skip(self):
        """Test that setup_virtual_environment respects the no_venv flag."""
        # Test with no_venv=True
        result = setup_virtual_environment(no_venv=True)
        
        # Should return True without creating venv
        assert result is True
    
    @patch('app.installer.venv.create')
    @patch('app.installer.subprocess.run')
    @patch('app.installer.sys')
    def test_setup_virtual_environment(self, mock_sys, mock_run, mock_venv_create, temp_home_dir):
        """Test virtual environment setup."""
        # Simulate we're not in a virtual environment
        mock_sys.prefix = '/usr'
        mock_sys.base_prefix = '/usr'
        
        # Run the setup function
        result = setup_virtual_environment(no_venv=False)
        
        # Verify venv creation was attempted
        assert mock_venv_create.called
        
        # Mock the existence of the Python executable in the venv
        with patch('pathlib.Path.exists', return_value=True):
            # Run the setup function again
            result = setup_virtual_environment(no_venv=False)
            
            # Verify subprocess was called to install packages
            assert mock_run.called
            assert result is True
    
    @patch('app.installer.shutil.which')
    @patch('app.installer.subprocess.run')
    def test_download_wordlists_skip(self, mock_run, mock_which, temp_home_dir):
        """Test that download_wordlists respects the skip_wordlists flag."""
        # Mock create_default_wordlist to return True
        with patch('app.installer.create_default_wordlist', return_value=True):
            # Test with skip_wordlists=True
            result = download_wordlists(skip_wordlists=True)
            
            # Should return True without attempting git commands
            assert result is True
            assert not mock_run.called
    
    @patch('app.installer.shutil.which')
    @patch('app.installer.subprocess.run')
    def test_download_wordlists_no_git(self, mock_run, mock_which, temp_home_dir):
        """Test download_wordlists when git is not available."""
        # Mock git not being installed
        mock_which.return_value = None
        
        # Mock create_default_wordlist to return True
        with patch('app.installer.create_default_wordlist', return_value=True):
            # Run the function
            result = download_wordlists(skip_wordlists=False)
            
            # Should call create_default_wordlist and return True
            assert result is True
            assert not mock_run.called
    
    def test_create_default_wordlist(self, temp_home_dir):
        """Test creating a default wordlist."""
        # Ensure wordlists directory exists
        WORDLISTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Run the function
        result = create_default_wordlist()
        
        # Check the result and file creation
        assert result is True
        wordlist_path = WORDLISTS_DIR / "common.txt"
        assert wordlist_path.exists()
        
        # Check content
        content = wordlist_path.read_text()
        assert "admin" in content
        assert "login" in content
        assert len(content.split('\n')) > 10  # Ensure we have several paths
    
    @patch('app.installer.shutil.which')
    def test_check_required_tools_all_installed(self, mock_which, temp_home_dir):
        """Test checking for required tools when all are installed."""
        # Mock all tools as being installed
        mock_which.return_value = '/usr/bin/mock_tool'
        
        # Run the check
        missing_tools = check_required_tools()
        
        # Should return an empty list
        assert missing_tools == []
    
    @patch('app.installer.shutil.which')
    def test_check_required_tools_missing(self, mock_which, temp_home_dir):
        """Test checking for required tools when some are missing."""
        # Mock 'nmap' and 'dig' as installed, others missing
        def mock_which_selective(tool):
            return '/usr/bin/tool' if tool in ['nmap', 'dig'] else None
            
        mock_which.side_effect = mock_which_selective
        
        # Run the check
        missing_tools = check_required_tools()
        
        # Should return list of missing tools
        assert len(missing_tools) > 0
        assert 'nmap' not in missing_tools
        assert 'dig' not in missing_tools
    
    @patch('app.installer.setup_directory_structure', return_value=True)
    @patch('app.installer.setup_virtual_environment', return_value=True)
    @patch('app.installer.download_wordlists', return_value=True)
    @patch('app.installer.check_required_tools', return_value=[])
    def test_run_installation_success(self, mock_check, mock_download, mock_venv, mock_dirs, temp_home_dir):
        """Test a successful installation run."""
        # Run the installation
        result = run_installation()
        
        # Should return True and call all setup functions
        assert result is True
        assert mock_dirs.called
        assert mock_venv.called
        assert mock_download.called
        assert mock_check.called
    
    @patch('app.installer.setup_directory_structure', return_value=False)
    def test_run_installation_directory_failure(self, mock_dirs, temp_home_dir):
        """Test installation when directory setup fails."""
        # Run the installation
        result = run_installation()
        
        # Should return False
        assert result is False
        assert mock_dirs.called
    
    @pytest.mark.parametrize("no_venv,skip_wordlists", [
        (True, False),
        (False, True),
        (True, True)
    ])
    @patch('app.installer.setup_directory_structure', return_value=True)
    @patch('app.installer.setup_virtual_environment')
    @patch('app.installer.download_wordlists')
    def test_run_installation_with_options(self, mock_download, mock_venv, mock_dirs, 
                                         no_venv, skip_wordlists, temp_home_dir):
        """Test installation with different options."""
        # Mock successful function calls
        mock_venv.return_value = True
        mock_download.return_value = True
        
        # Run the installation with options
        result = run_installation(no_venv=no_venv, skip_wordlists=skip_wordlists)
        
        # Should pass options to the appropriate functions
        assert result is True
        mock_venv.assert_called_with(no_venv)
        mock_download.assert_called_with(skip_wordlists)