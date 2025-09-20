import sqlite3

DB_NAME = "issues.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citizen_name TEXT,
            description TEXT,
            photo BLOB,
            status TEXT DEFAULT 'Pending',
            assigned_to TEXT,
            proof BLOB
        )
    ''')
    conn.commit()
    conn.close()

def insert_issue(citizen_name, description, photo):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO issues (citizen_name, description, photo) VALUES (?, ?, ?)",
              (citizen_name, description, photo))
    conn.commit()
    conn.close()

def get_issues():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM issues")
    data = c.fetchall()
    conn.close()
    return data

def update_issue_status(issue_id, status, assigned_to=None, proof=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if proof:
        c.execute("UPDATE issues SET status=?, assigned_to=?, proof=? WHERE id=?",
                  (status, assigned_to, proof, issue_id))
    elif assigned_to:
        c.execute("UPDATE issues SET status=?, assigned_to=? WHERE id=?",
                  (status, assigned_to, issue_id))
    else:
        c.execute("UPDATE issues SET status=? WHERE id=?", (status, issue_id))
    conn.commit()
    conn.close()
