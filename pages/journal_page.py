from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from database.connection import get_connection
import datetime

class JournalPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Date label in top right corner
        today = datetime.date.today().strftime("%d.%m.%Y.")
        date_label = QLabel(today)
        date_label.setObjectName("dateLabel")
        date_label.setAlignment(Qt.AlignRight)
        layout.addWidget(date_label)

        title = QLabel("How are you feeling today?")
        title.setObjectName("journalTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("journalInput")
        self.text_edit.setPlaceholderText("Ease your mind...")
        layout.addWidget(self.text_edit)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        controls_layout.setAlignment(Qt.AlignCenter)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_entry)
        
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)

        controls_layout.addWidget(save_btn)
        controls_layout.addWidget(back_btn)
        layout.addLayout(controls_layout)

    def save_entry(self):
        content = self.text_edit.toPlainText().strip()

        if not content:
            QMessageBox.warning(self, "Empty", "There is nothing to save?")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # No date column needed — created_at fills automatically
            cursor.execute(
                "INSERT INTO journal (entry) VALUES (%s)",
                (content,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.text_edit.clear()
            QMessageBox.information(self, "Saved", "Your record has been saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")