import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QFormLayout, QMessageBox, QDialog
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Qt, QSize
from experta import *
from PySide6.QtGui import QPixmap, QIcon



# Classe pour les informations d'entraînement
class Entrainement(Fact):
    """Informations sur l'entraînement de l'utilisateur."""
    pass

# Classe pour conseiller l'entraînement
class ConseillerEntrainement(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.conseils = []

    @Rule(Entrainement(objectif="perte_de_poids", niveau="debutant"))
    def perte_de_poids_debutant(self):
        self.conseils.append("Commencez par 30 minutes de marche rapide ou de vélo 3 à 4 fois par semaine.")
        self.conseils.append("Ajoutez des exercices au poids du corps comme les squats ou les planches.")

    @Rule(Entrainement(objectif="prise_de_muscle", niveau="avancé"))
    def prise_de_muscle_avance(self):
        self.conseils.append("Faites des séries lourdes avec 6 à 8 répétitions pour des exercices composés.")
        self.conseils.append("Travaillez chaque groupe musculaire au moins deux fois par semaine.")

    @Rule(Entrainement(objectif="maintien", niveau="intermediaire"))
    def maintien_intermediaire(self):
        self.conseils.append("Combinez 3 séances de cardio modéré et 2 séances de musculation légère.")
        self.conseils.append("Ajoutez des étirements ou des cours de yoga pour améliorer la mobilité.")

    @Rule(Entrainement(objectif="perte_de_poids", niveau="intermediaire"))
    def perte_de_poids_intermediaire(self):
        self.conseils.append("Intégrez des séances HIIT (entraînement par intervalles à haute intensité) deux fois par semaine.")
        self.conseils.append("Ajoutez des exercices de musculation pour maintenir votre masse musculaire.")

    @Rule(Entrainement(objectif="prise_de_muscle", niveau="intermediaire"))
    def prise_de_muscle_intermediaire(self):
        self.conseils.append("Concentrez-vous sur des séries de 8 à 12 répétitions avec des poids modérés.")
        self.conseils.append("Ajoutez des exercices d'isolation pour renforcer les muscles spécifiques.")

    @Rule(Entrainement(objectif="perte_de_poids", niveau="debutant", age=P(lambda x: x < 30)))
    def perte_de_poids_jeune_debutant(self):
        self.conseils.append("Ajoutez des sports dynamiques comme la course ou la natation pour accélérer la perte de poids.")

    @Rule(Entrainement(objectif="perte_de_poids", niveau="debutant", age=P(lambda x: x >= 30)))
    def perte_de_poids_adulte_debutant(self):
        self.conseils.append("Privilégiez des activités modérées comme la marche rapide ou le yoga pour éviter les blessures.")

    @Rule(Entrainement(objectif="perte_de_poids", niveau="intermediaire", condition="hypertension"))
    def perte_de_poids_hypertension(self):
        self.conseils.append("Privilégiez des exercices doux comme la marche ou le vélo d'appartement.")
        self.conseils.append("Évitez les activités à haute intensité.")

    @Rule(Entrainement(objectif="prise_de_muscle", niveau="avancé", temps_disponible=P(lambda x: x < 30)))
    def prise_de_muscle_rapide(self):
        self.conseils.append("Faites des circuits courts mais intenses, comme des supersets.")
        self.conseils.append("Concentrez-vous sur les exercices multi-articulaires.")

    @Rule(Entrainement(objectif="prise_de_muscle", niveau="avancé", temps_disponible=P(lambda x: x >= 60)))
    def prise_de_muscle_long(self):
        self.conseils.append("Consacrez du temps à des séries lourdes et des exercices d'isolation.")
        self.conseils.append("Ajoutez des temps de repos plus longs pour optimiser les gains musculaires.")
   
    @Rule(Entrainement(objectif="prise_de_muscle", niveau="intermediaire"))
    def prise_de_muscle_nutrition(self):
        self.conseils.append("Augmentez votre apport en protéines (1,5 à 2 g par kg de poids corporel).")
        self.conseils.append("Intégrez des glucides complexes avant l'entraînement pour l'énergie.")

    @Rule(Entrainement(objectif="perte_de_poids", niveau="intermediaire", sessions_completes=P(lambda x: x >= 5)))
    def progression_intermediaire(self):
        self.conseils.append("Augmentez l'intensité de vos exercices ou la durée des séances.")
        self.conseils.append("Essayez de nouvelles activités comme le spinning ou l'escalade.")


    
    

    def afficher_conseil(self):
        return "\n".join(self.conseils)

# Calcul des besoins en eau
def calculer_eau(poids, entrainements_par_semaine):
    """Calcule la quantité d'eau recommandée (litres/jour)."""
    base_eau = poids * 0.03  # 30 ml d'eau par kg
    extra_eau = entrainements_par_semaine * 0.5  # 500 ml par entraînement
    return round(base_eau + extra_eau, 1)

# Fonction pour sauvegarder les conseils dans un fichier texte
def sauvegarder_conseils(conseils, imc, etat_imc, eau_recommandee, conseils_nutrition):
    with open("conseils_entrainement.txt", "w", encoding="utf-8") as fichier:
        fichier.write(f"IMC : {imc} ({etat_imc})\n")
        fichier.write(f"Eau recommandée : {eau_recommandee} litres/jour\n\n")
        fichier.write("Conseils d'entraînement :\n")
        fichier.write(conseils + "\n\n")
        fichier.write("Conseils Nutritionnels :\n")
        fichier.write(conseils_nutrition)
    QMessageBox.information(window, "Succès", "Les conseils ont été enregistrés dans 'conseils_entrainement.txt'.")



# Fonction pour ouvrir une nouvelle interface d'entraînement avec images différentes
def ouvrir_interface_entrainement(numero_interface):
    interface = QWidget()
    interface.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
    interface.setWindowTitle(f"Interface Entraînement {numero_interface}")
    interface.setFixedSize(400, 500)

    # Style cohérent avec l'interface principale
    interface.setStyleSheet("""
        QWidget {
            background-color: #f0f8ff;
            font-family: Arial, sans-serif;
        }
        QPushButton {
            font-size: 14px;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #4CAF50;
            color: white;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLabel {
            font-size: 14px;
            color: #333;
        }
    """)

    layout = QVBoxLayout(interface)

    # Ajouter une image différente pour chaque interface
    image_label = QLabel()
    image_paths = [
        "exercise1.jpg",  # Image 2
        "exercise2.jpg",  # Image 3
        "exercise3.jpg",  # Image 4
        "exercise4.jpg",  # Image 5
        "exercise5.jpg",
        "exercise6.jpg", 
        "exercise7.jpg" # Image 6
    ]

    # Sélectionner l'image ou utiliser une image par défaut
    if numero_interface <= len(image_paths):
        image_path = image_paths[numero_interface - 1]
    else:
        image_path = "default_image.jpg"  # Image par défaut si le numéro dépasse la liste

    pixmap = QPixmap(image_path)
    if pixmap.isNull():  # Gestion des images manquantes
        pixmap = QPixmap(300, 200)
        pixmap.fill(Qt.gray)  # Image grise par défaut

    pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio)
    image_label.setPixmap(pixmap)
    image_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(image_label, alignment=Qt.AlignCenter)

    # Ajouter un chronomètre de 5 minutes
    countdown_label = QLabel("Temps restant : 5:00")
    countdown_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(countdown_label)

    def start_timer():
        time_left = 300  # 5 minutes en secondes

        def update_timer():
            nonlocal time_left
            if time_left > 0:
                time_left -= 1
                minutes = time_left // 60
                seconds = time_left % 60
                countdown_label.setText(f"Temps restant : {minutes:02}:{seconds:02}")
            else:
                timer.stop()
                QMessageBox.information(interface, "Temps écoulé", "La session d'entraînement est terminée !")

        timer = QTimer(interface)
        timer.timeout.connect(update_timer)
        timer.start(1000)  # Mise à jour toutes les secondes

    # Ajouter un bouton pour démarrer le chronomètre
    start_button = QPushButton("Démarrer le chronomètre")
    start_button.clicked.connect(start_timer)
    layout.addWidget(start_button)

    # Ajouter un bouton pour passer à l'interface suivante
    def ouvrir_suivante():
        if numero_interface < 6:  # Limiter à 6 interfaces
            ouvrir_interface_entrainement(numero_interface + 1)
        else:
            afficher_bilan_utilisation()  # Afficher le bilan après la 6ème interface

    next_button = QPushButton("Next")
    next_button.clicked.connect(ouvrir_suivante)
    layout.addWidget(next_button)

    # Bouton pour fermer l'interface actuelle
    def fermer():
        interface.close()

    close_button = QPushButton("Fermer")
    close_button.clicked.connect(fermer)
    layout.addWidget(close_button)

    interface.setLayout(layout)
    interface.show()


# Fonction pour afficher le bilan d'utilisation et de rendement
def afficher_bilan_utilisation():
    # Créer une fenêtre de bilan qui reste au-dessus de toutes les autres
    bilan_dialog = QDialog(window)
    bilan_dialog.setWindowFlags(
        Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint
    )  # Fenêtre au-dessus des autres
    bilan_dialog.setWindowTitle("Bilan d'Utilisation et Rendement")
    bilan_dialog.setFixedSize(600, 400)

    layout = QVBoxLayout(bilan_dialog)

    # Exemple de contenu pour le bilan
    layout.addWidget(QLabel("Bilan d'Utilisation :"))
    layout.addWidget(QLabel(" sessions d'entraînement complétées avec succès."))  # Mise à jour pour 6 sessions
    layout.addWidget(QLabel("Rendement de l'utilisateur :"))
    layout.addWidget(QLabel("Bonne progression, continuez à suivre les conseils !"))

    # Fonction pour fermer toutes les fenêtres
    def fermer_toutes_les_fenetres():
        for widget in QApplication.topLevelWidgets():
            widget.close()  # Ferme toutes les fenêtres principales ouvertes

    # Bouton pour fermer
    close_button = QPushButton("Fermer")
    close_button.clicked.connect(fermer_toutes_les_fenetres)  # Associe la fermeture de toutes les fenêtres
    layout.addWidget(close_button)

    bilan_dialog.exec()


# Données fictives pour l'exemple
client_data = {
    "nom": "Ademy",
    "prenom": "John",
    "age": 25,
    "poids": 70,
    "taille": 175,
    "objectif": "Perte de poids",
    "niveau": "Intermédiaire"
}
def afficher_profil():
    profil_dialog = QDialog(window)
    profil_dialog.setWindowTitle("Profil du Client")
    profil_dialog.setFixedSize(400, 300)

    layout = QVBoxLayout(profil_dialog)

    # Ajouter les informations du client
    layout.addWidget(QLabel(f"Nom: {client_data['nom']}"))
    layout.addWidget(QLabel(f"Prénom: {client_data['prenom']}"))
    layout.addWidget(QLabel(f"Âge: {client_data['age']} ans"))
    layout.addWidget(QLabel(f"Poids: {client_data['poids']} kg"))
    layout.addWidget(QLabel(f"Taille: {client_data['taille']} cm"))
    layout.addWidget(QLabel(f"Objectif: {client_data['objectif']}"))
    layout.addWidget(QLabel(f"Niveau: {client_data['niveau']}"))

    # Ajouter un bouton pour fermer le dialogue
    close_button = QPushButton("Fermer")
    close_button.clicked.connect(profil_dialog.close)
    layout.addWidget(close_button)

    profil_dialog.exec()

# Fonction pour soumettre les données et afficher les résultats
def submit_choices():
    objectif = objectif_combobox.currentText()
    niveau = niveau_combobox.currentText()
    poids = poids_input.text()
    taille = taille_input.text()
    entrainements_par_semaine = entrainements_input.text()
    eau_par_jour = eau_input.text()
    age = age_input.text()

    # Validation des champs
    if not objectif or not niveau or not poids or not taille or not entrainements_par_semaine or not eau_par_jour or not age:
        QMessageBox.critical(window, "Erreur", "Veuillez remplir tous les champs.")
        return

    try:
        poids = float(poids)
        taille = float(taille) / 100  # Conversion en mètres
        age = int(age)
        entrainements_par_semaine = int(entrainements_par_semaine)
        eau_par_jour = float(eau_par_jour)
        imc = round(poids / (taille ** 2), 2)
    except ValueError:
        QMessageBox.critical(window, "Erreur", "Veuillez entrer des valeurs valides.")
        return

    # Évaluation de l'IMC
    if imc < 18.5:
        etat_imc = "Insuffisance pondérale"
        conseils_nutrition = "Augmentez votre apport calorique avec des aliments riches en nutriments."
    elif 18.5 <= imc < 25:
        etat_imc = "Poids normal"
        conseils_nutrition = "Maintenez une alimentation équilibrée riche en légumes, protéines et glucides complexes."
    elif 25 <= imc < 30:
        etat_imc = "Surpoids"
        conseils_nutrition = "Réduisez les sucres rapides et les aliments transformés."
    else:
        etat_imc = "Obésité"
        conseils_nutrition = "Consultez un professionnel pour une alimentation adaptée."

    eau_recommandee = calculer_eau(poids, entrainements_par_semaine)

    # Conseils d'entraînement via Expert System
    conseiller = ConseillerEntrainement()
    conseiller.reset()
    conseiller.declare(Entrainement(objectif=objectif, age=age, niveau=niveau))
    conseiller.run()

    conseils = conseiller.afficher_conseil()

    # Fenêtre des résultats
    result_dialog = QDialog(window)
    result_dialog.setWindowTitle("Conseils d'Entraînement")
    result_dialog.setFixedSize(600, 600)  # Augmenter la largeur

    layout = QVBoxLayout(result_dialog)
    layout.addWidget(QLabel(f"IMC : {imc} ({etat_imc})"))
    layout.addWidget(QLabel(f"Eau recommandée : {eau_recommandee} litres/jour"))
    layout.addWidget(QLabel(f"Conseils d'entraînement :\n{conseils}"))
    layout.addWidget(QLabel(f"Conseils Nutritionnels : {conseils_nutrition}"))

    # Bouton pour sauvegarder les conseils
    save_button = QPushButton("Sauvegarder")
    save_button.clicked.connect(
        lambda: sauvegarder_conseils(conseils, imc, etat_imc, eau_recommandee, conseils_nutrition)
    )
    layout.addWidget(save_button)

    # Bouton pour ouvrir l'interface d'entraînement
    start_button = QPushButton("Commencez Entraînement")
    start_button.clicked.connect(lambda: ouvrir_interface_entrainement(1))
    layout.addWidget(start_button)

    result_dialog.exec()


# Fenêtre principale
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Conseiller en Entraînement")
window.setFixedSize(800, 650)

# Style moderne
window.setStyleSheet("""
    QWidget {
        background-color: #f0f8ff;
        font-family: Arial, sans-serif;
    }
    QComboBox, QLineEdit, QPushButton {
        font-size: 14px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")

# Disposition
layout = QFormLayout(window)



objectif_combobox = QComboBox()
objectif_combobox.addItems(["perte_de_poids", "prise_de_muscle", "maintien"])
layout.addRow("Objectif :", objectif_combobox)

niveau_combobox = QComboBox()
niveau_combobox.addItems(["debutant", "intermediaire", "avancé"])
layout.addRow("Niveau :", niveau_combobox)

poids_input = QLineEdit()
layout.addRow("Poids (kg) :", poids_input)

taille_input = QLineEdit()
layout.addRow("Taille (cm) :", taille_input)

age_input = QLineEdit()
layout.addRow("Âge :", age_input)

condition_input = QComboBox()
condition_input.addItems(["Aucune", "Hypertension", "Diabète", "Autre"])
layout.addRow("Condition médicale :", condition_input)

temps_disponible_input = QLineEdit()
layout.addRow("Temps disponible (minutes) :", temps_disponible_input)


entrainements_input = QLineEdit()
layout.addRow("Entraînements par semaine :", entrainements_input)

eau_input = QLineEdit()
layout.addRow("Consommation d'eau (litres/jour) :", eau_input)

button_layout = QHBoxLayout()

# Ajouter le bouton du profil avec une icône redimensionnée
profil_button = QPushButton()
profil_button.setIcon(QIcon("profile_icon.png"))  # Assurez-vous d'avoir une image d'icône dans le dossier
profil_button.setIconSize(QSize(30, 30))  # Réduire la taille de l'icône
profil_button.setToolTip("Voir le profil client")
profil_button.clicked.connect(afficher_profil)
# Ajouter le bouton de profil à l'interface
button_layout.addWidget(profil_button)
button_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Aligné en haut à gauche
# Ajouter la disposition du bouton en haut à gauche à la disposition principale
layout.addRow(button_layout)

submit_button = QPushButton("Soumettre")
submit_button.clicked.connect(submit_choices)
layout.addWidget(submit_button)

window.show()
sys.exit(app.exec())
