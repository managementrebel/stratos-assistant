FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV PORT=8080
# Gunicorn will serve the Flask app object named "app" from main.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
