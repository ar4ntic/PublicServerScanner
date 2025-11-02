#!/usr/bin/env python3
"""
Configuration manager for the Public Server Scanner Tool.

This module provides a Config class to load, save, and access application configuration.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from app.constants import CONFIG_PATH, WORDLISTS_DIR

logger = logging.getLogger(__name__)

class Config:
    """
    Configuration manager class for the Public Server Scanner Tool.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the Config object.
        
        Args:
            config_path (Path, optional): Path to config file. Defaults to APP_DIR/config.json.
        """
        self.config_path = config_path or CONFIG_PATH
        self.config = self._get_default_config()
        self.load()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get the default configuration.
        
        Returns:
            Dict[str, Any]: Default configuration dictionary.
        """
        return {
            "wordlists": {
                "dirb_common": str(WORDLISTS_DIR / "common.txt"),
                "seclists_common": str(WORDLISTS_DIR / "SecLists" / "Discovery" / "Web-Content" / "common.txt"),
                "seclists_big": str(WORDLISTS_DIR / "SecLists" / "Discovery" / "Web-Content" / "big.txt"),
                "selected": "default",
                "custom_path": "",
                "fallback_wordlists": [
                    "/usr/share/wordlists/dirb/common.txt",
                    "/usr/local/share/wordlists/dirb/common.txt",
                    str(Path.home() / "wordlists" / "dirb" / "common.txt"),
                    str(WORDLISTS_DIR / "common.txt")
                ]
            },
            "nmap": {
                "tcp_options": "-sS -Pn -p-",
                "service_options": "-sV -sC -p22,80,443",
                "udp_options": "-sU --top-ports 100"
            },
            "timeout": 3600,
            "scan_threads": 1,
            "advanced_mode": False,
            "ui": {
                "theme": "default",
                "window_size": "500x350",
                "font_size": 12
            },
            "auto_update": True
        }
    
    def load(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if not self.config_path.exists():
            logger.warning(f"Config file not found at {self.config_path}. Using defaults.")
            return False
        
        try:
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
                
            # Update config with user settings
            self._update_config_recursive(self.config, user_config)
            logger.info(f"Configuration loaded from {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return False
    
    def _update_config_recursive(self, target: Dict, source: Dict) -> None:
        """
        Recursively update nested dictionaries.
        
        Args:
            target (Dict): Target dictionary to update
            source (Dict): Source dictionary with new values
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._update_config_recursive(target[key], value)
            else:
                target[key] = value
    
    def save(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key, can use dot notation for nested keys
            default (Any, optional): Default value if key not found
        
        Returns:
            Any: Configuration value or default if not found
        """
        try:
            parts = key.split('.')
            value = self.config
            for part in parts:
                value = value[part]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration value.
        
        Args:
            key (str): Configuration key, can use dot notation for nested keys
            value (Any): Value to set
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            parts = key.split('.')
            config = self.config
            
            # Navigate to the deepest dict
            for part in parts[:-1]:
                if part not in config or not isinstance(config[part], dict):
                    config[part] = {}
                config = config[part]
            
            # Set the value
            config[parts[-1]] = value
            return True
            
        except Exception as e:
            logger.error(f"Error setting config value: {e}")
            return False