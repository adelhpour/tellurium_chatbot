#!/usr/bin/env python3

import argparse
from src.llm_service import llm_service

def main():
    parser = argparse.ArgumentParser(description="Tellurium Chatbot")
    parser.add_argument(
        "-i", "--interface",
        choices=["ui", "cli"],
        default="cli",
        help="Choose interface mode: 'ui' for React, 'cli' for command-line"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="gpt-4o",
        help="Name of the LLM model to use"
    )
    args = parser.parse_args()

    # Configure the LLM (applies to both CLI and UI)
    llm_service.set_model_name(args.model)

    if args.interface == "ui":
        # UI mode
        from src.ui import run_ui
        run_ui(args.model)
    else:
        # CLI mode
        from src.cli import run_cli
        run_cli()

if __name__ == "__main__":
    main()
