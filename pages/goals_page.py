from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt, QDate
import os

class GoalsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_date = QDate.currentDate()
        self.storage_dir = "ostvareni_ciljevi"

        # Glavni horizontalni layout (Strelice na rubovima)
        main_h_layout = QHBoxLayout(self)
        
        # Lijeva strelica
        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("navArrow")
        self.btn_prev.clicked.connect(self.prev_month)
        main_h_layout.addWidget(self.btn_prev)

        # Središnji vertikalni layout
        center_v_layout = QVBoxLayout()
        center_v_layout.setSpacing(10)
        center_v_layout.setAlignment(Qt.AlignCenter)
        main_h_layout.addLayout(center_v_layout, 1)

        # 1. Naslov (aktualni mjesec / ciljevi)
        self.month_label = QLabel()
        self.month_label.setObjectName("monthTitle")
        self.month_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.month_label)
       
        # 2. Mreža s 4 prozora (Zahvale, Ponosna, Fizička sprema, Emocionalno)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        center_v_layout.addLayout(grid_layout)

        self.sections = {
            "zahvale": self.create_goal_section("Acknowledgements", grid_layout, 0, 0),
            "ponosna": self.create_goal_section("What are you proud of", grid_layout, 0, 1),
            "fizicka": self.create_goal_section("Physical fitness", grid_layout, 1, 0),
            "emocionalno": self.create_goal_section("Emotional well-being", grid_layout, 1, 1)
        }

        # 3. Kontrole (Spremi i Nazad)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        controls_layout.setAlignment(Qt.AlignCenter)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_goals)
        
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)

        controls_layout.addWidget(save_btn)
        controls_layout.addWidget(back_btn)
        center_v_layout.addLayout(controls_layout)

        # Desna strelica
        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow")
        self.btn_next.clicked.connect(self.next_month)
        main_h_layout.addWidget(self.btn_next)

        # Inicijalno osvježavanje
        self.update_display()

    def create_goal_section(self, title, grid, row, col):
        """Pomoćna funkcija za kreiranje sekcije s naslovom i prozorom za tekst"""
        v_layout = QVBoxLayout()
        
        label = QLabel(title)
        label.setObjectName("goalSectionTitle")
        v_layout.addWidget(label)
        
        text_edit = QTextEdit()
        text_edit.setObjectName("goalInput")
        v_layout.addWidget(text_edit)
        
        grid.addLayout(v_layout, row, col)
        return text_edit

    def update_display(self):
        """Ažurira naslov i učitava podatke za trenutni mjesec"""
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_name = month_names[self.current_date.month() - 1]
        year = self.current_date.year()
        
        self.month_label.setText(f"{month_name.lower()} {year}")
        self.load_goals()

    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_display()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_display()

    def get_file_path(self, section_key):
        """Vraća putanju do .txt datoteke za određenu sekciju i mjesec"""
        month_names_en = [
            "sijecanj", "veljaca", "ozujak", "travanj", "svibanj", "lipanj",
            "srpanj", "kolovoz", "rujan", "listopad", "studeni", "prosinac"
        ]
        month_name = month_names_en[self.current_date.month() - 1]
        year = self.current_date.year()
        filename = f"{section_key}_{month_name}_{year}.txt"
        
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
        return os.path.join(self.storage_dir, filename)

    def save_goals(self):
        """Sprema tekst iz svih 4 sekcija"""
        try:
            for key, text_edit in self.sections.items():
                content = text_edit.toPlainText().strip()
                filepath = self.get_file_path(key)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            QMessageBox.information(self, "Spremljeno", "Ciljevi su uspješno spremljeni.")
        except Exception as e:
            QMessageBox.critical(self, "Greška", f"Došlo je do greške pri spremanju: {e}")

    def load_goals(self):
        """Učitava tekst za sve 4 sekcije"""
        for key, text_edit in self.sections.items():
            filepath = self.get_file_path(key)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text_edit.setPlainText(f.read())
                except Exception as e:
                    print(f"Greška pri učitavanju {key}: {e}")
                    text_edit.clear()
            else:
                text_edit.clear()
