from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate
import os

class MonthPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_date = QDate.currentDate()
        self.storage_dir = "pregledi_mjeseca"

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

        # 1. Naslov (Pitanje iz tvog dizajna)
        self.header_label = QLabel("")
        self.header_label.setObjectName("monthReviewTitle")
        self.header_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.header_label)

        # 2. Ime mjeseca (Dinamički naslov)
        self.month_label = QLabel()
        self.month_label.setObjectName("monthTitle")
        self.month_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.month_label)

        # 3. Veliki prozor za tekst (Sivi okvir kao na slici)
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("monthReviewInput")
        self.text_edit.setPlaceholderText("A little snapshot of your month, in a few sentences.")
        center_v_layout.addWidget(self.text_edit)

        # 4. Kontrole (Spremi i Nazad)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(20)
        controls_layout.setAlignment(Qt.AlignCenter)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_month_review)
        
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

    def update_display(self):
        """Ažurira naslov i učitava tekst za trenutni mjesec"""
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_name = month_names[self.current_date.month() - 1]
        year = self.current_date.year()
        
        ##self.month_label.setText(f"{month_name} {year}")
        self.header_label.setText(
            f"Few words about your {month_name} {year}\n" 
            "the moments that mattered, the things you’re proud of"
        )
        self.load_month_review()

    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_display()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_display()

    def get_file_path(self):
        """Vraća putanju do .txt datoteke za trenutni mjesec"""
        month_names_en = [
           "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_name = month_names_en[self.current_date.month() - 1]
        year = self.current_date.year()
        filename = f"{month_name}_{year}.txt"
        
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
        return os.path.join(self.storage_dir, filename)

    def save_month_review(self):
        """Sprema tekst u .txt datoteku"""
        content = self.text_edit.toPlainText().strip()
        filepath = self.get_file_path()

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "Saved", "The monthly review has been successfully saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")

    def load_month_review(self):
        """Učitava tekst iz .txt datoteke ako postoji"""
        filepath = self.get_file_path()
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.text_edit.setPlainText(f.read())
            except Exception as e:
                print(f"Loading error..{e}")
                self.text_edit.clear()
        else:
            self.text_edit.clear()
