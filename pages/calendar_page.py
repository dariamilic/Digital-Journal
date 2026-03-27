from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCalendarWidget, QFrame, QScrollArea, QInputDialog
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QTextCharFormat, QColor
from database.connection import get_connection

class CalendarPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("navArrow")
        self.btn_prev.clicked.connect(self.prev_month)
        
        self.month_label = QLabel()
        self.month_label.setObjectName("monthTitle")
        
        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow")
        self.btn_next.clicked.connect(self.next_month)
        
        header_layout.addWidget(self.btn_prev)
        header_layout.addWidget(self.month_label)
        header_layout.addWidget(self.btn_next)
        layout.addLayout(header_layout)

        content_h_layout = QHBoxLayout()
        content_h_layout.setSpacing(40)
        content_h_layout.setContentsMargins(0, 20, 0, 0)
        layout.addLayout(content_h_layout)

        left_v_layout = QVBoxLayout()
        left_v_layout.setAlignment(Qt.AlignTop)
        content_h_layout.addLayout(left_v_layout)

        right_v_layout = QVBoxLayout()
        right_v_layout.setAlignment(Qt.AlignTop)
        content_h_layout.addLayout(right_v_layout)

        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(300, 380)
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.selectionChanged.connect(self.update_task_list)
        self.calendar.clicked.connect(self.add_task_prompt)
        left_v_layout.addWidget(self.calendar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(380)
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.tasks_layout.setSpacing(0)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.tasks_container)
        right_v_layout.addWidget(self.scroll)

        footer_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.main_window.show_home)
        footer_layout.addStretch()
        footer_layout.addWidget(back_btn)
        footer_layout.addStretch()
        layout.addLayout(footer_layout)

        self.update_month_label()
        self.highlight_dates_with_tasks()
        self.update_task_list()

    def update_month_label(self):
        month = self.calendar.monthShown()
        year = self.calendar.yearShown()
        month_names = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        self.month_label.setText(f"{month_names[month - 1].lower()} {year}")
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QColor("#C8AABF"))
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

    def prev_month(self):
        self.calendar.showPreviousMonth()
        self.update_month_label()
        self.highlight_dates_with_tasks()
        self.update_task_list()

    def next_month(self):
        self.calendar.showNextMonth()
        self.update_month_label()
        self.highlight_dates_with_tasks()
        self.update_task_list()

    def add_task_prompt(self, date):
        date_str = date.toString("d.M.")
        text, ok = QInputDialog.getText(self, "New task", f"Task for {date_str}:")
        if ok and text:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO calendar (date, task) VALUES (%s, %s)",
                    (date.toPython(), text)
                )
                conn.commit()
                cursor.close()
                conn.close()
                self.highlight_date(date)
                self.update_task_list()
            except Exception as e:
                print(f"Error saving task: {e}")

    def highlight_date(self, date):
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#9E768F"))
        fmt.setForeground(Qt.white)
        self.calendar.setDateTextFormat(date, fmt)

    def highlight_dates_with_tasks(self):
        month = self.calendar.monthShown()
        year = self.calendar.yearShown()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT date FROM calendar WHERE EXTRACT(MONTH FROM date)=%s AND EXTRACT(YEAR FROM date)=%s",
                (month, year)
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            for row in rows:
                qdate = QDate(row[0].year, row[0].month, row[0].day)
                self.highlight_date(qdate)
        except Exception as e:
            print(f"Error highlighting dates: {e}")

    def update_task_list(self):
        for i in reversed(range(self.tasks_layout.count())):
            self.tasks_layout.itemAt(i).widget().setParent(None)

        month = self.calendar.monthShown()
        year = self.calendar.yearShown()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT date, task FROM calendar WHERE EXTRACT(MONTH FROM date)=%s AND EXTRACT(YEAR FROM date)=%s ORDER BY date",
                (month, year)
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            for row in rows:
                date_str = row[0].strftime("%-d.%-m.")
                task_text = f"{date_str} {row[1]}"
                item_layout = QHBoxLayout()
                item_layout.setContentsMargins(5, 2, 5, 2)
                bullet = QFrame()
                bullet.setObjectName("bulletPoint")
                item_layout.addWidget(bullet)
                label = QLabel(task_text)
                label.setObjectName("taskLabel")
                item_layout.addWidget(label)
                item_layout.addStretch()
                container = QWidget()
                container.setLayout(item_layout)
                self.tasks_layout.addWidget(container)
        except Exception as e:
            print(f"Error loading tasks: {e}")