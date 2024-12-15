import json
from cryptography.fernet import Fernet
from rbac_utils_decrypted import has_permission
import arabic_reshaper
from bidi.algorithm import get_display

def load_key(file_path="key.key"):
    """
    Charge la clé de cryptage depuis un fichier.
    """
    with open(file_path, "rb") as key_file:
        return key_file.read()

def format_arabic_text(text):
    
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def decrypt_conversation(file_path="conversation.json", key_path="key.key"):
    
    # Décrypte une conversation depuis un fichier JSON.
    
    #vérifier si l'utilisateur a la permission
    if not has_permission("decrypt"):
        print("Accès refusé : Vous n'avez pas la permission de décrypter la conversation.")
        return

    
    key = load_key(key_path)
    cipher = Fernet(key)

    # Charger la conversation cryptée
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            encrypted_conversation = json.load(f)
    except FileNotFoundError:
        print(f"Fichier {file_path} introuvable.")
        return

    # Décrypter chaque message
    decrypted_conversation = []
    for message in encrypted_conversation:
        decrypted_text = cipher.decrypt(message["message"].encode()).decode()
        formatted_text = format_arabic_text(decrypted_text)
        decrypted_conversation.append({"from": message["from"], "message": formatted_text})

    # Afficher la conversation
    print("Conversation décryptée :")
    for msg in decrypted_conversation:
        print(f"{msg['from'].capitalize()}: {msg['message']}")

if __name__ == "__main__":
    # Exemple d'utilisation
    decrypt_conversation("server_conversation.json")
