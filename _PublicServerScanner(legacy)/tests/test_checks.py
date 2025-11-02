#!/usr/bin/env python3
"""
Tests for the security check modules.

This file contains tests for the individual security check modules.
"""

import os
import sys
import pytest
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.checks.ping import ping_target
from app.checks.portscan import port_scan, tcp_port_scan, service_version_scan, udp_port_scan
from app.checks.bruteforce import directory_bruteforce
from app.checks.dns import dns_enumeration
from app.checks.cert import certificate_details
from app.checks.headers import gather_headers


@pytest.mark.unit
@pytest.mark.checks
class TestPing:
    """Tests for the ping check module."""
    
    @patch('app.utils.run_command')
    def test_ping_target_success(self, mock_run_command):
        """Test successful ping execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = ping_target("example.com", "/tmp")
        
        # Verify result and command formatting
        assert result is True
        mock_run_command.assert_called_once()
        # Check that command contains the target
        cmd_arg = mock_run_command.call_args[0][0]
        assert "ping" in cmd_arg
        assert "example.com" in cmd_arg


@pytest.mark.unit
@pytest.mark.checks
class TestPortScan:
    """Tests for the port scan module."""
    
    @patch('app.checks.portscan.tcp_port_scan')
    @patch('app.checks.portscan.service_version_scan')
    @patch('app.checks.portscan.udp_port_scan')
    def test_port_scan_all_success(self, mock_udp, mock_service, mock_tcp):
        """Test port scan when all scans succeed."""
        # Configure mocks to return success
        mock_tcp.return_value = True
        mock_service.return_value = True
        mock_udp.return_value = True
        
        # Call the function
        result = port_scan("example.com", "/tmp")
        
        # Verify all scan types were called
        assert result is True
        mock_tcp.assert_called_once()
        mock_service.assert_called_once()
        mock_udp.assert_called_once()
    
    @patch('app.checks.portscan.tcp_port_scan', return_value=False)
    @patch('app.checks.portscan.service_version_scan')
    @patch('app.checks.portscan.udp_port_scan')
    def test_port_scan_tcp_failure(self, mock_udp, mock_service, mock_tcp):
        """Test port scan when TCP scan fails."""
        # Call the function
        result = port_scan("example.com", "/tmp")
        
        # Verify result is False
        assert result is False
        
    @patch('app.utils.run_command')
    def test_tcp_port_scan(self, mock_run_command):
        """Test TCP port scan execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = tcp_port_scan("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "nmap" in cmd_arg
        assert "example.com" in cmd_arg
    
    @patch('app.utils.run_command')
    def test_service_version_scan(self, mock_run_command):
        """Test service version scan execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = service_version_scan("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "nmap" in cmd_arg
        assert "-sV" in cmd_arg
        assert "example.com" in cmd_arg
    
    @patch('app.utils.run_command')
    def test_udp_port_scan(self, mock_run_command):
        """Test UDP port scan execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = udp_port_scan("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "nmap" in cmd_arg
        assert "-sU" in cmd_arg
        assert "example.com" in cmd_arg


@pytest.mark.unit
@pytest.mark.checks
class TestBruteforce:
    """Tests for the directory bruteforce module."""
    
    @patch('app.utils.get_wordlist_path')
    @patch('app.utils.run_command')
    def test_directory_bruteforce(self, mock_run_command, mock_get_wordlist):
        """Test directory bruteforce execution."""
        # Configure mocks
        mock_get_wordlist.return_value = "/path/to/wordlist.txt"
        mock_run_command.return_value = True
        
        # Call the function
        result = directory_bruteforce("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "gobuster" in cmd_arg
        assert "http://example.com" in cmd_arg
        assert "/path/to/wordlist.txt" in cmd_arg
    
    @patch('app.utils.get_wordlist_path')
    @patch('app.utils.run_command')
    def test_directory_bruteforce_with_protocol(self, mock_run_command, mock_get_wordlist):
        """Test directory bruteforce when target already has protocol."""
        # Configure mocks
        mock_get_wordlist.return_value = "/path/to/wordlist.txt"
        mock_run_command.return_value = True
        
        # Call the function with a target that includes protocol
        result = directory_bruteforce("https://example.com", "/tmp")
        
        # Verify protocol wasn't duplicated
        assert result is True
        cmd_arg = mock_run_command.call_args[0][0]
        assert "https://example.com" in cmd_arg
        assert "http://https://" not in cmd_arg


@pytest.mark.unit
@pytest.mark.checks
class TestDns:
    """Tests for the DNS enumeration module."""
    
    @patch('app.utils.run_command')
    def test_dns_enumeration(self, mock_run_command):
        """Test DNS enumeration execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = dns_enumeration("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "dig" in cmd_arg
        assert "example.com" in cmd_arg
    
    @patch('app.utils.run_command')
    def test_dns_enumeration_strips_protocol(self, mock_run_command):
        """Test DNS enumeration removes protocol from target."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function with a URL
        result = dns_enumeration("https://example.com/path", "/tmp")
        
        # Verify protocol and path were removed
        assert result is True
        cmd_arg = mock_run_command.call_args[0][0]
        assert "https://" not in cmd_arg
        assert "/path" not in cmd_arg
        assert "example.com" in cmd_arg


@pytest.mark.unit
@pytest.mark.checks
class TestCert:
    """Tests for the certificate details module."""
    
    @patch('app.utils.run_command')
    def test_certificate_details(self, mock_run_command):
        """Test certificate details execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = certificate_details("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "openssl" in cmd_arg
        assert "s_client" in cmd_arg
        assert "example.com:443" in cmd_arg
    
    @patch('app.utils.run_command')
    def test_certificate_details_with_port(self, mock_run_command):
        """Test certificate details with custom port."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function with port specified
        result = certificate_details("example.com:8443", "/tmp")
        
        # Verify port was preserved
        assert result is True
        cmd_arg = mock_run_command.call_args[0][0]
        assert "example.com:8443" in cmd_arg
        assert "example.com:443:443" not in cmd_arg
    
    @patch('app.utils.run_command')
    def test_certificate_details_with_protocol(self, mock_run_command):
        """Test certificate details removes protocol from target."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function with a URL
        result = certificate_details("https://example.com/path", "/tmp")
        
        # Verify protocol and path were removed
        assert result is True
        cmd_arg = mock_run_command.call_args[0][0]
        assert "https://" not in cmd_arg
        assert "/path" not in cmd_arg
        assert "example.com:443" in cmd_arg


@pytest.mark.unit
@pytest.mark.checks
class TestHeaders:
    """Tests for the HTTP headers module."""
    
    @patch('app.utils.run_command')
    def test_gather_headers(self, mock_run_command):
        """Test HTTP headers gathering execution."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function
        result = gather_headers("example.com", "/tmp")
        
        # Verify command formatting
        assert result is True
        mock_run_command.assert_called_once()
        cmd_arg = mock_run_command.call_args[0][0]
        assert "curl" in cmd_arg
        assert "http://example.com" in cmd_arg
    
    @patch('app.utils.run_command')
    def test_gather_headers_with_protocol(self, mock_run_command):
        """Test HTTP headers with protocol specified."""
        # Configure mock to return success
        mock_run_command.return_value = True
        
        # Call the function with protocol
        result = gather_headers("https://example.com", "/tmp")
        
        # Verify protocol was preserved
        assert result is True
        cmd_arg = mock_run_command.call_args[0][0]
        assert "https://example.com" in cmd_arg
        assert "http://https://" not in cmd_arg