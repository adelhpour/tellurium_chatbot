# main.py
#!/usr/bin/env python3

import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Tellurium Chatbot")
    parser.add_argument(
        "-i", "--interface",
        choices=["ui", "cli"],
        default="cli",
        help="Choose interface mode: 'ui' for Streamlit, 'cli' for command-line"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="llama3.2",
        help="Name of the LLM model to use (e.g. llama3.2, gpt-4o, etc.)"
    )
    args = parser.parse_args()

    # Set the model once for all messages
    from llm_service import llm_service
    llm_service.set_model_name(args.model)

    script_path = os.path.abspath(__file__)

    # If user requested the UI but we're not yet running under Streamlit, re-launch
    if args.interface == "ui" and not os.environ.get("STREAMLIT_RUN"):
        os.environ["STREAMLIT_RUN"] = "1"
        subprocess.run([
            "streamlit", "run", script_path,
            "--", "-i", "ui", "-m", args.model
        ])
        sys.exit()

    # Dispatch to UI or CLI
    if args.interface == "ui" or os.environ.get("STREAMLIT_RUN"):
        from ui import render_chat
        render_chat()
    else:
        from cli import run_cli
        run_cli()

if __name__ == "__main__":
    main()
