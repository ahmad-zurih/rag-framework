import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, '.env')) # Load environment variables from .env file


class ConfigLoader:
    """
    Loads configuration from YAML files with environment variable override support.
    """
    
    def __init__(self, config_dir=None):
        """
        Initialize the config loader.
        
        Args:
            config_dir: Directory where config files are located. Defaults to the 'config' directory.
        """
        if config_dir is None:
            # Default to the directory where this file is located
            self.config_dir = Path(__file__).parent
        else:
            self.config_dir = Path(config_dir)
        
        self._config_cache = {}
    
    def load_config(self, name):
        """
        Load configuration from a YAML file.
        
        Args:
            name: Name of the configuration file without extension (e.g., 'embedding_config')
            
        Returns:
            dict: Configuration as a dictionary
        """
        if name in self._config_cache:
            return self._config_cache[name]
            
        config_path = self.config_dir / f"{name}.yaml"
            
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file {config_path} not found")
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Process any path expansions like ~ for home directory
        self._process_paths(config)
        
        # Apply environment variable overrides
        self._apply_env_overrides(config, name.upper())
        
        self._config_cache[name] = config
        return config
    
    def _process_paths(self, config):
        """Process any paths in the config to expand user paths."""
        for key, value in config.items():
            if isinstance(value, str) and '~' in value:
                config[key] = os.path.expanduser(value)
            elif isinstance(value, dict):
                self._process_paths(value)
    
    def _apply_env_overrides(self, config, prefix):
        """Apply environment variable overrides to the configuration."""
        for key, value in config.items():
            env_key = f"{prefix}_{key.upper()}"
            if env_key in os.environ:
                # Convert environment variable to appropriate type
                env_value = os.environ[env_key]
                if isinstance(value, bool):
                    config[key] = env_value.lower() in ('true', 'yes', '1')
                elif isinstance(value, int):
                    config[key] = int(env_value)
                elif isinstance(value, float):
                    config[key] = float(env_value)
                else:
                    config[key] = env_value
            elif isinstance(value, dict):
                self._apply_env_overrides(value, f"{prefix}_{key.upper()}")

# Create a singleton instance for use throughout the application
config_loader = ConfigLoader()

# Helper functions to easily access specific configs
def get_embedding_config():
    """Get the embedding configuration."""
    return config_loader.load_config('embedding_config')

def get_llm_config():
    """Get the LLM configuration."""
    return config_loader.load_config('llm_config')