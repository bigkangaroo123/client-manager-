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
        hours REAL,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (client_id) REFERENCES clients(id)
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


def add_task_db(client_id, project_id, task_name, deadline, notes, hours):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (client_id, project_id, task_name, deadline, notes, hours, complete)
        VALUES (?, ?, ?, ?, ?, ?, 0)
    """, (client_id, project_id, task_name, deadline, notes, hours))
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

def update_project_db(client_id, project_id, project_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projects
        SET project_name = ?
        WHERE id = ? AND client_id = ?
    """, (project_name, project_id, client_id))
    conn.commit()
    conn.close()

def update_task_status(task_id, complete):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET complete = ?
        WHERE id = ?
    """, (complete, task_id))
    conn.commit()
    conn.close()

def update_task_details(client_id, project_id, task_id, task_name, deadline, notes, hours):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET task_name = ?, deadline = ?, notes = ?, hours = ?
        WHERE id = ? AND project_id = ? AND client_id = ?
    """, (task_name, deadline, notes, hours, task_id, project_id, client_id))
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
    cursor.execute("DELETE FROM projects WHERE client_id = ?", (client_id,))
    conn.commit()
    conn.close()

def delete_task(client_id, project_id, task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ? AND client_id = ? AND project_id = ?
    """, (task_id, client_id, project_id))
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
    cursor.execute("UPDATE projects SET status = 'archived' WHERE client_id = ? AND id = ?", (client_id, project_id)) 
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
    cursor.execute("UPDATE projects SET status = 'active' WHERE client_id = ? AND id = ?", (client_id, project_id)) 
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

def get_client_by_id(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    client = cursor.fetchone()
    conn.close()
    return dict(client) if client else None

def get_all_archived_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE status = 'archived'")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_archived_projects_by_client(client_id):
    """Fetch all archived projects for a specific client."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, project_name
        FROM projects
        WHERE client_id = ? AND status = 'archived'
    """
    cursor.execute(query, (client_id,))
    projects = cursor.fetchall()
    conn.close()

    # Convert the results to a list of dictionaries for easier use
    return [{"id": row[0], "project_name": row[1]} for row in projects]
    

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
        SELECT id, project_name FROM projects WHERE client_id = ? AND status != 'archived'
    """, (client_id,))
    projects = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'project_name': row[1]} for row in projects]

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

def get_total_money_earned(client_id, project_id):
    """
    Calculates the total money earned for a specific client and project.

    Args:
        client_id (int): The ID of the client.
        project_id (int): The ID of the project.

    Returns:
        float: Total money earned for the project.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to calculate the total hours for the given client and project
    query = """
    SELECT 
        SUM(hours) 
    FROM 
        tasks
    WHERE 
        client_id = ? AND project_id = ?
    """
    cursor.execute(query, (client_id, project_id))
    total_hours = cursor.fetchone()[0]  # Fetch the sum of hours

    # If no tasks exist, SUM(hours) will return None; handle that case
    total_hours = total_hours if total_hours is not None else 0.0

    # Get the rate for the client
    query_rate = """
    SELECT 
        rate 
    FROM 
        clients
    WHERE 
        id = ?
    """
    cursor.execute(query_rate, (client_id,))
    client_rate = cursor.fetchone()[0]  # Fetch the client's rate

    conn.close()

    # Calculate total money earned
    total_money = total_hours * client_rate
    return total_money

    
