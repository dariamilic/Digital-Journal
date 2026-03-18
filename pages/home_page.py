from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import datetime

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Glavni layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        # Naslovi
        self.welcome = QLabel("welcome back!")
        self.welcome.setObjectName("welcomeLabel")
        self.welcome.setAlignment(Qt.AlignCenter)
        
        self.subtitle = QLabel("What’s been on your mind today?")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.welcome)
        layout.addWidget(self.subtitle)

        # Layout za gumbe
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(20)

        # Prvi red gumba
        row1 = QHBoxLayout()
        row1.setSpacing(20)
        row1.addWidget(self.create_styled_button("Calendar", self.main_window.show_calendar))
        row1.addWidget(self.create_styled_button("Daily tasks", self.main_window.show_daily))
        row1.addWidget(self.create_styled_button("Goals", self.main_window.show_goals))
        buttons_container.addLayout(row1)

        # Drugi red gumba
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        row2.addStretch()
        row2.addWidget(self.create_styled_button("Month overview", self.main_window.show_month))
        row2.addWidget(self.create_styled_button("Journal", self.main_window.show_journal))
        row2.addStretch()
        buttons_container.addLayout(row2)

        layout.addLayout(buttons_container)

        # Datum na dnu
        today = datetime.date.today().strftime("%d.%m.%Y.")
        self.date_label = QLabel(today)
        self.date_label.setObjectName("dateLabel")
        self.date_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.date_label)

    def create_styled_button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        
        # Dodavanje sjene
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        btn.setGraphicsEffect(shadow)
        
        return btn
