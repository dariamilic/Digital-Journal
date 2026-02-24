import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from pages.home_page import HomePage
from pages.journal_page import JournalPage
from pages.calendar_page import CalendarPage
from pages.goals_page import GoalsPage
from pages.daily_page import DailyPage
from pages.month_page import MonthPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Journal")
        self.resize(600, 600)

        # STACK
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # STRANICE
        self.home_page = HomePage(self)
        self.journal_page = JournalPage(self)
        self.calendar_page = CalendarPage(self)
        self.goals_page = GoalsPage(self)
        self.daily_page = DailyPage(self)
        self.month_page = MonthPage(self)

        # DODAJ U STACK
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.journal_page)
        self.stack.addWidget(self.calendar_page)
        self.stack.addWidget(self.goals_page)
        self.stack.addWidget(self.daily_page)
        self.stack.addWidget(self.month_page)

        # DEFAULT
        self.show_home()

    # ================= NAVIGACIJA =================

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