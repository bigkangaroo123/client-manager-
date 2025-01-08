import sqlite3

def init_db():
    conn = sqlite3.connect("client_management.db")
    cursor= conn.cursor()

    #clients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            rate INTEGER NOT NULL
        )
    """)

    #projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY (client_id) REFERENCES clients(client_id)
        )
    """)

    #tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            deadline TEXT
            complete INTEGER DEFAULT 0,
            notes TEXT
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        )
    """)

    conn.commit()
    conn.close()

def add_client()

def add_project()

def add_task()
