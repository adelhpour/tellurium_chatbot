# llm_service.py
import logging
import requests
import os

from .servers.server_manager import ServerManager
from .clients import MCPClient

# —– module-level singletons —–
_server_manager = ServerManager()
_client: MCPClient | None = None

# default; overridden by set_model_name()
_model_name = "gpt-4o"

def set_model_name(name: str) -> None:
    """
    Configure which LLM model to use for all subsequent send_message() calls.
    """
    global _model_name
    _model_name = name

def get_model_name() -> str:
    """
    Retrieve the current model name in use.
    """
    return _model_name

def _get_client() -> MCPClient:
    """
    Lazily start the server and instantiate the MCPClient,
    caching it for reuse.
    """
    global _client
    if _client is None:
        _server_manager.ensure_running()
        _client = MCPClient(model_name=_model_name)
    return _client

def send_message(query: str) -> str:
    """
    Forward `query` to the running MCP server via a persistent client.
    """
    try:
        client = _get_client()
        return client.ask(query)

    except requests.RequestException as err:
        logging.exception("Backend error when talking to MCP server")
        # propagate so the HTTP layer can handle it
        raise

    except Exception as err:
        logging.exception("Unexpected error in send_message")
        raise