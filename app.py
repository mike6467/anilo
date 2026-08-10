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
    # Check configuration first
    if not SUPABASE_URL or not SUPABASE_KEY:
        return jsonify({
            "status": "error",
            "message": "Supabase environment variables are not configured."
        }), 500

    # Read JSON body
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON body."
        }), 400

    # Get kheed
    kheed = data.get("kheed")

    if not kheed:
        return jsonify({
            "status": "error",
            "message": "Missing 'kheed'."
        }), 400

    # Send data to Supabase
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/claimtoken",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            },
            json={
                "kheed": kheed
            },
            timeout=15,
        )

    except requests.RequestException as error:
        return jsonify({
            "status": "error",
            "message": "Could not connect to Supabase.",
            "details": str(error),
        }), 502

    # Supabase successfully inserted the record
    if response.status_code in (200, 201):
        return jsonify({
            "status": "success",
            "inserted": {
                "kheed": kheed
            }
        }), response.status_code

    # Supabase returned an error
    return jsonify({
        "status": "failed",
        "details": response.text,
    }), response.status_code


# Netlify uses this Flask application as the function handler.
handler = app
