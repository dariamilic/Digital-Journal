from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QCalendarWidget, QFrame, QScrollArea, QLineEdit, QInputDialog
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QTextCharFormat, QColor

class CalendarPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        self.tasks = {}

        # Glavni vertikalni layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 1. Naslov mjeseca s malim strelicama
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("navArrow") # Promijenjeno u navArrow
        self.btn_prev.clicked.connect(self.prev_month)
        
        self.month_label = QLabel()
        self.month_label.setObjectName("monthTitle")
        
        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("navArrow") # Promijenjeno u navArrow
        self.btn_next.clicked.connect(self.next_month)
        
        header_layout.addWidget(self.btn_prev)
        header_layout.addWidget(self.month_label)
        header_layout.addWidget(self.btn_next)
        layout.addLayout(header_layout)

        # 2. Središnji dio (Kalendar + Obaveze)
        content_h_layout = QHBoxLayout()
        content_h_layout.setSpacing(40)
        layout.addLayout(content_h_layout)

        # Kalendar (uokviren u kontejner sa zaobljenim rubovima)
        self.calendar_container = QFrame()
        self.calendar_container.setObjectName("calendarContainer")
        calendar_layout = QVBoxLayout(self.calendar_container)
        
        self.calendar = QCalendarWidget()
        self.calendar.setFixedSize(280, 280)
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.selectionChanged.connect(self.update_task_list)
        self.calendar.clicked.connect(self.add_task_prompt)
        
        calendar_layout.addWidget(self.calendar)
        content_h_layout.addWidget(self.calendar_container, 0, Qt.AlignTop)

        # Obaveze
        tasks_v_layout = QVBoxLayout()
        tasks_v_layout.setAlignment(Qt.AlignTop)
        content_h_layout.addLayout(tasks_v_layout)

        obaveze_label = QLabel("obaveze")
        obaveze_label.setObjectName("obavezeTitle")
        tasks_v_layout.addWidget(obaveze_label)

        line = QFrame()
        line.setObjectName("separatorLine")
        line.setFrameShape(QFrame.HLine)
        tasks_v_layout.addWidget(line)
        tasks_v_layout.addSpacing(-10) # Povlačenje crte gore (Crvena oznaka)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.tasks_container = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_container)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.tasks_container)
        tasks_v_layout.addWidget(self.scroll)

        # Gumb za povratak (mali i diskretan u kutu)
        footer_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.main_window.show_home)
        footer_layout.addStretch()
        footer_layout.addWidget(back_btn)
        layout.addLayout(footer_layout)

        self.update_month_label()
        self.update_task_list()

    def update_month_label(self):
        """Ažurira naslov i postavlja boje vikenda (Ljubičasta oznaka)"""
        month = self.calendar.monthShown()
        year = self.calendar.yearShown()
        month_names = [
            "Siječanj", "Veljača", "Ožujak", "Travanj", "Svibanj", "Lipanj",
            "Srpanj", "Kolovoz", "Rujan", "Listopad", "Studeni", "Prosinac"
        ]
        month_name = month_names[month - 1]
        self.month_label.setText(f"{month_name.lower()} {year}")

        # Postavljanje boje vikenda (Ljubičasta oznaka)
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QColor("#C8AABF")) # Boja crte ispod mjeseca
        
        # Prolazimo kroz sve dane u tjednu (Subota=6, Nedjelja=7)
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekend_format)

    def prev_month(self):
        self.calendar.showPreviousMonth()
        self.update_month_label()

    def next_month(self):
        self.calendar.showNextMonth()
        self.update_month_label()

    def add_task_prompt(self, date):
        """Otvara prozor za unos obaveze kada se klikne na datum"""
        date_str = date.toString("d.M.")
        text, ok = QInputDialog.getText(self, "Nova obaveza", f"Obaveza za {date_str}:")
        
        if ok and text:
            full_task = f"{date_str} {text}"
            date_key = date.toString(Qt.ISODate)
            
            if date_key not in self.tasks:
                self.tasks[date_key] = []
            
            self.tasks[date_key].append(full_task)
            
            # Zatamni datum u kalendaru
            self.highlight_date(date)
            self.update_task_list()

    def highlight_date(self, date):
        """Zatamnjuje datum u kalendaru ako ima obavezu"""
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#9E768F")) # Tamnija roza boja
        fmt.setForeground(Qt.white)
        self.calendar.setDateTextFormat(date, fmt)

    def update_task_list(self):
        """Osvježava listu obaveza na desnoj strani"""
        # Očisti trenutnu listu
        for i in reversed(range(self.tasks_layout.count())): 
            self.tasks_layout.itemAt(i).widget().setParent(None)

        # Prikaži obaveze za odabrani datum (ili sve za taj mjesec?)
        # Prema tvojoj slici, čini se da želiš listu obaveza.
        # Ovdje ćemo prikazati sve obaveze za trenutno prikazani mjesec.
        
        current_month = self.calendar.monthShown()
        current_year = self.calendar.yearShown()

        for date_key, task_list in self.tasks.items():
            date = QDate.fromString(date_key, Qt.ISODate)
            if date.month() == current_month and date.year() == current_year:
                for task in task_list:
                    item_layout = QHBoxLayout()
                    
                    # Bullet point
                    bullet = QFrame()
                    bullet.setObjectName("bulletPoint")
                    item_layout.addWidget(bullet)
                    
                    # Tekst obaveze
                    label = QLabel(task)
                    label.setObjectName("taskLabel")
                    item_layout.addWidget(label)
                    item_layout.addStretch()
                    
                    container = QWidget()
                    container.setLayout(item_layout)
                    self.tasks_layout.addWidget(container)
