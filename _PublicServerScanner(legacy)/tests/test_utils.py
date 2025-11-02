#!/usr/bin/env python3
"""
Tests for the utils module.

This file contains tests for the utility functions in utils.py.
"""

import os
import sys
import pytest
import tempfile
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.utils import (
    setup_logging,
    run_command,
    run_command_capture_output,
    sanitize_target,
    create_output_dir,
    get_wordlist_path
)


@pytest.mark.unit
class TestUtils:
    """Tests for utility functions."""
    
    def test_setup_logging(self):
        """Test that setup_logging returns a logger."""
        logger = setup_logging()
        assert isinstance(logger, logging.Logger)
        assert logger.name == "security_scan"
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test running a command successfully."""
        # Configure the mock to simulate success
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        # Use a temporary file for output
        with tempfile.NamedTemporaryFile() as tmp:
            # Run the command
            result = run_command("echo test", tmp.name)
            
            # Verify success and mock was called
            assert result is True
            mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test running a command that fails."""
        # Configure the mock to simulate failure
        mock_run.side_effect = subprocess.CalledProcessError(1, "test command")
        
        # Use a temporary file for output
        with tempfile.NamedTemporaryFile() as tmp:
            # Run the command
            result = run_command("false", tmp.name)
            
            # Verify failure
            assert result is False
    
    @patch('subprocess.run')
    def test_run_command_timeout(self, mock_run):
        """Test running a command that times out."""
        # Configure the mock to simulate timeout
        mock_run.side_effect = subprocess.TimeoutExpired("test command", 10)
        
        # Use a temporary file for output
        with tempfile.NamedTemporaryFile() as tmp:
            # Run the command
            result = run_command("sleep 100", tmp.name, timeout=1)
            
            # Verify failure
            assert result is False
    
    @patch('subprocess.run')
    def test_run_command_capture_output_success(self, mock_run):
        """Test capturing command output successfully."""
        # Configure the mock to simulate success
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Command output"
        mock_run.return_value = mock_process
        
        # Run the command
        success, output = run_command_capture_output("echo test")
        
        # Verify success and output
        assert success is True
        assert output == "Command output"
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_run_command_capture_output_failure(self, mock_run):
        """Test capturing command output when command fails."""
        # Configure the mock to simulate failure with output
        mock_error = subprocess.CalledProcessError(1, "test command")
        mock_error.stdout = "Error output"
        mock_run.side_effect = mock_error
        
        # Run the command
        success, output = run_command_capture_output("false")
        
        # Verify failure and output
        assert success is False
        assert output == "Error output"
    
    def test_sanitize_target(self):
        """Test sanitizing target names for use in filenames."""
        # Test various inputs
        assert sanitize_target("example.com") == "example.com"
        assert sanitize_target("http://example.com") == "http___example.com"
        assert sanitize_target("test/path?query=value") == "test_path_query_value"
        assert sanitize_target("192.168.1.1") == "192.168.1.1"
    
    def test_create_output_dir(self):
        """Test creating an output directory."""
        # Call the function
        output_dir = create_output_dir("example.com")
        
        # Verify directory was created and has correct name format
        assert output_dir.exists()
        assert output_dir.is_dir()
        assert "scan_example.com_" in str(output_dir)
        
        # Clean up
        output_dir.rmdir()
    
    @patch('app.config.Config')
    def test_get_wordlist_path_default(self, mock_config_class, sample_wordlist):
        """Test getting the default wordlist path."""
        # Setup mock config
        mock_config = MagicMock()
        mock_config.get.side_effect = lambda key, default=None: {
            "wordlists.selected": "default",
            "wordlists.dirb_common": str(sample_wordlist)
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        # Get the wordlist path
        path = get_wordlist_path()
        
        # Verify the path is correctly returned
        assert path == str(sample_wordlist)
    
    @patch('os.path.exists')
    @patch('app.config.Config')
    def test_get_wordlist_path_fallback(self, mock_config_class, mock_exists, tmp_path):
        """Test fallback to alternative wordlists."""
        # Setup mock config with nonexistent primary path
        mock_config = MagicMock()
        fallback_paths = ["/nonexistent/path", str(tmp_path / "wordlist.txt")]
        mock_config.get.side_effect = lambda key, default=None: {
            "wordlists.selected": "default",
            "wordlists.dirb_common": "/nonexistent/path",
            "wordlists.fallback_wordlists": fallback_paths
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        # Mock exists to return True only for the second fallback path
        mock_exists.side_effect = lambda path: path == fallback_paths[1]
        
        # Create the fallback wordlist
        os.makedirs(os.path.dirname(fallback_paths[1]), exist_ok=True)
        with open(fallback_paths[1], 'w') as f:
            f.write("test\n")
        
        # Get the wordlist path
        path = get_wordlist_path()
        
        # Verify we got the fallback path
        assert path == fallback_paths[1]