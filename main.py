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
            return jsonify({"error": "GOOGLE_API_KEY missing"}), 500

        genai.configure(api_key=api_key)

        model_name = os.getenv("MODEL_ID", "models/gemini-1.5-flash")
        model = genai.GenerativeModel(model_name)

        data = request.get_json(silent=True) or {}
        user_text = data.get("q", "Say hello to me in one short sentence.")

        resp = model.generate_content(user_text)
        # resp.text is the simplest way to return content
        return jsonify({"answer": resp.text})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))