import streamlit as st
import requests

from llm_service.servers.server_manager import ServerManager
from llm_service.clients import MCPClient

def send_message(query: str) -> str:
    """
    Ensure the tellurium MCP server is up,
    forward `query` to it via MCPClient, and
    return the assistant’s response.
    """
    # 1) start your subprocesses if needed
    ServerManager().ensure_running()

    try:
        # 2) instantiate the refactored client
        client = MCPClient(
            server_script="llm_service/servers/mcp_server.py",
            model_name="llama3.2"
        )
        # 3) synchronously ask & return
        return client.ask(query)

    except requests.RequestException as err:
        st.error(f"Backend error: {err}")
        return "Sorry, something went wrong."
    except Exception as err:
        st.error(f"Unexpected error: {err}")
        return "Sorry, something went wrong."
