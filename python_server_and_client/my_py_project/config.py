import json
import os

class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load the configuration from a JSON file."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def get(self, key, default=None):
        """Get a configuration value by key."""
        return self.config.get(key, default)


def load_client_config():
    config_file = os.path.join(os.path.dirname(__file__), 'client', 'config.json')
    return ConfigLoader(config_file)


def load_server_config():
    config_file = os.path.join(os.path.dirname(__file__), 'server', 'config.json')
    return ConfigLoader(config_file)

