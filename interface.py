import json
import os
from cryptography.fernet import Fernet
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QTextEdit, QMenuBar, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
import socket
import sys
import threading


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


class ListenerThread(QThread):
    message_received = Signal(str)

    def __init__(self, socket_obj):
        super().__init__()
        self.socket = socket_obj
        self.running = True

    def run(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.message_received.emit(message)
            except Exception as e:
                print(f"Erreur de réception : {e}")
                break

    def stop(self):
        self.running = False
        self.socket.close()


class ChatWindow(QWidget):
    def __init__(self, title, mode):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(600, 500)
        self.mode = mode  # "client" ou "server"
        self.listener = None
        self.client_socket = None
        self.conversation_file = "server_conversation.json"
        self.key = load_key()
        self.cipher = Fernet(self.key)
        self.conversation_data = self.load_conversation_file()
        self.setup_ui()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.mode == "server":
            self.setup_server()
        else:
            self.setup_client()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # En-tête
        self.header_label = QLabel(f"Espace {self.mode.capitalize()}")
        self.header_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)

        # Zone de discussion
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: #F0F0F0; border: none; padding: 5px; border-radius: 10px;"
        )

        # Champ d'envoi de message
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Tapez votre message ici...")

        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_message)

        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)

        # Ajouter au layout principal
        layout.addWidget(self.header_label)
        layout.addWidget(self.chat_display)
        layout.addLayout(input_layout)

        self.setLayout(layout)

    def setup_server(self):
        try:
            self.socket.bind(("127.0.0.1", 12345))
            self.socket.listen(1)
            self.chat_display.append("Serveur en attente de connexion...")
            threading.Thread(target=self.accept_connection, daemon=True).start()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du démarrage du serveur : {e}")

    def accept_connection(self):
        try:
            self.client_socket, addr = self.socket.accept()
            self.chat_display.append(f"Client connecté depuis {addr}")
            self.listener = ListenerThread(self.client_socket)
            self.listener.message_received.connect(self.receive_message)
            self.listener.start()
        except Exception as e:
            self.chat_display.append(f"Erreur de connexion : {e}")

    def setup_client(self):
        try:
            self.socket.connect(("127.0.0.1", 12345))
            self.chat_display.append("Connecté au serveur.")
            self.listener = ListenerThread(self.socket)
            self.listener.message_received.connect(self.receive_message)
            self.listener.start()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de se connecter au serveur : {e}")

    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            encrypted_message = self.cipher.encrypt(message.encode()).decode()
            if self.mode == "server":
                self.chat_display.append(f"<div style='text-align: right; background: #0078D7; color: white; "
                                         f"padding: 5px; border-radius: 10px;'>Serveur : {message}</div>")
                self.client_socket.send(encrypted_message.encode())
                self.save_message("server", encrypted_message)
            else:
                self.chat_display.append(f"<div style='text-align: right; background: #0078D7; color: white; "
                                         f"padding: 5px; border-radius: 10px;'>Client : {message}</div>")
                self.socket.send(encrypted_message.encode())
                self.save_message("client", encrypted_message)
            self.message_input.clear()

    def receive_message(self, encrypted_message):
        decrypted_message = self.cipher.decrypt(encrypted_message.encode()).decode()
        self.chat_display.append(f"<div style='text-align: left; background: #E0E0E0; color: black; "
                                 f"padding: 5px; border-radius: 10px;'>{decrypted_message}</div>")
        if self.mode == "server":
            self.save_message("client", encrypted_message)
        else:
            self.save_message("server", encrypted_message)

    def load_conversation_file(self):
        if os.path.exists(self.conversation_file):
            with open(self.conversation_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_message(self, sender, encrypted_message):
        entry = {"from": sender, "message": encrypted_message}
        self.conversation_data.append(entry)
        with open(self.conversation_file, "w", encoding="utf-8") as file:
            json.dump(self.conversation_data, file, ensure_ascii=False, indent=4)

    def closeEvent(self, event):
        if self.listener:
            self.listener.stop()
        self.socket.close()
        super().closeEvent(event)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion Utilisateur")
        self.resize(400, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        header = QLabel("Connexion")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(header)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        users_db = {
            "admin": {"password": "admin123", "role": "admin"},
            "user": {"password": "user123", "role": "user"},
        }

        if username in users_db and users_db[username]["password"] == password:
            self.open_main_window(users_db[username]["role"])
        else:
            QMessageBox.critical(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def open_main_window(self, role):
        self.main_window = MainWindow(role)
        self.main_window.show()
        self.close()


class MainWindow(QWidget):
    def __init__(self, role):
        super().__init__()
        self.setWindowTitle("Serveur-Client Chat")
        self.resize(400, 300)
        self.role = role
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        header = QLabel("Bienvenue dans le Chat Serveur-Client")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)

        button_layout = QHBoxLayout()
        client_button = QPushButton("Ouvrir Espace Client")
        server_button = QPushButton("Ouvrir Espace Serveur")

        client_button.clicked.connect(lambda: self.open_chat_window("client"))
        server_button.clicked.connect(lambda: self.open_chat_window("server"))

        # Boutons Retour et Quitter
        utility_layout = QHBoxLayout()
        back_button = QPushButton("Retour")
        back_button.clicked.connect(self.go_back_to_login)

        quit_button = QPushButton("Quitter")
        quit_button.clicked.connect(self.quit_application)

        button_layout.addWidget(client_button)
        button_layout.addWidget(server_button)
        utility_layout.addWidget(back_button)
        utility_layout.addWidget(quit_button)

        layout.addWidget(header)
        layout.addLayout(button_layout)
        layout.addLayout(utility_layout)
        self.setLayout(layout)

    def open_chat_window(self, mode):
        self.chat_window = ChatWindow(f"Espace {mode.capitalize()}", mode)
        self.chat_window.show()

    def go_back_to_login(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def quit_application(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
