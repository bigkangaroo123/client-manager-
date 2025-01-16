import sqlite3

# Initialize the database:
def init_db():
    conn = sqlite3.connect('client_manager.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    # Create the clients table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        rate REAL,
        status TEXT DEFAULT 'active'
    )
    """)

    # Create the projects table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        project_name TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    # Create the tasks table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        task_name TEXT NOT NULL,
        deadline DATE,
        notes TEXT,
        complete BOOLEAN DEFAULT 0,
        hours REAL NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)

    conn.commit()
    conn.close()

# Utility function for database connection
def get_db_connection():
    conn = sqlite3.connect('client_manager.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

#-------------- Adding Stuff to DB --------------

def add_client_db(client_name, rate):
    conn = get_db_connection()
    cursor = conn.cursor()  # Added parentheses to invoke the cursor
    cursor.execute("INSERT INTO clients (client_name, rate) VALUES (?, ?)", (client_name, rate))
    conn.commit()
    conn.close()

def add_project_db(client_id, project_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projects (client_id, project_name)
        VALUES (?, ?)
    """, (client_id, project_name))
    conn.commit()
    conn.close()


def add_task_db(client_id, project_id, task_name, deadline, complete, notes, hours):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (client_id, project_id, task_name, deadline, complete, notes, hours) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (client_id, project_id, task_name, deadline, complete, notes, hours)
    )
    conn.commit()
    conn.close()

#-------------- Updating Stuff in DB --------------

def update_client_db(client_id, client_name, rate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET client_name = ?, rate = ?
        WHERE id = ?
    """, (client_name, rate, client_id))
    conn.commit()
    conn.close()

def update_project_db(project_id, project_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET project_name = ?
        WHERE id = ?  # Fixed: Correct column name `id`
    """, (project_name, project_id))
    conn.commit()
    conn.close()

def update_task_db(task_id, task_name, deadline, complete, notes, hours):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET task_name = ?, deadline = ?, complete = ?, notes = ?, hours = ?
        WHERE id = ?  # Fixed: Correct column name `id`
    """, (task_name, deadline, complete, notes, hours, task_id))
    conn.commit()
    conn.close()

#-------------- Deleting Stuff from DB --------------

def delete_client_db(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE client_id = ?", (client_id,))
    cursor.execute("DELETE FROM projects WHERE client_id = ?", (client_id,))
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

def delete_project_db(client_id, project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE client_id = ? AND id = ?", (client_id, project_id))
    cursor.execute("DELETE FROM projects WHERE client_id = ?", (client_id))
    conn.commit()
    conn.close()

def delete_task_db(client_id, project_id, task_id): #OVER EHRE, CHANGE IN THE MORE OPTIONS TAB AND DELETE IN TASK IN VIEWEING TAB 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE client_id = ? AND project_id = ? AND id = ?", (client_id, project_id, task_id))
    conn.commit()
    conn.close()

#-------------- Archiving / Unarchiving Stuff --------------

def archive_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET status = 'archived' WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

def archive_project(client_id, project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET status = 'archived' WHERE client_id = ? AND id = ?", (client_id, project_id))  # Fixed column name `id`
    conn.commit()
    conn.close()

def unarchive_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET status = 'active' WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

def unarchive_project(client_id, project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET status = 'active' WHERE client_id = ? AND id = ?", (client_id, project_id))  # Fixed column name `id`
    conn.commit()
    conn.close()

#-------------- Viewing Stuff from DB --------------

def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE status != 'archived'")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_all_archived_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id AS project_id, p.project_name, c.id AS client_id, c.client_name
        FROM projects p
        JOIN clients c ON p.client_id = c.id
        WHERE p.status = 'archived' AND c.status = 'archived'
    """)
    archived_projects = cursor.fetchall()
    conn.close()

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
    query = """SELECT * FROM clients WHERE client_name = ?"""
    client = conn.execute(query, (client_name,)).fetchone()  # fetchone returns the first match or None
    conn.close()

    if client:
        return dict(client)  # Returning client as a dictionary for easy access to attributes
    else:
        return None
    
def get_all_projects(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, project_name FROM projects WHERE client_id = ?
    """, (client_id,))
    projects = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'project_name': row[1]} for row in projects]

    # Convert fetched results to a list of dictionaries
    projects_data = []
    for project in projects:
        projects_data.append({
            "id": project[0],
            "client_id": project[1],
            "project_name": project[2],
            "status": project[3]
        })

    return projects_data

def get_tasks_by_client_and_project(client_id, project_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to fetch tasks
    query = """
    SELECT 
        id, task_name, deadline, notes, complete, hours
    FROM 
        tasks
    WHERE 
        client_id = ? AND project_id = ?
    """
    cursor.execute(query, (client_id, project_id))
    rows = cursor.fetchall()

    # Convert the fetched rows into a list of dictionaries
    tasks = [
        {
            "id": row[0],
            "task_name": row[1],
            "deadline": row[2],
            "notes": row[3],
            "complete": bool(row[4]),  # Convert to boolean for clarity
            "hours": row[5],
        }
        for row in rows
    ]

    conn.close()
    return tasks
    