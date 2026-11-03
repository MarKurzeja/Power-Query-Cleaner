"""Run the project's workflows from the repository root."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(*args: str) -> None:
    result = subprocess.run([sys.executable, *args], cwd=ROOT)
    if result.returncode != 0:  # stop the workflow and pass the failure on (e.g. to CI)
        sys.exit(result.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Power Query Cleaner project workflows.")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("app", help="open the Streamlit app in your browser")
    commands.add_parser("generate", help="generate the messy sample file data/orders_messy.csv")
    commands.add_parser("test", help="run the automated tests")
    commands.add_parser("check", help="CI check: generate the sample data, then run the tests")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "app":
        run("-m", "streamlit", "run", str(ROOT / "python" / "app.py"))
    elif args.command == "generate":
        run(str(ROOT / "python" / "generate_data.py"))
    elif args.command == "test":
        run("-m", "pytest", "-q")
    elif args.command == "check":
        run(str(ROOT / "python" / "generate_data.py"))
        run("-m", "pytest", "-q")


if __name__ == "__main__":
    main()
