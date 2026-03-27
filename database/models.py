from database.connection import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Journal table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            entry TEXT NOT NULL
        )
    """)

    # 2. Month overview table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS month_overview (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            entry TEXT NOT NULL
        )
    """)

    # 3. Goals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            acknowledgements TEXT,
            proud_of TEXT,
            physical TEXT,
            emotional TEXT
        )
    """)

    # 4. Daily tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_tasks (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            day VARCHAR(10) NOT NULL,
            task1 VARCHAR(200),
            task2 VARCHAR(200),
            task3 VARCHAR(200),
            additional_tasks TEXT
        )
    """)

    # 5. Task completion table (connected to daily_tasks)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_completion (
            id SERIAL PRIMARY KEY,
            daily_task_id INTEGER REFERENCES daily_tasks(id) ON DELETE CASCADE,
            task1_done BOOLEAN DEFAULT FALSE,
            task2_done BOOLEAN DEFAULT FALSE,
            task3_done BOOLEAN DEFAULT FALSE
        )
    """)

    # 6. Calendar table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()