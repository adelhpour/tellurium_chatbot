# llm_service.py
import streamlit as st
import requests

from llm_service.servers.server_manager import ServerManager
from llm_service.clients import MCPClient

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
        _client = MCPClient(
            server_script="llm_service/servers/mcp_server.py",
            model_name=_model_name,
        )
    return _client

def send_message(query: str) -> str:
    """
    Forward `query` to the running MCP server via a persistent client.
    """
    try:
        client = _get_client()
        return client.ask(query)
    except requests.RequestException as err:
        st.error(f"Backend error: {err}")
        return "Sorry, something went wrong."
    except Exception as err:
        st.error(f"Unexpected error: {err}")
        return "Sorry, something went wrong."
