from flask import Flask, jsonify, request
from importlib import import_module
from typing import Dict

app = Flask(__name__)

# Root endpoint
@app.get("/")
def index():
    return jsonify(message="Welcome to the API"), 200


# Basic health-check or “status” endpoint
@app.get("/status")
def status():
    return jsonify(ok=True, message="API is alive"), 200


# Example POST endpoint that echoes JSON back
@app.post("/echo")
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify(received=data, length=len(data)), 200


from importlib import metadata


@app.get("/version")
def version():
    try:
        ver = metadata.version("tellurium")
    except metadata.PackageNotFoundError:
        ver = "not-installed"
    return jsonify(package="tellurium", version=ver), 200


@app.post("/simulate")
def simulate():
    """
    Body JSON:
        {
          "antimony": "<Antimony text>",
          "t_start": 0,
          "t_end":   100,
          "n_steps": 200
        }
    Returns:
        {
          "columns": [...],
          "data":    [[row0], [row1], ...]
        }
    """
    payload = request.get_json(silent=True) or {}
    antimony = payload.get("antimony")
    t0 = int(payload.get("t_start", 0))
    t1 = int(payload.get("t_end", 100))
    n_steps = int(payload.get("n_steps", 100))

    if not antimony:
        return jsonify(error="Field 'antimony' is required."), 400

    # Import tellurium only when needed (avoids startup cost elsewhere)
    try:
        te = import_module("tellurium")
    except ModuleNotFoundError:
        return jsonify(error="Tellurium is not installed on the server"), 500

    try:
        rr = te.loada(antimony)
        result = rr.simulate(t0, t1, n_steps)

        columns = list(result.colnames)
        data = result.tolist()  # numpy ndarray → list of lists

        return jsonify(columns=columns, data=data), 200
    except Exception as exc:
        return jsonify(error=str(exc)), 500


if __name__ == "__main__":
    # • debug=True ⇢ auto-reload on code change
    # • host="0.0.0.0" ⇢ bind all interfaces (LAN) instead of only 127.0.0.1
    app.run(port=5000, debug=True)
