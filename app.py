import pandas as pd
import os
import json
from config import AppConfig

def load_config() -> AppConfig:
    app_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(app_dir, 'config', 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}")
        exit(1)
    except json.decoder.JSONDecodeError:
        print(f"Config file at {config_path} is not valid JSON")
        exit(1)
    except Exception as e:
        print(f"Error loading config file at {config_path}: {e}")
        exit(1)

    try:
        return AppConfig(**config)
    except Exception as e:
        print(f"Error parsing config file at {config_path}: {e}")
        exit(1)

def main():
    config = load_config()

if __name__ == "__main__":
    main()
