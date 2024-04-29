import json
import tkinter as tk
from typing import Dict

from constants import CONFIG_FILE_PATH


def serialize_config(app_config: Dict) -> dict:
    """Converts the configuration data with Tkinter variables into JSON-serializable format."""
    serializable_config = {
        "configuration_history": {
            key: value.get() if isinstance(value, tk.Variable) else value
            for key, value in app_config["configuration_history"].items()
        },
        "email_distribution_lists": app_config["email_distribution_lists"],
        "email_credentials": app_config["email_credentials"]
    }
    return serializable_config


def save_configuration_to_file(app_config: Dict, filename: str = CONFIG_FILE_PATH) -> None:
    """Saves the application configuration to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(serialize_config(app_config), f, indent=4)


def deserialize_config(serialized_config: Dict) -> Dict:
    """Converts JSON-loaded data back to the appropriate Tkinter variables and structures."""
    app_config = {
        "configuration_history": {
            key: tk.BooleanVar(value=value) if isinstance(value, bool) else tk.StringVar(value=value)
            for key, value in serialized_config["configuration_history"].items()
        },
        "email_distribution_lists": serialized_config["email_distribution_lists"],
        "email_credentials": serialized_config["email_credentials"]
    }
    return app_config


def load_configuration_from_file(filename: str = CONFIG_FILE_PATH) -> Dict:
    """Loads the application configuration from a JSON file."""
    with open(filename, 'r') as f:
        serialized_config = json.load(f)
    return deserialize_config(serialized_config)
