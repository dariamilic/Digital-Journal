import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from pages.home_page import HomePage
from pages.journal_page import JournalPage
from pages.calendar_page import CalendarPage
from pages.goals_page import GoalsPage
from pages.daily_page import DailyPage
from pages.month_page import MonthPage
from database.models import create_tables
from database.queries import save_entry, get_all_entries

# Run once when app starts to make sure tables exist
create_tables()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Journal")
        self.resize(800, 600)
        self.setObjectName("mainWindow")

        # Učitavanje stila iz vanjske datoteke
        self.load_stylesheet("style.qss")

        # Centralni widget je QStackedWidget koji omogućuje promjenu stranica
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Inicijalizacija stranica
        self.home_page = HomePage(self)
        self.journal_page = JournalPage(self)
        self.calendar_page = CalendarPage(self)
        self.goals_page = GoalsPage(self)
        self.daily_page = DailyPage(self)
        self.month_page = MonthPage(self)

        # Dodavanje stranica u stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.journal_page)
        self.stack.addWidget(self.calendar_page)
        self.stack.addWidget(self.goals_page)
        self.stack.addWidget(self.daily_page)
        self.stack.addWidget(self.month_page)

        # Početna stranica
        self.show_home()

    def load_stylesheet(self, filename):
        """Učitava CSS datoteku koristeći apsolutnu putanju"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Warning: {file_path} not found.")

    # Metode za navigaciju
    def show_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def show_journal(self):
        self.stack.setCurrentWidget(self.journal_page)

    def show_calendar(self):
        self.stack.setCurrentWidget(self.calendar_page)

    def show_goals(self):
        self.stack.setCurrentWidget(self.goals_page)

    def show_daily(self):
        self.stack.setCurrentWidget(self.daily_page)

    def show_month(self):
        self.stack.setCurrentWidget(self.month_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
