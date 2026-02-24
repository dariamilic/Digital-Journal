from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import datetime

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # Učitavanje stila iz vanjske datoteke
        self.load_stylesheet("style.qss")

        # Glavni layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)

        # 1. Naslovi
        self.welcome = QLabel("dobrodošla natrag!")
        self.welcome.setObjectName("welcomeLabel")
        self.welcome.setAlignment(Qt.AlignCenter)
        
        self.subtitle = QLabel("što ti je danas na umu?")
        self.subtitle.setObjectName("subtitleLabel")
        self.subtitle.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.welcome)
        main_layout.addWidget(self.subtitle)

        # Kreiranje gumba
        self.btn_kalendar = self.create_button("kalendar", self.main_window.show_calendar)
        self.btn_obaveze = self.create_button("dnevne obaveze", self.main_window.show_daily)
        self.btn_ciljevi = self.create_button("ciljevi", self.main_window.show_goals)
        self.btn_pregled = self.create_button("pregled mjeseca", self.main_window.show_month)
        self.btn_dnevnik = self.create_button("dnevnik", self.main_window.show_journal)

        # 2. Layout s gumbima
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(20)

        # Prvi red: 3 gumba
        first_row = QHBoxLayout()
        first_row.setSpacing(20)
        first_row.addWidget(self.btn_kalendar)
        first_row.addWidget(self.btn_obaveze)
        first_row.addWidget(self.btn_ciljevi)
        buttons_layout.addLayout(first_row)

        # Drugi red: 2 gumba, centrirana
        second_row = QHBoxLayout()
        second_row.setSpacing(20)  # Razmak kao u prvom redu
        second_row.addStretch()
        second_row.addWidget(self.btn_pregled)
        second_row.addWidget(self.btn_dnevnik)
        second_row.addStretch()
        buttons_layout.addLayout(second_row)

        main_layout.addLayout(buttons_layout)

        # 3. Datum na dnu
        today = datetime.date.today().strftime("%d.%m.%Y.")
        self.date_label = QLabel(today)
        self.date_label.setObjectName("dateLabel")
        self.date_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.date_label)

    def create_button(self, text, function):
        """Pomoćna funkcija za kreiranje gumba sa sjenom"""
        btn = QPushButton(text)
        btn.clicked.connect(function)
        
        # Dodavanje sjene (kao na tvojoj slici)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 60))
        btn.setGraphicsEffect(shadow)
        
        return btn

    def load_stylesheet(self, filename):
        """Učitava QSS datoteku"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Upozorenje: {filename} nije pronađena.")