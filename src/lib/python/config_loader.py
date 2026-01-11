"""Configuration loader for environment variables."""

import os
from pathlib import Path


def load_config():
    """Load environment configuration from .env file.

    Returns:
        os.environ dictionary with loaded variables
    """
    config_path = Path(__file__).parent.parent.parent.parent / "data" / "config" / ".env"

    if config_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(config_path)
        except ImportError:
            # If python-dotenv not installed, manually parse the file
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    return os.environ
