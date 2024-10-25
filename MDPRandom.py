import sys
import random
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSlider, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Constantes pour les caractères
chars = "abcdefghijklmnopqrstuvwxyz"
nums = "0123456789"
special = "!;[]/?-+=@#$%&*"


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MdP Random")
        self.setGeometry(100, 100, 250, 250)
        self.setWindowIcon(QIcon("ico/MDPico.png"))

        # Widgets de l'interface
        self.label_length = QLabel("Longueur du mot de passe (8-32) :", self)
        self.slider_length = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_length.setRange(8, 32)
        self.slider_length.setValue(8)  # Valeur par défaut
        self.slider_length.valueChanged.connect(self.update_length_label)

        self.length_display = QLabel("8", self)  # Affiche la valeur par défaut du slider

        self.label_name = QLabel("Nom du mot de passe :", self)
        self.input_name = QLineEdit(self)

        self.button_generate = QPushButton("Générer", self)
        self.button_generate.clicked.connect(self.generate_password)

        self.output_password = QTextEdit(self)
        self.output_password.setReadOnly(True)

        self.button_save = QPushButton("Sauvegarder", self)
        self.button_save.clicked.connect(self.save_password)

        # Layout de l'interface
        layout = QVBoxLayout()
        layout.addWidget(self.label_length)
        layout.addWidget(self.slider_length)
        layout.addWidget(self.length_display)
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.button_generate)
        layout.addWidget(self.output_password)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def update_length_label(self, value):
        self.length_display.setText(str(value))

    def generate_password(self):
        pass_len = self.slider_length.value()  # Récupère la valeur actuelle du slider

        # Calcul des longueurs de chaque type de caractère
        chars_len = pass_len // 2
        num_len = math.ceil(pass_len * 30 / 100)
        special_len = pass_len - (chars_len + num_len)

        # Génération des caractères
        def generate_randoms(length, array, chars=False):
            result = []
            for _ in range(length):
                index = random.randint(0, len(array) - 1)
                character = array[index]
                if chars:
                    character = character.upper() if random.randint(0, 1) else character
                result.append(character)
            return result

        buffer = []
        buffer.extend(generate_randoms(chars_len, chars, True))
        buffer.extend(generate_randoms(num_len, nums))
        buffer.extend(generate_randoms(special_len, special))
        random.shuffle(buffer)
        password = "".join(buffer)

        self.output_password.setText(f"mot de passe généré :\n\n{password}")
        self.generated_password = password  # Stocker le mot de passe généré pour sauvegarde

    def save_password(self):
        password_name = self.input_name.text()
        if not password_name:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom pour le mot de passe.")
            return

        try:
            with open("passwords.txt", "a") as file:
                file.write(f"{password_name}: {self.generated_password}\n")
            QMessageBox.information(self, "Succès", "Mot de passe sauvegardé avec succès.\n\n Pour le consulté ouvrir passwords.txt")
        except AttributeError:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord générer un mot de passe.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
