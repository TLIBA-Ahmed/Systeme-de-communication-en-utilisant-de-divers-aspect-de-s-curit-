import socket
from audio_to_text import transform_audio_into_text
import arabic_reshaper
from bidi.algorithm import get_display
from cryptography.fernet import Fernet
import json
import os

# Charger ou générer une clé
def load_key(file_path="key.key"):
    if os.path.exists(file_path):
        with open(file_path, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(file_path, "wb") as key_file:
            key_file.write(key)
        return key

# Initialiser le chiffreur
key = load_key()
cipher = Fernet(key)

# Sauvegarder une conversation cryptée
def save_conversation(conversation, file_path="server_conversation.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=4)

def start_server():
    host = '127.0.0.1'
    port = 12345

    # Création du socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Serveur en attente de connexion...")
    conversation = []  # Stocker les messages

    conn, addr = server_socket.accept()
    print(f"Connexion établie avec {addr}")

    while True:
        # Recevoir le message crypté
        encrypted_message = conn.recv(1024).decode()
        decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
        conversation.append({"from": "client", "message": encrypted_message})

        if decrypted_message.lower() == 'exit':
            print("Connexion terminée par le client.")
            break

        print(f"Client: {decrypted_message}")

        # Envoyer une réponse
        response = transform_audio_into_text()
        encrypted_response = cipher.encrypt(response.encode()).decode()
        conn.send(encrypted_response.encode())
        conversation.append({"from": "server", "message": encrypted_response})

        if response.lower() == 'exit':
            print("Vous avez terminé la connexion.")
            break

    save_conversation(conversation)
    conn.close()

if __name__ == "__main__":
    start_server()
