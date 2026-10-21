
import hashlib
import os
import threading
from datetime import datetime, timezone

import streamlit as st
from flask import Flask, jsonify, request
from werkzeug.serving import make_server

st.set_page_config(
    page_title="Termux Connection Test",
    page_icon="🔗",
    layout="centered",
)

# -------------------------------
# API server for ordinary test data
# -------------------------------

api = Flask(__name__)

MAX_MESSAGE_BYTES = 64 * 1024


@api.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "Termux Connection Test",
        "time_utc": datetime.now(timezone.utc).isoformat(),
    })


@api.route("/api/echo", methods=["POST"])
def echo():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Send JSON with Content-Type: application/json",
        }), 415

    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return jsonify({
            "status": "error",
            "message": "Expected a JSON object",
        }), 400

    message = body.get("message", "")

    if not isinstance(message, str):
        return jsonify({
            "status": "error",
            "message": "The message must be text",
        }), 400

    encoded = message.encode("utf-8")

    if len(encoded) > MAX_MESSAGE_BYTES:
        return jsonify({
            "status": "error",
            "message": "Message is too large",
        }), 413

    return jsonify({
        "status": "success",
        "message_received": message,
        "bytes_received": len(encoded),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "server_time_utc": datetime.now(timezone.utc).isoformat(),
    })


# -------------------------------
# Start the local API server once
# -------------------------------

@st.cache_resource
def start_api_server():
    server = make_server("0.0.0.0", 8502, api, threaded=True)
    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()
    return server


st.title("🔗 Termux ↔ Streamlit")
st.write("HTTP connection and data-integrity test")

st.info(
    "The API provides /api/health and /api/echo "
    "for ordinary test messages."
)

st.subheader("Local test")

message = st.text_input(
    "Test message",
    value="Hello from Streamlit",
)

if st.button("Test message"):
    encoded = message.encode("utf-8")
    st.json({
        "status": "success",
        "message": message,
        "bytes": len(encoded),
        "sha256": hashlib.sha256(encoded).hexdigest(),
    })

st.divider()
st.subheader("API endpoints")

st.code(
    "GET  /api/health\n"
    "POST /api/echo"
)

st.warning(
    "Hosting note: Streamlit Community Cloud normally exposes "
    "the Streamlit web application, not arbitrary extra ports. "
    "The Flask API on port 8502 may therefore not be reachable "
    "through your public Streamlit URL."
)
