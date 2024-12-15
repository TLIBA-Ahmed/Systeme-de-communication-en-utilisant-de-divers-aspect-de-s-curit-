from azure.storage.blob import BlobServiceClient
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

# Configuration
connection_string = "DefaultEndpointsProtocol=https;AccountName=rbaccode;AccountKey=xUqCGlnIO24BwTccYOJwq5wTlVn5IZDM8DXoc+7eb4IEKUFVl2VssD/s/Prjd2L+/0nOLspZADjA+ASt3/6drA==;EndpointSuffix=core.windows.net"  # Remplacez par votre chaîne de connexion
container_name = "coderbac"
blob_name = "ahmed.txt"

# Secret à stocker
secret = "IyByYmFjX3V0aWxzLnB5ClJPTEVTX1BFUk1JU1NJT05TID0gewogICAgImFkbWluIjogWyJkZWNyeXB0Il0sICAjIFNldWxzIGxlcyBhZG1pbnMgcGV1dmVudCBkw4PCqWNyeXB0ZXIKICAgICJ1c2VyIjogW10gICMgTGVzIHV0aWxpc2F0ZXVycyBuJ29udCBwYXMgY2V0dGUgcGVybWlzc2lvbgp9CgojIFLDg8K0bGUgZGUgbCd1dGlsaXNhdGV1ciBhY3R1ZWwKY3VycmVudF91c2VyX3JvbGUgPSAiYWRtaW4iICAjIENoYW5nZXogZW4gInVzZXIiIHBvdXIgdGVzdGVyIGxlIGNhcyBzYW5zIHBlcm1pc3Npb24KCmRlZiBoYXNfcGVybWlzc2lvbihhY3Rpb24pOgogICAgIiIiCiAgICBWw4PCqXJpZmllIHNpIGwndXRpbGlzYXRldXIgYWN0dWVsIGEgbGEgcGVybWlzc2lvbiBkJ2VmZmVjdHVlciB1bmUgYWN0aW9uIGRvbm7Dg8KpZS4KICAgICIiIgogICAgcGVybWlzc2lvbnMgPSBST0xFU19QRVJNSVNTSU9OUy5nZXQoY3VycmVudF91c2VyX3JvbGUsIFtdKQogICAgcmV0dXJuIGFjdGlvbiBpbiBwZXJtaXNzaW9ucw=="

# Clé et IV pour AES (doivent être gérés de manière sécurisée)
aes_key = os.urandom(32)  # Clé AES de 256 bits
aes_iv = os.urandom(16)   # IV (vecteur d'initialisation)

# Fonction pour chiffrer le secret
def encrypt_secret(secret, key, iv):
    # Padding pour AES
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_secret = padder.update(secret.encode()) + padder.finalize()

    # Chiffrement
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted_secret = encryptor.update(padded_secret) + encryptor.finalize()

    return encrypted_secret

# Fonction pour déchiffrer le secret
def decrypt_secret(encrypted_secret, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_secret = decryptor.update(encrypted_secret) + decryptor.finalize()

    # Retirer le padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    secret = unpadder.update(padded_secret) + unpadder.finalize()

    return secret.decode()

# Chiffrer le secret
encrypted_secret = encrypt_secret(secret, aes_key, aes_iv)

# Charger le secret chiffré dans Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# Charger les données dans le blob
blob_client.upload_blob(encrypted_secret, overwrite=True)
print(f"Secret chiffré chargé dans le blob : {blob_name}")

# Récupérer et déchiffrer le secret
downloaded_secret = blob_client.download_blob().readall()
decrypted_secret = decrypt_secret(downloaded_secret, aes_key, aes_iv)
print(f"Secret déchiffré : {decrypted_secret}")
