from database.connection import get_connection

def save_entry(text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO journal (entry) VALUES (%s)", (text,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_entries():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM journal ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows