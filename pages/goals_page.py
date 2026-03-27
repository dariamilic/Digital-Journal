from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QGridLayout
from PySide6.QtCore import Qt, QDate
from database.connection import get_connection
import datetime

class GoalsPage(QWidget):
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

        self.month_label = QLabel()
        self.month_label.setObjectName("monthTitle")
        self.month_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.month_label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)
        center_v_layout.addLayout(grid_layout)

        self.sections = {
            "acknowledgements": self.create_goal_section("Acknowledgements", grid_layout, 0, 0),
            "proud_of": self.create_goal_section("What are you proud of", grid_layout, 0, 1),
            "physical": self.create_goal_section("Physical fitness", grid_layout, 1, 0),
            "emotional": self.create_goal_section("Emotional well-being", grid_layout, 1, 1)
        }

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

        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow")
        self.btn_next.clicked.connect(self.next_month)
        main_h_layout.addWidget(self.btn_next)

        self.update_display()

    def create_goal_section(self, title, grid, row, col):
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
        month_names = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        month_name = month_names[self.current_date.month() - 1]
        self.month_label.setText(f"{month_name.lower()} {self.current_date.year()}")
        self.load_goals()

    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_display()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_display()

    def save_goals(self):
        date = datetime.date(self.current_date.year(), self.current_date.month(), 1)
        acknowledgements = self.sections["acknowledgements"].toPlainText().strip()
        proud_of = self.sections["proud_of"].toPlainText().strip()
        physical = self.sections["physical"].toPlainText().strip()
        emotional = self.sections["emotional"].toPlainText().strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM goals WHERE date = %s", (date,))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("""
                    UPDATE goals SET acknowledgements=%s, proud_of=%s, physical=%s, emotional=%s
                    WHERE date=%s
                """, (acknowledgements, proud_of, physical, emotional, date))
            else:
                cursor.execute("""
                    INSERT INTO goals (date, acknowledgements, proud_of, physical, emotional)
                    VALUES (%s, %s, %s, %s, %s)
                """, (date, acknowledgements, proud_of, physical, emotional))
            conn.commit()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Saved", "Goals saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")

    def load_goals(self):
        date = datetime.date(self.current_date.year(), self.current_date.month(), 1)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT acknowledgements, proud_of, physical, emotional FROM goals WHERE date = %s", (date,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                self.sections["acknowledgements"].setPlainText(row[0] or "")
                self.sections["proud_of"].setPlainText(row[1] or "")
                self.sections["physical"].setPlainText(row[2] or "")
                self.sections["emotional"].setPlainText(row[3] or "")
            else:
                for section in self.sections.values():
                    section.clear()
        except Exception as e:
            print(f"Loading error: {e}")