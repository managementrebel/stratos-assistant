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
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return jsonify({"error": "Missing GOOGLE_API_KEY"}), 500

        genai.configure(api_key=api_key)
        model_id = os.getenv("MODEL_ID", "models/gemini-1.5-flash")
        model = genai.GenerativeModel(model_id)

        try:
            data = request.get_json(silent=True) or {}
            user_text = data.get("q", "Say hello to me")

            # ✅ Correct structure for Gemini
            response = model.generate_content([{"role": "user", "parts": [{"text": user_text}]}])
            return jsonify({"answer": response.text})

        except Exception as e:
            # capture the real Python error in logs
            return jsonify({"error": str(e)}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))