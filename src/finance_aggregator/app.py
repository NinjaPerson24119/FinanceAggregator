import os
import json
from finance_aggregator.config import AppConfig
from finance_aggregator.finance_data_builder import build_finance_data_objects
from finance_aggregator.finance_data import FinanceData
import argparse
from dataclasses import dataclass


def load_app_config(config_path: str) -> AppConfig:
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


@dataclass
class AppArgs:
    config_path: str
    work_dir: str


def parse_args() -> AppArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        help="Path to config file. Check config_example/config_example.json for an example.",
        required=True,
    )
    parser.add_argument(
        "-w",
        "--work-dir",
        help="Path to working directory. Adds to the beginning of all paths in config file. Defaults to current directory.",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output file. Defaults to output.csv in working directory.",
        default="output.csv",
    )
    args = parser.parse_args()

    return AppArgs(config_path=args.config, work_dir=args.work_dir)


def rebase_config_paths(config: AppConfig, work_dir: str) -> AppConfig:
    for source in config.sources:
        source.path = os.path.join(work_dir, source.path)
    return config


def main():
    app_args = parse_args()
    app_config = load_app_config(os.path.join(app_args.work_dir, app_args.config_path))
    app_config = rebase_config_paths(app_config, app_args.work_dir)
    output_path = os.path.join(app_args.work_dir, app_args.output)

    finance_data_objects = build_finance_data_objects(app_config)
    combined_finance_data = FinanceData()
    for finance_data in finance_data_objects:
        combined_finance_data.combine(finance_data)

    combined_finance_data.to_csv(output_path)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
