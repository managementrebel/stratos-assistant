import os
from flask import Flask, request, jsonify
import google.generativeai as genai

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def health():
        return "Stratos Assistant is up."

    @app.post("/chat")
    def chat():
        data = request.get_json(silent=True) or {}
        text = data.get("q", "Hello!")

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return jsonify({"error": "GOOGLE_API_KEY missing"}), 500

        genai.configure(api_key=api_key)
        model_id = os.getenv("MODEL_ID", "gemini-1.5-flash")
        model = genai.GenerativeModel(model_id)

        resp = model.generate_content(text)
        return jsonify({"answer": resp.text})

    return app

app = create_app()