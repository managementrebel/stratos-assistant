import os
from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def health():
        return "Stratos Assistant is up."

    @app.post("/chat")
    def chat():
        # Load env at request time so missing keys don't crash the worker
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return jsonify({"error": "GOOGLE_API_KEY not set in environment"}), 500

        import google.generativeai as genai
        genai.configure(api_key=api_key)

        model = os.getenv("MODEL_ID", "models/gemini-1.5-flash")
        data = request.get_json(silent=True) or {}
        text = data.get("q", "Explain Stratos packages in under 120 words.")
        resp = genai.chat(model=model, messages=[{"role": "user", "content": text}])
        return jsonify({"answer": resp.last})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
