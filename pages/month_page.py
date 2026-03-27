from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QDate
from database.connection import get_connection
import datetime

class MonthPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_date = QDate.currentDate()

        main_h_layout = QHBoxLayout(self)
        
        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("navArrow")
        self.btn_prev.clicked.connect(self.prev_month)
        main_h_layout.addWidget(self.btn_prev)

        center_v_layout = QVBoxLayout()
        center_v_layout.setSpacing(10)
        center_v_layout.setAlignment(Qt.AlignCenter)
        main_h_layout.addLayout(center_v_layout, 1)

        self.header_label = QLabel("")
        self.header_label.setObjectName("monthReviewTitle")
        self.header_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.header_label)

        self.month_label = QLabel()
        self.month_label.setObjectName("monthTitle")
        self.month_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.month_label)

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("monthReviewInput")
        self.text_edit.setPlaceholderText("A little snapshot of your month, in a few sentences.")
        center_v_layout.addWidget(self.text_edit)

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

        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow")
        self.btn_next.clicked.connect(self.next_month)
        main_h_layout.addWidget(self.btn_next)

        self.update_display()

    def update_display(self):
        month_names = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        month_name = month_names[self.current_date.month() - 1]
        year = self.current_date.year()
        self.header_label.setText(
            f"Few words about your {month_name} {year}\n"
            "the moments that mattered, the things you're proud of"
        )
        self.load_month_review()

    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_display()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_display()

    def save_month_review(self):
        content = self.text_edit.toPlainText().strip()
        # Use the first day of the current month as the date
        date = datetime.date(self.current_date.year(), self.current_date.month(), 1)

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Update if exists, insert if not
            cursor.execute("SELECT id FROM month_overview WHERE date = %s", (date,))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("UPDATE month_overview SET entry = %s WHERE date = %s", (content, date))
            else:
                cursor.execute("INSERT INTO month_overview (date, entry) VALUES (%s, %s)", (date, content))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Saved", "The monthly review has been successfully saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")

    def load_month_review(self):
        date = datetime.date(self.current_date.year(), self.current_date.month(), 1)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT entry FROM month_overview WHERE date = %s", (date,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                self.text_edit.setPlainText(row[0])
            else:
                self.text_edit.clear()
        except Exception as e:
            print(f"Loading error: {e}")
            self.text_edit.clear()