from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QTextEdit
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QKeyEvent
from database.connection import get_connection
import datetime

class DailyPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_date = QDate.currentDate()

        main_h_layout = QHBoxLayout(self)
        
        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("navArrow")
        self.btn_prev.clicked.connect(self.prev_day)
        main_h_layout.addWidget(self.btn_prev)

        center_v_layout = QVBoxLayout()
        center_v_layout.setSpacing(20)
        center_v_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        main_h_layout.addLayout(center_v_layout, 1)

        self.date_label = QLabel()
        self.date_label.setObjectName("dailyDateLabel")
        self.date_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.date_label)

        center_v_layout.addSpacing(20)

        top_line = QFrame()
        top_line.setObjectName("dailySeparator")
        top_line.setFrameShape(QFrame.HLine)
        center_v_layout.addWidget(top_line, 0, Qt.AlignCenter)

        self.bullets_container = QVBoxLayout()
        self.bullets_container.setContentsMargins(50, 10, 50, 10)
        self.task_inputs = []
        for _ in range(3):
            self.add_bullet_item()
        center_v_layout.addLayout(self.bullets_container)

        bottom_line = QFrame()
        bottom_line.setObjectName("dailySeparator")
        bottom_line.setFrameShape(QFrame.HLine)
        center_v_layout.addWidget(bottom_line, 0, Qt.AlignCenter)

        self.notes_edit = NotesTextEdit()
        self.notes_edit.setObjectName("notesInput")
        self.notes_edit.setPlaceholderText("- ...")
        self.notes_edit.setPlainText("- ")
        notes_layout = QVBoxLayout()
        notes_layout.setContentsMargins(50, 10, 50, 10)
        notes_layout.addWidget(self.notes_edit)
        center_v_layout.addLayout(notes_layout)

        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignCenter)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_tasks)
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)
        controls_layout.addWidget(save_btn)
        controls_layout.addWidget(back_btn)

        center_v_layout.addStretch()
        center_v_layout.addLayout(controls_layout)

        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow")
        self.btn_next.clicked.connect(self.next_day)
        main_h_layout.addWidget(self.btn_next)

        self.update_date_display()

    def add_bullet_item(self):
        item_layout = QHBoxLayout()
        item_layout.setSpacing(15)
        bullet = QFrame()
        bullet.setObjectName("bulletPoint")
        item_layout.addWidget(bullet)
        input_field = QLineEdit()
        input_field.setObjectName("dailyInput")
        input_field.setPlaceholderText("Add a task.")
        item_layout.addWidget(input_field)
        self.task_inputs.append(input_field)
        container = QWidget()
        container.setObjectName("bulletItem")
        container.setLayout(item_layout)
        self.bullets_container.addWidget(container)

    def update_date_display(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = days[self.current_date.dayOfWeek() - 1]
        date_str = self.current_date.toString("d.M.")
        self.date_label.setText(f"{day_name} {date_str}")
        self.load_tasks()

    def prev_day(self):
        self.current_date = self.current_date.addDays(-1)
        self.update_date_display()

    def next_day(self):
        self.current_date = self.current_date.addDays(1)
        self.update_date_display()

    def save_tasks(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = days[self.current_date.dayOfWeek() - 1]
        date = self.current_date.toPython()
        task1 = self.task_inputs[0].text().strip()
        task2 = self.task_inputs[1].text().strip()
        task3 = self.task_inputs[2].text().strip()
        additional = self.notes_edit.toPlainText().strip()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM daily_tasks WHERE date = %s", (date,))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("""
                    UPDATE daily_tasks SET day=%s, task1=%s, task2=%s, task3=%s, additional_tasks=%s
                    WHERE date=%s
                """, (day_name, task1, task2, task3, additional, date))
            else:
                cursor.execute("""
                    INSERT INTO daily_tasks (date, day, task1, task2, task3, additional_tasks)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (date, day_name, task1, task2, task3, additional))
            conn.commit()
            cursor.close()
            conn.close()
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Saved", "Tasks saved successfully.")
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def load_tasks(self):
        date = self.current_date.toPython()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT task1, task2, task3, additional_tasks FROM daily_tasks WHERE date = %s", (date,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if row:
                self.task_inputs[0].setText(row[0] or "")
                self.task_inputs[1].setText(row[1] or "")
                self.task_inputs[2].setText(row[2] or "")
                self.notes_edit.setPlainText(row[3] or "- ")
            else:
                for inp in self.task_inputs:
                    inp.clear()
                self.notes_edit.setPlainText("- ")
        except Exception as e:
            print(f"Loading error: {e}")

class NotesTextEdit(QTextEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            super().keyPressEvent(event)
            self.insertPlainText("- ")
        else:
            super().keyPressEvent(event)