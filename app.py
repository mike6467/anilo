import os

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


@app.get("/")
def home():
    return jsonify({
        "status": "success",
        "message": "claimtoken API is running."
    })


@app.post("/submit")
def submit():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return jsonify({
            "status": "error",
            "message": "Supabase environment variables are not configured."
        }), 500

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON body."
        }), 400

    kheed = data.get("kheed")

    if not kheed:
        return jsonify({
            "status": "error",
            "message": "Missing 'kheed'."
        }), 400

    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/claimtoken",
            headers={
                "apikey": SUPABASE_KEY,
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json={
                "kheed": kheed
            },
            timeout=15,
        )

    except requests.RequestException:
        return jsonify({
            "status": "error",
            "message": "Could not connect to Supabase."
        }), 502

    if response.status_code in (200, 201):
        return "", 204

    return jsonify({
        "status": "failed",
        "details": response.text,
    }), response.status_code


handler = app
