import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

MODEL = os.environ.get("MODEL_ID", "models/gemini-1.5-flash")
API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

@app.get("/")
def health():
  return "Stratos Assistant is up."

@app.post("/chat")
def chat():
  data = request.get_json(silent=True) or {}
  text = data.get("q", "Explain Stratos packages in under 120 words.")
  resp = genai.chat(model=MODEL, messages=[{"role":"user","content":text}])
  return jsonify({"answer": resp.last})
