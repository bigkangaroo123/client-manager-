import customtkinter as ctk
import sqlite3

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Initialize main application window
window = ctk.CTk()
window.geometry('800x600')
window.title("Client Manager")

# SQLite database setup
def setup_database():
    connection = sqlite3.connect("client_manager.db")
    cursor = connection.cursor()

    # Create Clients table
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        hourly_rate REAL DEFAULT 0
                    )''')

    # Create Projects table
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        hours_spent REAL DEFAULT 0,
                        earnings REAL DEFAULT 0,
                        FOREIGN KEY(client_id) REFERENCES clients(id)
                    )''')

    # Create Tasks table
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        completed INTEGER DEFAULT 0,
                        hours_spent REAL DEFAULT 0,
                        FOREIGN KEY(project_id) REFERENCES projects(id)
                    )''')

    connection.commit()
    connection.close()

setup_database()

# Helper functions
def fetch_clients():
    connection = sqlite3.connect("client_manager.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name FROM clients")
    clients = cursor.fetchall()
    connection.close()
    return clients

def add_client_to_db(name, hourly_rate):
    connection = sqlite3.connect("client_manager.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO clients (name, hourly_rate) VALUES (?, ?)", (name, hourly_rate))
    connection.commit()
    connection.close()

def fetch_projects(client_id):
    connection = sqlite3.connect("client_manager.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, hours_spent, earnings FROM projects WHERE client_id = ?", (client_id,))
    projects = cursor.fetchall()
    connection.close()
    return projects

# UI Functions
def update_client_portals():
    for widget in client_frame.winfo_children():
        widget.destroy()

    clients = fetch_clients()
    for client_id, client_name in clients:
        client_button = ctk.CTkButton(client_frame, text=client_name, 
                                      command=lambda cid=client_id, cname=client_name: open_client_portal(cid, cname))
        client_button.pack(pady=10)

def open_add_client_window():
    add_client_window = ctk.CTkToplevel(window)
    add_client_window.geometry('400x300')
    add_client_window.title("Add Client")

    ctk.CTkLabel(add_client_window, text="Client Name:").grid(row=0, column=0, pady=10, padx=10)
    name_entry = ctk.CTkEntry(add_client_window)
    name_entry.grid(row=0, column=1, pady=10, padx=10)

    ctk.CTkLabel(add_client_window, text="Hourly Rate:").grid(row=1, column=0, pady=10, padx=10)
    rate_entry = ctk.CTkEntry(add_client_window)
    rate_entry.grid(row=1, column=1, pady=10, padx=10)

    def save_client():
        name = name_entry.get().strip()
        try:
            hourly_rate = float(rate_entry.get().strip())
        except ValueError:
            hourly_rate = 0

        if name:
            add_client_to_db(name, hourly_rate)
            update_client_portals()
            add_client_window.destroy()
        else:
            ctk.CTkLabel(add_client_window, text="Please enter a valid client name.", text_color="red").grid(row=3, columnspan=2, pady=10)

    save_button = ctk.CTkButton(add_client_window, text="Save", command=save_client)
    save_button.grid(row=2, columnspan=2, pady=20)

def open_client_portal(client_id, client_name):
    client_portal = ctk.CTkToplevel(window)
    client_portal.geometry('600x400')
    client_portal.title(client_name)

    projects = fetch_projects(client_id)

    # Header
    ctk.CTkLabel(client_portal, text=f"{client_name}'s Projects", font=("Arial", 18)).pack(pady=10)

    # Projects List
    project_frame = ctk.CTkFrame(client_portal)
    project_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for project_id, project_name, hours_spent, earnings in projects:
        project_label = ctk.CTkLabel(project_frame, text=f"{project_name}: {hours_spent} hrs, ${earnings:.2f}")
        project_label.pack(pady=5)

    def add_project():
        add_project_window = ctk.CTkToplevel(client_portal)
        add_project_window.geometry('400x300')
        add_project_window.title("Add Project")

        ctk.CTkLabel(add_project_window, text="Project Name:").grid(row=0, column=0, pady=10, padx=10)
        project_entry = ctk.CTkEntry(add_project_window)
        project_entry.grid(row=0, column=1, pady=10, padx=10)

        def save_project():
            project_name = project_entry.get().strip()
            if project_name:
                connection = sqlite3.connect("client_manager.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO projects (client_id, name) VALUES (?, ?)", (client_id, project_name))
                connection.commit()
                connection.close()
                add_project_window.destroy()
                open_client_portal(client_id, client_name)  # Refresh portal

        save_button = ctk.CTkButton(add_project_window, text="Save", command=save_project)
        save_button.grid(row=1, columnspan=2, pady=20)

    add_project_button = ctk.CTkButton(client_portal, text="Add Project", command=add_project)
    add_project_button.pack(pady=10)

# Main UI Frame
client_frame = ctk.CTkFrame(window)
client_frame.pack(fill="both", expand=True, padx=20, pady=20)

add_client_button = ctk.CTkButton(window, text="Add Client", command=open_add_client_window)
add_client_button.pack(pady=10)

update_client_portals()
window.mainloop()
