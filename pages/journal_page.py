from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import datetime
import os

class JournalPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Naslov
        title = QLabel("How are you feeling today?")
        title.setObjectName("journalTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Polje za unos teksta
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("journalInput")
        self.text_edit.setPlaceholderText("Ease your mind…")
        layout.addWidget(self.text_edit)

        # Kontrole (Spremi i Nazad)
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

        # Glavna mapa za zapise
        base_dir = "dnevnik zapisi"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Migracija starih zapisa ako postoje u rootu
        self.migrate_old_entries(base_dir)

        # Kreiranje podmape s datumom unutar glavne mape
        today_str = datetime.date.today().strftime('%d-%m-%Y')
        full_date_path = os.path.join(base_dir, today_str)
        if not os.path.exists(full_date_path):
            os.makedirs(full_date_path)

        # Ime datoteke je trenutno vrijeme
        filename = datetime.datetime.now().strftime('%H-%M-%S') + ".txt"
        filepath = os.path.join(full_date_path, filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.text_edit.clear()
            QMessageBox.information(self, "Saved", "Your record has been saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving. {e}")

    def migrate_old_entries(self, base_dir):
        """Pronađi mape s datumom u rootu i premjesti ih u 'dnevnik zapisi'"""
        import re
        import shutil
        
        # Tražimo mape koje izgledaju kao DD-MM-YYYY
        date_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')
        
        for item in os.listdir('.'):
            if os.path.isdir(item) and date_pattern.match(item) and item != base_dir:
                try:
                    dest = os.path.join(base_dir, item)
                    if not os.path.exists(dest):
                        shutil.move(item, dest)
                    else:
                        # Ako već postoji, premjesti samo datoteke unutra
                        for file in os.listdir(item):
                            shutil.move(os.path.join(item, file), os.path.join(dest, file))
                        os.rmdir(item)
                except Exception as e:
                    print(f"Migration error {item}: {e}")
