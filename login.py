import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
import sqlite3

# Classe principale pour la fenêtre de l'application (interface principale)
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface principale")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()
        welcome_label = QLabel("Bienvenue dans l'interface principale!")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Exemple de bouton
        play_button = QPushButton("Commencer le jeu")
        layout.addWidget(play_button)

        self.setLayout(layout)

# Classe pour la fenêtre de connexion
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(400, 350)

        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                color: #333333;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                min-height: 45px;
                border-radius: 10px;
                background-color: #FFFFFF;
                padding-left: 15px;
                border: 2px solid #B0BEC5;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:pressed {
                background-color: #2C6A29;
            }
        """)

        layout = QVBoxLayout()

        # Champs d'entrée
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Entrez votre email")
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        layout.addWidget(QLabel("Mot de passe"))
        layout.addWidget(self.password_input)

        # Boutons
        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        signup_button = QPushButton("S'inscrire")
        signup_button.clicked.connect(self.open_signup)
        layout.addWidget(signup_button)

        reset_button = QPushButton("Mot de passe oublié ?")
        reset_button.clicked.connect(self.reset_password)
        layout.addWidget(reset_button)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        # Vérification dans la base de données
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Succès", "Connexion réussie!")
            self.open_main_app()  # Ouvrir l'interface principale
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def open_main_app(self):
        self.close()  # Fermer la fenêtre de connexion
        self.main_app = MainApp()
        self.main_app.show()

    def open_signup(self):
        signup_window = QWidget()
        signup_window.setWindowTitle("Inscription")
        signup_window.setFixedSize(400, 350)

        signup_layout = QFormLayout()

        # Champs d'inscription
        name_input = QLineEdit()
        name_input.setPlaceholderText("Entrez votre nom")
        signup_layout.addRow("Nom", name_input)

        surname_input = QLineEdit()
        surname_input.setPlaceholderText("Entrez votre prénom")
        signup_layout.addRow("Prénom", surname_input)

        phone_input = QLineEdit()
        phone_input.setPlaceholderText("Entrez votre numéro")
        signup_layout.addRow("Numéro", phone_input)

        email_input_signup = QLineEdit()
        email_input_signup.setPlaceholderText("Entrez votre email")
        signup_layout.addRow("Email", email_input_signup)

        password_input_signup = QLineEdit()
        password_input_signup.setEchoMode(QLineEdit.Password)
        password_input_signup.setPlaceholderText("Entrez votre mot de passe")
        signup_layout.addRow("Mot de passe", password_input_signup)

        def submit_signup():
            name = name_input.text()
            surname = surname_input.text()
            phone = phone_input.text()
            email = email_input_signup.text()
            password = password_input_signup.text()

            # Enregistrer l'utilisateur dans la base de données SQLite
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, surname, phone, email, password) VALUES (?, ?, ?, ?, ?)",
                           (name, surname, phone, email, password))
            conn.commit()
            conn.close()

            QMessageBox.information(signup_window, "Succès", "Inscription réussie!")
            signup_window.close()

        signup_button = QPushButton("S'inscrire")
        signup_button.clicked.connect(submit_signup)
        signup_layout.addWidget(signup_button)

        signup_window.setLayout(signup_layout)
        signup_window.setStyleSheet(self.styleSheet())  # Appliquer le style actuel
        signup_window.show()

    def reset_password(self):
        email = self.email_input.text()

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Réinitialisation", "Un e-mail avec un code de réinitialisation a été envoyé.")
        else:
            QMessageBox.warning(self, "Erreur", "Aucun utilisateur trouvé avec cet e-mail.")

# Initialisation de la base de données
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    phone TEXT,
    email TEXT UNIQUE,
    password TEXT)''')
conn.commit()
conn.close()

# Lancer l'application
app = QApplication(sys.argv)
login_window = LoginWindow()
login_window.show()
sys.exit(app.exec())
