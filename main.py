# main.py
from PySide6.QtWidgets import QApplication, QMainWindow,QDialog
from login import LoginWindow
from ll import Entrainement

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Fitness")
        self.setFixedSize(800, 600)

        # Affichage de la fenêtre de login
        self.login_window = LoginWindow()
        if self.login_window.exec() == QDialog.Accepted:
            self.open_entrainement_window()

    def open_entrainement_window(self):
        self.entrainement_window = Entrainement()
        self.entrainement_window.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
