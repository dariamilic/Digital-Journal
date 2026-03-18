from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QLineEdit, QTextEdit, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QKeyEvent

class DailyPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_date = QDate.currentDate()

        # Glavni horizontalni layout (Strelice na rubovima)
        main_h_layout = QHBoxLayout(self)
        
        # Lijeva strelica
        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("navArrow")
        self.btn_prev.clicked.connect(self.prev_day)
        main_h_layout.addWidget(self.btn_prev)

        # Središnji vertikalni layout
        center_v_layout = QVBoxLayout()
        center_v_layout.setSpacing(20)
        center_v_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        main_h_layout.addLayout(center_v_layout, 1)

        # 1. Naslov (Dan i Datum)
        self.date_label = QLabel()
        self.date_label.setObjectName("dailyDateLabel")
        self.date_label.setAlignment(Qt.AlignCenter)
        center_v_layout.addWidget(self.date_label)

        # Razmak prije gornje crte
        center_v_layout.addSpacing(20)

        # 2. Gornja crta
        top_line = QFrame()
        top_line.setObjectName("dailySeparator")
        top_line.setFrameShape(QFrame.HLine)
        center_v_layout.addWidget(top_line, 0, Qt.AlignCenter)

        # 3. Bullet points (3 defaultna)
        self.bullets_container = QVBoxLayout()
        self.bullets_container.setContentsMargins(50, 10, 50, 10)
        for _ in range(3):
            self.add_bullet_item()
        center_v_layout.addLayout(self.bullets_container)

        # 4. Donja crta
        bottom_line = QFrame()
        bottom_line.setObjectName("dailySeparator")
        bottom_line.setFrameShape(QFrame.HLine)
        center_v_layout.addWidget(bottom_line, 0, Qt.AlignCenter)

        # 5. Dodatne bilješke (crtice)
        self.notes_edit = NotesTextEdit()
        self.notes_edit.setObjectName("notesInput")
        self.notes_edit.setPlaceholderText("- ...")
        # Početna crtica
        self.notes_edit.setPlainText("- ")
        
        notes_layout = QVBoxLayout()
        notes_layout.setContentsMargins(50, 10, 50, 10)
        notes_layout.addWidget(self.notes_edit)
        center_v_layout.addLayout(notes_layout)

        # 6. Gumb za povratak
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.main_window.show_home)
        center_v_layout.addStretch()
        center_v_layout.addWidget(back_btn, 0, Qt.AlignCenter)

        # Desna strelica
        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow")
        self.btn_next.clicked.connect(self.next_day)
        main_h_layout.addWidget(self.btn_next)

        # Inicijalno osvježavanje
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
        
        container = QWidget()
        container.setObjectName("bulletItem")
        container.setLayout(item_layout)
        self.bullets_container.addWidget(container)

    def update_date_display(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_name = days[self.current_date.dayOfWeek() - 1]
        date_str = self.current_date.toString("d.M.")
        self.date_label.setText(f"{day_name} {date_str}")

    def prev_day(self):
        self.current_date = self.current_date.addDays(-1)
        self.update_date_display()

    def next_day(self):
        self.current_date = self.current_date.addDays(1)
        self.update_date_display()

class NotesTextEdit(QTextEdit):
    """Specijalni QTextEdit koji dodaje '- ' na svaki novi red"""
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            super().keyPressEvent(event)
            self.insertPlainText("- ")
        else:
            super().keyPressEvent(event)
