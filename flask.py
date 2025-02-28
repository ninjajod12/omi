import os
import subprocess
import socket
import time
import requests
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# Auto-detect public IP
def get_public_ip():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except Exception:
        return "Unable to detect public IP"

vps_ip = get_public_ip()

@app.route('/run_Sid', methods=['POST'])
def run_sid():
    data = request.get_json()
    ip = data.get("ip")
    port = data.get("port")
    duration = data.get("time")
    packet_size = data.get("packet_size")
    threads = data.get("threads")

    if not (ip and port and duration and packet_size and threads):
        return jsonify({"error": "Missing required parameters (ip, port, time, packet_size, threads)"}), 400

    try:
        result = subprocess.run(
            ["./ii2", ip, str(port), str(duration), str(packet_size), str(threads)],
            capture_output=True, text=True
        )

        output = result.stdout
        error = result.stderr
        return jsonify({"output": output, "error": error})

    except Exception as e:
        return jsonify({"error": f"Failed to run Sid: {str(e)}"}), 500

def keep_alive():
    while True:
        print("Bot is running...")
        time.sleep(60)

if __name__ == '__main__':
    # Flask URL Print Fix
    if vps_ip == "Unable to detect public IP":
        print("⚠ Warning: Could not detect public IP. Using local network IP.")
        vps_ip = socket.gethostbyname(socket.gethostname())

    print(f"✅ Server running on: http://{vps_ip}:5000")

    threading.Thread(target=keep_alive, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000)  # Listen on all interfaces
