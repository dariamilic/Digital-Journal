from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Dobrodošla natrag.\n\nŠto ti je danas na umu?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        journal_btn = QPushButton("Dnevnik")
        journal_btn.clicked.connect(self.main_window.show_journal)
        layout.addWidget(journal_btn)

        calendar_btn = QPushButton("Kalendar")
        calendar_btn.clicked.connect(self.main_window.show_calendar)
        layout.addWidget(calendar_btn)

        goals_btn = QPushButton("Ciljevi")
        goals_btn.clicked.connect(self.main_window.show_goals)
        layout.addWidget(goals_btn)

        daily_tasks_btn = QPushButton("Dnevne obaveze")
        daily_tasks_btn.clicked.connect(self.main_window.show_daily)
        layout.addWidget(daily_tasks_btn)

        month_review_btn = QPushButton("Pregled mjeseca")
        month_review_btn.clicked.connect(self.main_window.show_month)
        layout.addWidget(month_review_btn)

