# 📓 Digital Journal

A personal desktop application built with Python and PySide6, designed to help you organize your time, track your goals, and reflect on your emotions — all in one place.

---

## 💡 About the Project

Digital Journal is a fully local desktop application that serves as your personal space for self-reflection and daily organization. The idea behind it is simple: everything you need to stay on top of your days, months, and emotions should live in one clean, focused place — no cloud, no distractions, just you and your thoughts.

The app was built as a portfolio project to demonstrate real-world skills in Python desktop development, UI design with PySide6, and relational database management with PostgreSQL.

---

## ✨ Features

| Page | Description |
|------|-------------|
| 🏠 **Home** | Clean welcome screen with quick navigation to all sections |
| 📅 **Calendar** | Add tasks and obligations to specific dates, with visual highlights on days that have entries |
| ✅ **Daily Tasks** | Log up to 3 tasks per day with an additional notes section, navigable by date |
| 🎯 **Goals** | Monthly reflection across four areas: Acknowledgements, What you're proud of, Physical fitness, and Emotional well-being |
| 📆 **Month Overview** | Write a short narrative summary of each month |
| 📝 **Journal** | A free-form daily journal entry with automatic timestamping |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **PySide6** — Qt-based framework used for building the entire desktop UI, including custom widgets, layouts, calendar components, and styled input fields
- **PostgreSQL** — relational database used to persist all user data locally across six structured tables
- **psycopg2** — PostgreSQL adapter for Python, used to handle all database connections and queries
- **python-dotenv** — used to manage database credentials securely via a `.env` file

---

## 🗄️ Database Structure

The application uses a local PostgreSQL database with the following tables:

- **`journal`** — stores free-form journal entries with an automatic timestamp
- **`month_overview`** — stores one monthly reflection entry per month
- **`goals`** — stores four reflection categories per month (acknowledgements, proud of, physical, emotional)
- **`daily_tasks`** — stores up to 3 tasks and additional notes per day, including the day of the week
- **`task_completion`** — linked to `daily_tasks` via a foreign key, tracks whether each task has been marked as done
- **`calendar`** — stores tasks and obligations associated with specific calendar dates

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9 or higher
- PostgreSQL installed and running on your machine
- pip

### 1. Clone the repository

```bash
git clone https://github.com/dariamilic/Digital-Journal.git
cd Digital-Journal
```

### 2. Create and activate a virtual environment

```bash
python -m venv virtualka
source virtualka/bin/activate  # On Windows: virtualka\Scripts\activate
```

### 3. Install dependencies

```bash
pip install PySide6 psycopg2-binary python-dotenv
```

### 4. Set up PostgreSQL

Make sure PostgreSQL is running, then create a database:

```bash
psql -U postgres -p YOUR_PORT
```

```sql
CREATE DATABASE journal;
\q
```

### 5. Configure environment variables

Create a `.env` file in the root of the project:

```
DB_HOST=localhost
DB_NAME=journal
DB_USER=postgres
DB_PASSWORD=your_password_or_leave_empty
DB_PORT=5432
```

> ⚠️ The `.env` file is listed in `.gitignore` and will never be pushed to GitHub.

### 6. Run the application

```bash
python main.py
```

The app will automatically create all required database tables on first launch.

---

## 📁 Project Structure

```
Digital-Journal/
│
├── database/
│   ├── __init__.py
│   ├── connection.py       # PostgreSQL connection setup
│   ├── models.py           # Table creation (runs on startup)
│   └── queries.py          # Reusable SQL queries
│
├── pages/
│   ├── home_page.py
│   ├── journal_page.py
│   ├── daily_page.py
│   ├── goals_page.py
│   ├── month_page.py
│   └── calendar_page.py
│
├── .env                    # Local credentials (not tracked by git)
├── .gitignore
├── main.py                 # App entry point
└── README.md
```

---

## 🔒 Privacy

All data is stored **locally on your machine** in your own PostgreSQL database. Nothing is sent to any server or third party.

---

## 👩‍💻 Author

**Daria Milić**  
