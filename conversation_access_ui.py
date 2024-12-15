from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
import json
from rbac_utils_decrypted import has_permission
from threading import Thread
import socket

app = Flask(__name__)

# Charger la clé pour le chiffrement

def load_key(file_path="key.key"):
    with open(file_path, "rb") as key_file:
        return key_file.read()

def decrypt_message(message, cipher):
    return cipher.decrypt(message.encode()).decode()

def encrypt_message(message, cipher):
    return cipher.encrypt(message.encode()).decode()

key = load_key()
cipher = Fernet(key)

# Stockage temporaire des messages
conversation = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global conversation
    data = request.json
    message = data.get('message', '')
    if message:
        try:
            encrypted_message = encrypt_message(message, cipher)
            client_socket.send(encrypted_message.encode())
            conversation.append({"from": "Vous", "message": message})
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "Empty message"})

@app.route('/receive_messages', methods=['GET'])
def receive_messages():
    global conversation
    try:
        encrypted_response = client_socket.recv(1024).decode()
        decrypted_response = decrypt_message(encrypted_response, cipher)
        conversation.append({"from": "Serveur", "message": decrypted_response})
        return jsonify({"status": "success", "message": decrypted_response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/decrypt_conversation', methods=['GET'])
def decrypt_conversation():
    if not has_permission("decrypt"):
        return jsonify({"status": "error", "message": "Permission denied"})

    try:
        with open("server_conversation.json", "r", encoding="utf-8") as file:
            encrypted_conversation = json.load(file)
        
        decrypted_conversation = []
        for message in encrypted_conversation:
            decrypted_message = decrypt_message(message["message"], cipher)
            decrypted_conversation.append({"from": message["from"], "message": decrypted_message})

        return jsonify({"status": "success", "conversation": decrypted_conversation})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))

    Thread(target=lambda: app.run(debug=True, use_reloader=False), daemon=True).start()
