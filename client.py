import socket
import arabic_reshaper
from bidi.algorithm import get_display
from cryptography.fernet import Fernet
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


key = load_key()
cipher = Fernet(key)

def start_client():
    host = '127.0.0.1'  # Adresse IP du serveur
    port = 12345         # Port communication

    # Création du socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connecté au serveur.")
    
    # Stocker les messages
    conversation = []  
    
    while True:
        # Envoyer un message
        message = input("Vous: ")
        encrypted_message = cipher.encrypt(message.encode()).decode()
        client_socket.send(encrypted_message.encode())
        conversation.append({"from": "client", "message": encrypted_message})

        if message.lower() == 'exit':
            print("Vous avez terminé la connexion.")
            break

        # Recevoir une réponse
        encrypted_response = client_socket.recv(1024).decode()
        decrypted_response = cipher.decrypt(encrypted_response.encode()).decode()

        reshaped_response = arabic_reshaper.reshape(decrypted_response)
        bidi_response = get_display(reshaped_response)
        conversation.append({"from": "server", "message": encrypted_response})

        if decrypted_response.lower() == 'exit':
            print("Connexion terminée par le serveur.")
            break

        print(f"Serveur: {bidi_response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
