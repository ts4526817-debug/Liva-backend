from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Render पर Environment Variable में डालना होगा
OPENROUTER_API_KEY = os.getenv("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", "your_api_key_here")

@app.route("/")
def home():
    return {"message": "Student AI Notes Backend is running!"}

@app.route("/notes", methods=["POST"])
def notes():
    data = request.get_json()
    topic = data.get("topic", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are an AI assistant for students.
    Topic: {topic}

    Give the answer in this exact format:
    1. Definition (2–3 lines, simple).
    2. Short memorable scoring note (4–6 lines, exam-ready).
    3. Key Points (3–5 bullets).
    """

    payload = {
        "model": "openai/gpt-3.5-turbo",  # चाहो तो gpt-4 या कोई भी model चुन सकते हो
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=headers, json=payload)
        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        return jsonify({"notes": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
