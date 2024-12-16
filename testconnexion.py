import socket

host = "127.0.0.1"
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Serveur en écoute sur {host}:{port}")

while True:
    print("En attente de connexion...")
    conn, addr = server_socket.accept()
    print(f"Connexion acceptée depuis {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            print(f"Connexion fermée par {addr}")
            break
        print(f"Données reçues de {addr} : {data.decode()}")
        conn.send("Message bien reçu")
    conn.close()
