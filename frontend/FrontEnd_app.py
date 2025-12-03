from flask import Flask, render_template, request, redirect
import requests
import re

app = Flask(__name__)


BACKEND_URL = "http://backend:5001"


def extract_message_and_timestamp(full_message: str):
    
    match = re.search(r'\((updated at\s)(.*)\)', full_message)
    
    if match:
        timestamp = match.group(2) 
        message = full_message.replace(f" (updated at {timestamp})", "").strip()
        return message, timestamp
    
    # Fallback for V1 format or if timestamp is missing
    return full_message, ""


@app.route("/", methods=["GET"])
def index():
    
    current_message = "Could not connect to backend."
    last_updated_at = ""
    
    try:
        # Send GET request to fetch the message (which now includes the timestamp)
        response = requests.get(f"{BACKEND_URL}/api/message")
        response.raise_for_status() 
        
        data = response.json()
        full_message = data.get("message", "Message not found in backend response.")
        
        # Parse the message and timestamp
        current_message, last_updated_at = extract_message_and_timestamp(full_message)
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to backend: {e}")
        
    return render_template("index.html", 
                           current_message=current_message, 
                           last_updated_at=last_updated_at)


@app.route("/update", methods=["POST"])
def update():
    """
    Saves the new message to the backend (which automatically adds the V2 timestamp).
    """
    new_message = request.form.get("new_message")
    payload = {"message": new_message}
    
    try:
        requests.post(f"{BACKEND_URL}/api/message", json=payload).raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error updating message in backend: {e}")
        
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
