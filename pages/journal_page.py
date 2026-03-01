from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
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

        label = QLabel("Kako se osjecas danas?")
        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("font-size: 18px; color: #C8AABF; ")
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Olaksaj dusu...")
        self.text_edit.setStyleSheet("color: #C8AABF; font-size: 16px;")
        layout.addWidget(self.text_edit)
        

        # Centriran layout za dugmadi
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_entry)
        buttons_layout.addWidget(save_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)
        buttons_layout.addWidget(back_btn)

        buttons_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(buttons_layout)

    def save_entry(self):
        content = self.text_edit.toPlainText().strip()

        if not content:
            msg = QMessageBox(self)
            msg.setWindowTitle("Prazno")
            msg.setText("Ništa nisi napisala.")
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("color: #C8AABF;")
            msg.exec()
            return

        today = datetime.date.today().strftime('%d-%m-%Y')
        if not os.path.exists(today):
            os.mkdir(today)

        filename = datetime.datetime.now().strftime('%H-%M-%S') + ".txt"
        filepath = os.path.join(today, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.text_edit.clear()
        msg = QMessageBox(self)
        msg.setWindowTitle("Spremljeno")
        msg.setText("Unos spremljen.")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("color: #C8AABF; font-size: 14px;")
        msg.exec()