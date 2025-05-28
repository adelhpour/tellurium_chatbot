import os
import sys
import subprocess
import time
import signal
import atexit
import threading

class ServerManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._endpoint_script = os.path.join(current_dir, "endpoint.py")
        self._mcp_script = os.path.join(current_dir, "mcp_server.py")
        self.endpoint_proc = None
        self.mcp_proc      = None

        # Register cleanup and signal handlers:
        if threading.current_thread() is threading.main_thread():
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, lambda s, f: self._cleanup_and_exit())
        atexit.register(self._cleanup)

    def ensure_running(self):
        self._start_endpoint()
        self._start_mcp()

    def _start_endpoint(self):
        # Only start if not running:
        if not self.endpoint_proc or self.endpoint_proc.poll() is not None:
            self.endpoint_proc = subprocess.Popen(
                [sys.executable, self._endpoint_script],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            time.sleep(1)

    def _start_mcp(self):
        if not self.mcp_proc or self.mcp_proc.poll() is not None:
            # Assume 'mcp' exe is still in Python env dir:
            mcp_exe = os.path.join(os.path.dirname(sys.executable), "mcp")
            self.mcp_proc = subprocess.Popen(
                [mcp_exe, "dev", self._mcp_script],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            time.sleep(1)

    def _cleanup(self):
        for proc in (self.endpoint_proc, self.mcp_proc):
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=1)
                except:
                    proc.kill()
        self.endpoint_proc = self.mcp_proc = None

    def _cleanup_and_exit(self):
        self._cleanup()
        sys.exit(0)
