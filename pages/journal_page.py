from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import datetime
import os

class JournalPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Naslov
        title = QLabel("Kako se osjećaš danas?")
        title.setObjectName("journalTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Polje za unos teksta
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("journalInput")
        self.text_edit.setPlaceholderText("Olakšaj dušu...")
        layout.addWidget(self.text_edit)

        # Kontrole (Spremi i Nazad)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        controls_layout.setAlignment(Qt.AlignCenter)

        save_btn = QPushButton("Spremi")
        save_btn.clicked.connect(self.save_entry)
        
        back_btn = QPushButton("Nazad")
        back_btn.clicked.connect(self.main_window.show_home)

        controls_layout.addWidget(save_btn)
        controls_layout.addWidget(back_btn)
        
        layout.addLayout(controls_layout)

    def save_entry(self):
        content = self.text_edit.toPlainText().strip()

        if not content:
            QMessageBox.warning(self, "Prazno", "Ništa nisi napisala.")
            return

        # Kreiranje mape s datumom
        today_str = datetime.date.today().strftime('%d-%m-%Y')
        if not os.path.exists(today_str):
            os.makedirs(today_str)

        # Ime datoteke je trenutno vrijeme
        filename = datetime.datetime.now().strftime('%H-%M-%S') + ".txt"
        filepath = os.path.join(today_str, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.text_edit.clear()
            QMessageBox.information(self, "Spremljeno", "Tvoj unos je uspješno spremljen.")
        except Exception as e:
            QMessageBox.critical(self, "Greška", f"Došlo je do greške pri spremanju: {e}")
