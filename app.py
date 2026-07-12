"""
Josh AI — Flask backend
-----------------------
Serves the static frontend and exposes a /api/config endpoint so that
IBM watsonx Orchestrate credentials stay server-side (never hardcoded in JS).

Usage:
    pip install -r requirements.txt
    cp .env.example .env          # then fill in your values
    python app.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, send_from_directory, url_for
from flask_cors import CORS

# ── Load environment variables from .env ──────────────────────────────────
load_dotenv()

# ── App factory ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")
CORS(app)  # allow local dev tools / reverse-proxies to hit the API


# ── Helpers ───────────────────────────────────────────────────────────────
def _page(filename: str):
    """Send an HTML page from the project root."""
    return send_from_directory(BASE_DIR, filename)


def _require_env(key: str) -> str:
    """Return an env value or raise a clear error if missing."""
    val = os.environ.get(key, "").strip()
    if not val:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            "Copy .env.example to .env and fill in your credentials."
        )
    return val


# ── Page routes ───────────────────────────────────────────────────────────
@app.route("/")
def root():
    return redirect(url_for("home"))


@app.route("/index")
@app.route("/index.html")
def home():
    return _page("index.html")


@app.route("/chat")
@app.route("/chat.html")
def chat():
    return _page("chat.html")


@app.route("/about")
@app.route("/about.html")
def about():
    return _page("about.html")


@app.route("/Menu.html")
@app.route("/menu")
def menu():
    return redirect(url_for("home"))


# ── API routes ────────────────────────────────────────────────────────────
@app.route("/api/config")
def api_config():
    """
    Return the watsonx Orchestrate configuration as JSON.
    The frontend fetches this once on page load so credentials
    never need to be hardcoded in the HTML/JS files.
    """
    return jsonify({
        "orchestrationID": _require_env("ORCHESTRATION_ID"),
        "hostURL":         _require_env("HOST_URL"),
        "deploymentPlatform": os.environ.get("DEPLOYMENT_PLATFORM", "ibmcloud"),
        "crn":             _require_env("CRN"),
        "agentId":         _require_env("AGENT_ID"),
    })


@app.route("/health")
def health():
    """Liveness probe."""
    return jsonify({"status": "ok", "app": "Josh AI"}), 200


# ── Entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"\n  Josh AI  →  http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
