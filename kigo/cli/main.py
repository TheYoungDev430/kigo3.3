# SPDX-License-Identifier: Zlib
# kigo/cli/main.py

import sys
import argparse

from kigo.cli.doctor import run_doctor


def main():
    parser = argparse.ArgumentParser(
        prog="kigo",
        description="Kigo CLI"
    )

    sub = parser.add_subparsers(dest="command")

    # kigo run
    sub.add_parser("run", help="Run the Kigo app")

    # kigo doctor
    sub.add_parser("doctor", help="Diagnose common Kigo issues")

    args = parser.parse_args()

    if args.command == "run":
        run_app()
    elif args.command == "doctor":
        run_doctor()
    else:
        parser.print_help()


def run_app():
    """
    Runs app.py in the current directory.
    """
    try:
        __import__("app")
    except ModuleNotFoundError:
        print("❌ No app.py found in current directory. Please rename your file to app.py and try again.")
        sys.exit(1)
    except Exception as e:
        print("❌ Failed to run app:")
        print(e)
        sys.exit(1)