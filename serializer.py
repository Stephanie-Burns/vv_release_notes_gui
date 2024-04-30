import json
import logging
import os
import tkinter as tk
from typing import Dict

from constants import CONFIG_FILE_PATH


logger = logging.getLogger('AppLogger')


def build_app_config() -> Dict:
    """Builds a default application configuration dictionary."""
    return {
        "configuration_history": {},
        "email_distribution_lists": {},
        "email_credentials": {}
    }


def serialize_config(app_config: Dict) -> dict:
    """Converts the configuration data with Tkinter variables into JSON-serializable format."""
    try:
        serializable_config = {
            "configuration_history": {
                key: value.get() if isinstance(value, tk.Variable) else value
                for key, value in app_config["configuration_history"].items()
            },
            "email_distribution_lists": app_config["email_distribution_lists"],
            "email_credentials": app_config["email_credentials"]
        }
        logger.info("Configuration serialized successfully.")
        return serializable_config
    except Exception as e:
        logger.error("Failed to serialize configuration: %s", str(e))
        raise


def deserialize_config(serialized_config: Dict) -> Dict:
    """Converts JSON-loaded data back to the appropriate Tkinter variables and structures."""
    try:
        app_config = {
            "configuration_history": {
                key: tk.BooleanVar(value=value) if isinstance(value, bool) else tk.StringVar(value=value)
                for key, value in serialized_config["configuration_history"].items()
            },
            "email_distribution_lists": serialized_config["email_distribution_lists"],
            "email_credentials": serialized_config["email_credentials"]
        }
        logger.info("Configuration deserialized successfully.")
        return app_config
    except Exception as e:
        logger.error("Failed to deserialize configuration: %s", str(e))
        raise


def save_configuration_to_file(app_config: Dict, filename: str = CONFIG_FILE_PATH) -> None:
    """Saves the application configuration to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(serialize_config(app_config), f, indent=4)
        logger.info("Configuration saved to file successfully.")
    except Exception as e:
        logger.error("Failed to save configuration to file: %s", str(e))
        raise


def load_configuration_from_file(filename: str = CONFIG_FILE_PATH) -> Dict:
    """Loads the application configuration from a JSON file or creates a new one if necessary."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                serialized_config = json.load(f)
                logger.info("Configuration loaded from disk successfully.")
            return deserialize_config(serialized_config)
        else:
            raise FileNotFoundError("Configuration file not found.")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning("Error loading configuration: %s. Building a default configuration.", str(e))
        return build_app_config()
    except Exception as e:
        logger.error("An unexpected error occurred: %s. Using default configuration.", str(e))
        return build_app_config()
