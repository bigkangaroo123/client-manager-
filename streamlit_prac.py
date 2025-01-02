import streamlit as st
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('project_management.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, hourly_rate REAL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, client_id INTEGER, name TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, project_id INTEGER, description TEXT, completed BOOLEAN, hours_spent REAL)''')

# Function to display client-specific page
def client_page(client_name):
    # Fetch client data from DB
    cursor.execute("SELECT * FROM clients WHERE name=?", (client_name,))
    client = cursor.fetchone()
    hourly_rate = client[2] if client else None
    
    # Show hourly rate input and update if necessary
    if hourly_rate is None:
        hourly_rate = st.number_input(f"Enter hourly rate for {client_name}:", min_value=0.0, step=0.5)
        if hourly_rate:
            add_client(client_name, hourly_rate)
            st.success(f"Hourly rate for {client_name} is set to {hourly_rate}")
    
    # Fetch and display projects for this client
    cursor.execute("SELECT * FROM projects WHERE client_id=?", (client[0],))
    projects = cursor.fetchall()
    
    # Add new project for the client
    project_name = st.text_input(f"Add a project for {client_name}:")
    if st.button(f"Add Project for {client_name}") and project_name:
        cursor.execute("INSERT INTO projects (client_id, name) VALUES (?, ?)", (client[0], project_name))
        conn.commit()
        st.success(f"Project '{project_name}' added!")
    
    # Display the projects in a dropdown
    if projects:
        project_names = [project[2] for project in projects]
        selected_project = st.selectbox("Select a project:", project_names)
        if selected_project:
            project_id = [project[0] for project in projects if project[2] == selected_project][0]
            project_page(client_name, selected_project, project_id)

# Function to display project page (tasks and hours)
def project_page(client_name, project_name, project_id):
    st.write(f"Managing tasks for project: {project_name}")
    
    # Add tasks for the project
    task_name = st.text_input(f"Add a task for project '{project_name}':")
    if st.button(f"Add Task for {project_name}") and task_name:
        cursor.execute("INSERT INTO tasks (project_id, description, completed, hours_spent) VALUES (?, ?, ?, ?)", 
                       (project_id, task_name, False, 0.0))
        conn.commit()
        st.success(f"Task '{task_name}' added to project '{project_name}'")
    
    # Fetch tasks for this project
    cursor.execute("SELECT * FROM tasks WHERE project_id=?", (project_id,))
    tasks = cursor.fetchall()
    
    if tasks:
        for task in tasks:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(task[2])
            with col2:
                completed = st.checkbox(f"Complete task '{task[2]}'", value=task[3])
                if completed != task[3]:
                    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task[0]))
                    conn.commit()
                
                if completed:
                    hours = st.number_input(f"Enter hours for '{task[2]}':", min_value=0.0, step=0.5)
                    cursor.execute("UPDATE tasks SET hours_spent = ? WHERE id = ?", (hours, task[0]))
                    conn.commit()
                    st.write(f"Money earned from task: {hours * get_hourly_rate(client_name)}")

# Function to get the hourly rate for a client
def get_hourly_rate(client_name):
    cursor.execute("SELECT hourly_rate FROM clients WHERE name=?", (client_name,))
    result = cursor.fetchone()  # Fetch the result once
    if result:
        return result[0]  # Return hourly rate
    else:
        return 0  # Return 0 if no client found

# Function to display project page (tasks and hours)
def project_page(client_name, project_name, project_id):
    st.write(f"Managing tasks for project: {project_name}")
    
    # Add tasks for the project
    task_name = st.text_input(f"Add a task for project '{project_name}':")
    if st.button(f"Add Task for {project_name}") and task_name:
        cursor.execute("INSERT INTO tasks (project_id, description, completed, hours_spent) VALUES (?, ?, ?, ?)", 
                       (project_id, task_name, False, 0.0))
        conn.commit()
        st.success(f"Task '{task_name}' added to project '{project_name}'")
    
    # Fetch tasks for this project
    cursor.execute("SELECT * FROM tasks WHERE project_id=?", (project_id,))
    tasks = cursor.fetchall()
    
    if tasks:
        for task in tasks:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(task[2])
            with col2:
                completed = st.checkbox(f"Complete task '{task[2]}'", value=task[3])
                if completed != task[3]:
                    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task[0]))
                    conn.commit()
                
                if completed:
                    hours = st.number_input(f"Enter hours for '{task[2]}':", min_value=0.0, step=0.5)
                    cursor.execute("UPDATE tasks SET hours_spent = ? WHERE id = ?", (hours, task[0]))
                    conn.commit()
                    st.write(f"Money earned from task: {hours * get_hourly_rate(client_name)}")


# Function to add a new client
def add_client(client_name, hourly_rate):
    cursor.execute("INSERT INTO clients (name, hourly_rate) VALUES (?, ?)", (client_name, hourly_rate))
    conn.commit()

# Main app page
def main():
    st.title("EasyManage - Client & Project Manager")
    
    # Light/Dark mode toggle
    mode = st.selectbox("Choose mode", ["Light Mode", "Dark Mode"])
    if mode == "Dark Mode":
        st.markdown("""
            <style>
                body {
                    background-color: #121212;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body {
                    background-color: white;
                    color: black;
                }
            </style>
        """, unsafe_allow_html=True)

    # Display clients and manage them
    st.sidebar.title("Navigation")
    
    # Fetch all clients
    clients = [client[1] for client in cursor.execute("SELECT * FROM clients").fetchall()]
    clients.insert(0, "Add New Client")  # Add option to add new client at the top
    
    selected_client = st.sidebar.selectbox("Select a client", clients)
    
    # Dropdown for each client to show their projects
    if selected_client == "Add New Client":
        new_client_name = st.text_input("Enter new client name:")
        hourly_rate = st.number_input("Enter hourly rate for new client:", min_value=0.0, step=0.5)
        if st.button("Add Client"):
            if new_client_name and hourly_rate > 0:
                add_client(new_client_name, hourly_rate)
                st.success(f"Client '{new_client_name}' added successfully!")
            else:
                st.error("Please enter a valid client name and hourly rate")
    elif selected_client:
        # Create a dropdown under the selected client to choose projects
        cursor.execute("SELECT * FROM projects WHERE client_id = (SELECT id FROM clients WHERE name = ?)", (selected_client,))
        projects = cursor.fetchall()
        
        if projects:
            project_names = [project[2] for project in projects]
            selected_project = st.sidebar.selectbox(f"Select a project for {selected_client}", project_names)
            if selected_project:
                project_id = [project[0] for project in projects if project[2] == selected_project][0]
                client_page(selected_client)  # Show the client page after project is selected

if __name__ == "__main__":
    main()