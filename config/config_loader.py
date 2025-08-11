import os
import yaml
import logging
from pathlib import Path
from dotenv import load_dotenv

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, '.env')) # Load environment variables from .env file


class ConfigLoader:
    """
    Loads configuration from YAML files with environment variable override support.
    """
    
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self._config_cache = {}
    
    def load_config(self, name):
        """
        Load configuration from a YAML file.
        
        Args:
            name: Name of the configuration file without extension (e.g., 'embedding_config')
            
        Returns:
            dict: Configuration as a dictionary
        """
        # If this file was already loaded, serve the version from the cache
        if name in self._config_cache:
            return self._config_cache[name]
        
        # Check if the config file exists and load it
        config_path = self.config_dir / f"{name}.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file {config_path} not found")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Process any path expansions like ~ for home directory
        self._process_paths(config)
        
        self._config_cache[name] = config
        return config
    
    def _process_paths(self, config):
        """Process any paths in the config to expand user paths."""
        for key, value in config.items():
            if isinstance(value, str) and '~' in value:
                config[key] = os.path.expanduser(value)
            elif isinstance(value, dict):
                self._process_paths(value)

# Create a singleton instance for use throughout the application
config_loader = ConfigLoader()

# Helper functions to easily access specific configs
def get_embedding_config():
    """Get the embedding configuration."""
    return config_loader.load_config('embedding_config')

def get_llm_config():
    """Get the LLM configuration."""
    return config_loader.load_config('llm_config')