from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class DailyPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        label = QLabel("Ovdje će biti dnevni zadaci.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)
        layout.addWidget(back_btn)