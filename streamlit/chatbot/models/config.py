"""Configuration for model providers and their supported models."""
import tomli
from pathlib import Path

# Read the TOML configuration file
CONFIG_PATH = Path(__file__).parent / "models.toml"
with open(CONFIG_PATH, "rb") as f:
    PROVIDER_CONFIGS = tomli.load(f)

# Validate the configuration
for provider, config in PROVIDER_CONFIGS.items():
    required_fields = ["name", "models", "requires_base_url"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field '{field}' in {provider} configuration") 