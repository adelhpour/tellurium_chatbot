from typing import Any, Dict, List, Optional, Union
import httpx
from mcp.server.fastmcp import FastMCP

# ----------------------------------------------------------------------
#  FastMCP server initialisation
# ----------------------------------------------------------------------

mcp = FastMCP("tellurium_server")

# ----------------------------------------------------------------------
#  Local-API settings
# ----------------------------------------------------------------------

LOCAL_API_BASE = "http://127.0.0.1:5000"  # adjust port/host if needed
DEFAULT_TIMEOUT = 10.0  # seconds


async def call_local_api(
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """
    Helper that performs an HTTP request against your local Flask server.

    Args:
        method:  "GET", "POST", etc.
        path:    Endpoint path beginning with '/' (e.g. '/status')
        json:    Optional JSON body for POST/PUT requests

    Returns:
        Parsed JSON dict *or* None on any exception / non-2xx status.
    """
    url = f"{LOCAL_API_BASE}{path}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(method, url, json=json, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None


# ----------------------------------------------------------------------
#  MCP-exposed tools
# ----------------------------------------------------------------------

@mcp.tool()
async def status() -> str:
    """
    Fetch the API server health check information from the `/status` endpoint.

    This tool requires no parameters and returns a formatted string containing
    key health metrics about the Tellurium server.

    Returns:
        A multi-line string with key-value pairs showing server status information.
        Each line will be formatted as "key: value".
        Example return value:
        ```
        status: online
        uptime: 124 minutes
        memory_usage: 256MB
        active_simulations: 2
        ```

    If the server cannot be reached, returns an error message.
    """
    data = await call_local_api("GET", "/status")

    if not data:
        return "❌ Unable to reach the local API on /status. The server may be offline or not responding."

    # Pretty-print the returned dict
    return "\n".join(f"{k}: {v}" for k, v in data.items())


@mcp.tool()
async def echo(message: str) -> str:
    """
    Send a message to the `/echo` endpoint to test connectivity and response.

    This tool sends your message to the server and returns whatever the server sends back.
    Use this tool to verify server communication is working properly.

    Args:
        message: The string message to send to the server.
                Must be a non-empty string.

    Returns:
        A string containing the server's response, typically an echo of your message
        possibly with additional metadata.
        Example return value for message="hello":
        ```
        {"echo": "hello", "timestamp": "2025-05-07T12:34:56Z"}
        ```

    If the server cannot be reached, returns an error message.
    """
    if not message or not isinstance(message, str):
        return "Error: 'message' parameter must be a non-empty string."

    payload = {"message": message}
    data = await call_local_api("POST", "/echo", json=payload)

    if not data:
        return "Unable to reach the local API on /echo. The server may be offline or not responding."

    return str(data)


@mcp.tool()
async def tellurium_version() -> str:
    """
    Fetch the Tellurium software version information from the `/version` endpoint.

    This tool requires no parameters and returns formatted version details about
    the Tellurium simulation environment and its dependencies.

    Returns:
        A multi-line string with key-value pairs showing version information.
        Each line will be formatted as "component: version".
        Example return value:
        ```
        tellurium: 2.2.0
        roadrunner: 2.1.3
        antimony: 2.13.0
        libsbml: 5.19.0
        python: 3.9.7
        ```

    If the server cannot be reached, returns an error message.
    """
    data = await call_local_api("GET", "/version")

    if not data:
        return "Unable to reach the local API on /version. The server may be offline or not responding."

    # Pretty-print the returned dict
    return "\n".join(f"{k}: {v}" for k, v in data.items())


@mcp.tool()
async def tellurium_simulate(
        antimony: str,
        t_start: int,
        t_end: int,
        n_steps: int
) -> str:
    """
    Run a Tellurium biochemical model simulation and return the time-series results.

    This tool takes an Antimony model string and simulation parameters, sends them
    to the server for processing, and returns tabular simulation results.

    Args:
        antimony: Antimony model string defining the biochemical system.
                 Must follow Antimony syntax (http://antimony.sourceforge.net/).
                 Example: "S1 -> S2; k1*S1; k1=0.1; S1 = 10"

        t_start: Simulation start time (integer).
                Must be a non-negative integer, typically 0.

        t_end: Simulation end time (integer).
               Must be greater than t_start.
               Typical values range from 10 to 100 depending on model dynamics.

        n_steps: Number of data points to compute (integer).
                Must be a positive integer between 10 and 1000.
                Higher values give smoother curves but take longer to compute.

    Returns:
        A tab-separated values (TSV) string containing the simulation results.
        The first row contains column headers (typically "time" followed by species names).
        Subsequent rows contain the simulation data points.

        Example return value:
        ```
        time	S1	S2
        0.0	10.0	0.0
        1.0	9.048	0.952
        2.0	8.187	1.813
        ...
        ```

    If the simulation fails or the server is unreachable, returns an error message.

    Usage tips:
    - Ensure your Antimony model is syntactically correct
    - Use sufficient n_steps (>= 100) for complex dynamics
    - Set t_end large enough to capture the behavior of interest
    - Check that all reactions and parameters are properly defined
    """
    # Input validation
    if not antimony or not isinstance(antimony, str):
        return "Error: 'antimony' parameter must be a non-empty string containing a valid Antimony model."

    if not isinstance(t_start, int) or t_start < 0:
        return "Error: 't_start' must be a non-negative integer."

    if not isinstance(t_end, int) or t_end <= t_start:
        return "Error: 't_end' must be an integer greater than t_start."

    if not isinstance(n_steps, int) or n_steps < 10 or n_steps > 1000:
        return "Error: 'n_steps' must be an integer between 10 and 1000."

    payload = {
        "antimony": antimony,
        "t_start": t_start,
        "t_end": t_end,
        "n_steps": n_steps,
    }
    data = await call_local_api("POST", "/simulate", json=payload)

    if not data:
        return "❌ Simulation failed or endpoint unreachable. The server may be offline or not responding."

    if "columns" not in data:
        return "❌ Simulation failed to return expected data format. Server response: " + str(data)

    # Convert to TSV for easy reading inside chat
    header = "\t".join(data["columns"])
    rows = ["\t".join(map(str, row)) for row in data["data"]]
    return "\n".join([header] + rows)


# ----------------------------------------------------------------------
#  Entrypoint
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Make sure your Flask app is running *before* starting FastMCP.
    mcp.run(transport="stdio")