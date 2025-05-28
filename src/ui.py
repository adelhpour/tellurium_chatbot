#!/usr/bin/env python3

import os
import sys
import subprocess
import signal

def run_ui(model_name: str):
    """
    Launches the Tellurium Chatbot in UI mode:
      1) configures the LLM
      2) spins up the Flask backend
      3) starts the React dev server
      4) handles clean shutdown on Ctrl+C
    """
    # 1) Configure the LLM
    from src.llm_service import llm_service
    llm_service.set_model_name(model_name)

    # 2) Resolve paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_app   = os.path.join(project_root, "src", "backend.py")
    frontend_dir  = os.path.join(project_root, "src", "frontend")

    # 3) Start Flask backend
    backend_proc = subprocess.Popen(
        [sys.executable, backend_app],
    )

    # 4) Start React dev server
    frontend_proc = subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_dir,
    )

    # 5) Clean shutdown handler
    def _shutdown(sig, frame):
        backend_proc.terminate()
        frontend_proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)

    # 6) Block until frontend exits
    frontend_proc.wait()
    _shutdown(None, None)
