from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests

# ===========================
# ⚙️ App Setup
# ===========================
app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes and origins

# ===========================
# 🔐 Configuration (from Render environment variables)
# ===========================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ===========================
# 🏠 Home Route
# ===========================
@app.route("/")
def home():
    return "✅ claimtoken API is running."

# ===========================
# 📩 Submit Route (write-only)
# ===========================
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    kheed = data.get("kheed")
    if not kheed:
        return jsonify({"error": "Missing 'kheed'"}), 400

    # ===========================
    # 🚀 Send data to Supabase
    # ===========================
    try:
        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/claimtoken",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            },
            json={"kheed": kheed}
        )

        if res.status_code in (200, 201):
            return jsonify({
                "status": "success",
                "inserted": {"kheed": kheed}
            }), res.status_code
        else:
            return jsonify({
                "status": "failed",
                "details": res.text
            }), res.status_code

    except Exception as e:
        return jsonify({
            "status": "error",
            "details": str(e)
        }), 500

# ===========================
# ▶️ Run Server
# ===========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5111)
