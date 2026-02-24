from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
import datetime
import os


class JournalPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        label = QLabel("How are you feeling today?")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px;")
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Piši ovdje svoje misli...")
        layout.addWidget(self.text_edit)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_entry)
        layout.addWidget(save_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)
        layout.addWidget(back_btn)

    def save_entry(self):
        content = self.text_edit.toPlainText().strip()

        if not content:
            QMessageBox.warning(self, "Prazno", "Ništa nisi napisala.")
            return

        today = datetime.date.today().strftime('%d-%m-%Y')
        if not os.path.exists(today):
            os.mkdir(today)

        filename = datetime.datetime.now().strftime('%H-%M-%S') + ".txt"
        filepath = os.path.join(today, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.text_edit.clear()
        QMessageBox.information(self, "Spremljeno", "Unos spremljen.")