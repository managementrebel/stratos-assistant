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
        try:
            data = request.get_json(silent=True) or {}
            text = data.get("q") or data.get("message") or "Hello!"

            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return jsonify({"error": "Missing GOOGLE_API_KEY"}), 500

            model_id = os.getenv("MODEL_ID", "models/gemini-1.5-flash")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_id)

            response = model.generate_content(text)

            return jsonify({"answer": response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

app = create_app()