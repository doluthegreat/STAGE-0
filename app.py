import requests
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

GENDERIZE_URL = "https://api.genderize.io/"

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "Genderize API is running"}), 200
@app.route("/api/classify", methods=["GET"])
def classify():
    name = request.args.get("name")

    if name is None or name.strip() == "":
        return jsonify({"status": "error", "message": "Missing or empty 'name' parameter"}), 400

    if not isinstance(name, str):
        return jsonify({"status": "error", "message": "'name' must be a string"}), 422

    
    try:
        response = requests.get(GENDERIZE_URL, params={"name": name}, timeout=5)
        response.raise_for_status()
        api_data = response.json()
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Genderize API timed out"}), 502
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "error", "message": "Could not reach Genderize API"}), 502
    except Exception:
        return jsonify({"status": "error", "message": "Unexpected error calling Genderize API"}), 500

    
    gender = api_data.get("gender")
    count = api_data.get("count", 0)

    if gender is None or count == 0:
        return jsonify({
            "status": "error",
            "message": "No prediction available for the provided name"
        }), 200

    
    probability = api_data.get("probability", 0)
    sample_size = count
    is_confident = probability >= 0.7 and sample_size >= 100
    processed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return jsonify({
        "status": "success",
        "data": {
            "name": api_data.get("name", name),
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        }
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)