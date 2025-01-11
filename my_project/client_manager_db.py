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
            task_id INTEGER PRIMARY KEY AUTOI   NCREMENT,
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

init_db()

#--------------adding stuff to db------------------
def get_db_connection():
    conn = sqlite3.connect('client_management.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_client_db(client_name, rate):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor
    cursor.execute("INSERT INTO clients (client_name, rate) VALUES (?, ?)", (client_name, rate))
    conn.commit()
    conn.close()

def add_project_db(client_id, project_name):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor
    cursor.execute("INSERT INTO projects (client_id, project_name) VALUES (?, ?)", (client_id, project_name))
    conn.commit()
    conn.close()

def add_task_db(client_id, project_id, task_name, deadline, complete, notes):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor
    cursor.execute("""
        INSERT INTO tasks (client_id, project_id, task_name, deadline, complete, notes) VALUES (?, ?, ?, ?, ?, ?)""",
        (client_id, project_id, task_name, deadline, complete, notes)
    )
    conn.commit()
    conn.close()

#--------------updating stuff from db------------------
def update_client_db(client_id, client_name, rate):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET client_name = ?, rate = ?
        WHERE client_id = ?
    """, (client_name, rate, client_id))
    conn.commit()
    conn.close()

def update_project_db(project_id, project_name):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET project_name = ?
        WHERE project_id = ?
    """, (project_name, project_id))
    conn.commit()
    conn.close()

def update_task_db(task_id, task_name, deadline, complete, notes):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET task_name = ?, deadline = ?, complete = ?, notes = ?
        WHERE task_id = ?
    """, (task_name, deadline, complete, notes, task_id))
    conn.commit()
    conn.close()

#--------------deleting stuff from db------------------
def delete_client_db(client_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
    cursor.execute("DELETE FROM projects WHERE client_id = ?", (client_id,))
    cursor.execute("DELETE FROM tasks WHERE client_id = ?", (client_id,))
    conn.commit()
    conn.close()

def delete_project_db(client_id, project_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM projects WHERE client_id = ? AND project_id = ?", (client_id, project_id))
    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    conn.commit()
    conn.close()

#--------------archiving / unarchiving stuff from db------------------
def archive_client(client_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET status = 'archived' WHERE client_id = ?", (client_id,))
    conn.commit()
    conn.close()

def archive_project(client_id, project_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET status = 'archived' WHERE client_id = ? AND project_id = ?", (client_id, project_id,))
    conn.commit()
    conn.close()

def unarchive_client(client_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET status = 'active' WHERE client_id = ?", (client_id,))
    conn.commit()
    conn.close()

def unarchive_project(client_id, project_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET status = 'active' WHERE client_id = ? AND project_id = ?", (client_id, project_id,))
    conn.commit()
    conn.close()

#--------------viewing stuff from db------------------
def get_all_clients():
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE status != 'archived'")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_all_projects(client_id):
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE status != 'archived' AND client_id = ?", (client_id,))
    projects = cursor.fetchall()
    conn.close()
    return projects

def get_all_archived_projects():
    conn = sqlite3.connect("client_management.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.project_id, p.name AS project_name, c.client_id, c.name AS client_name
        FROM projects p
        JOIN clients c ON p.client_id = c.client_id
        WHERE p.status = 'archived' AND c.status = 'archived'
    """)
    archived_projects = cursor.fetchall()
    conn.close()

    # Format the result into a list of dictionaries
    archived_projects_data = []
    for project in archived_projects:
        archived_projects_data.append({
            "client_name": project[3],
            "project_name": project[1],
            "client_id": project[2],
            "project_id": project[0]
        })

    return archived_projects_data

def get_client_by_name(client_name):
    conn = get_db_connection()
    query = """
        SELECT * FROM clients WHERE name = ?
    """
    client = conn.execute(query, (client_name,)).fetchone()  # fetchone returns the first match or returns None
    conn.close()

    if client:
        return dict(client) #returning client as a dictionary for easy access to its different attributes like name, billing rate
    else:
        return None