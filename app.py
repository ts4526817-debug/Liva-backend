# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/notes", methods=["POST"])
def notes():
    data = request.get_json()
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "Topic required"}), 400

    try:
        # OpenRouter GPT call
        headers = {
            "Authorization": f"Bearer {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}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4.1-mini",
            "input": f"Generate short, scoring, memorable, and easy study notes for the topic: {topic}. Include definition and key points."
        }
        response = requests.post("https://openrouter.ai/api/v1/completions", json=payload, headers=headers, timeout=25)
        response.raise_for_status()
        result = response.json()
        notes_text = result["completion"]["output_text"] if "completion" in result else "No notes generated."
        return jsonify({"notes": notes_text})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
