import pandas as pd
import os
import json
from config import AppConfig
from finance_data_builder import build_finance_data_objects
from finance_data import FinanceData


def load_app_config() -> AppConfig:
    app_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(app_dir, "config", "config.json")
    try:
        with open(config_path, "r") as f:
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
    app_config = load_app_config()
    finance_data_objects = build_finance_data_objects(app_config)

    combined_finance_data = FinanceData()
    for finance_data in finance_data_objects:
        combined_finance_data.combine(finance_data)

    combined_finance_data.to_csv(app_config.output_path)


if __name__ == "__main__":
    main()
