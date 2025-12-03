from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

DATA_PATH = "/data/message.txt"


def read_message():
    """
    If DATA_PATH exists, read and return the text inside.
    If it doesn't exist, return an empty string.
    """
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, 'r') as f:
                return f.read().strip()
        except IOError:
            return ""
    return ""


def write_message(msg: str):
    """
    V2: Writes msg to file, appending a timestamp[cite: 81].
    Format: "<message> (updated at YYYY-MM-DD HH:MM:SS)" [cite: 82]
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    v2_msg = f"{msg} (updated at {timestamp})"
    
    
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True) 
    with open(DATA_PATH, 'w') as f:
        f.write(v2_msg)


@app.route("/api/message", methods=["GET"])
def get_message():
    """
    Returns { "message": <stored message> } as JSON[cite: 24].
    The stored message now includes the V2 timestamp.
    """
    stored_message = read_message()
    if not stored_message:
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stored_message = f"Hello! This is the default v2 message. (updated at {timestamp})"
        
    return jsonify({"message": stored_message})


@app.route("/api/message", methods=["POST"])
def update_message():
    """
    Accepts { "message": "New message here" } and saves it with a timestamp [cite: 25-29, 81].
    Returns { "status": "ok" }.
    """
    data = request.get_json()
    new_message = data.get("message", "")
    if new_message:
        write_message(new_message)
        
    return jsonify({"status": "ok"})


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    V2: New endpoint for health check[cite: 84].
    Must return { "status": "healthy" }[cite: 85, 86].
    """
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
