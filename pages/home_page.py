from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QGraphicsDropShadowEffect
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
# 2. Mreža s gumbima (Grid)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20) # Razmak između gumba
        grid_layout.setContentsMargins(20, 20, 20, 20) # Margine oko cijelog grida

        # Kreiranje gumba (koristimo ispravna imena sa slike)
        self.btn_kalendar = self.create_button("kalendar", self.main_window.show_calendar)
        self.btn_obaveze = self.create_button("dnevne obaveze", self.main_window.show_daily)
        self.btn_ciljevi = self.create_button("ciljevi", self.main_window.show_goals)
        self.btn_pregled = self.create_button("pregled mjeseca", self.main_window.show_month)
        self.btn_dnevnik = self.create_button("dnevnik", self.main_window.show_journal)

        # Raspored: grid_layout.addWidget(widget, red, stupac, [red_span, stupac_span])
        
        # PRVI RED (3 gumba)
        grid_layout.addWidget(self.btn_kalendar, 0, 0)
        grid_layout.addWidget(self.btn_obaveze, 0, 1)
        grid_layout.addWidget(self.btn_ciljevi, 0, 2)

        # DRUGI RED (2 gumba, centrirana ispod prva tri)
        # Koristimo stupce 0-1 za prvi i 1-2 za drugi da izgledaju centrirano
        grid_layout.addWidget(self.btn_pregled, 1, 0, 1, 2, alignment=Qt.AlignRight)
        grid_layout.addWidget(self.btn_dnevnik, 1, 1, 1, 2, alignment=Qt.AlignLeft)

        main_layout.addLayout(grid_layout)

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