import streamlit as st
import client_manager_db

# -------------- Task Table -----------------
# 1st column: checkbox
# 2nd: task name
# 3rd: deadline
# 4th: notes

def task_table(client_name, project_name):
    st.subheader(f"📋 Task Table for {project_name} under {client_name}")

    # Add Task Button
    if st.button("Add Task"):
        task_name = st.text_input("Enter Task Name", placeholder="Task Name")
        deadline = st.date_input("Select Deadline", value=None)
        notes = st.text_area("Enter Notes", height=100)

        # Check if task data is filled before adding it to the database
        if task_name and deadline and notes:
            # Fetch client_id using client_name
            clients = client_manager_db.get_all_clients()
            client_id = None
            for client in clients:
                if client['name'] == client_name:
                    client_id = client['id']
                    break

            if client_id:
                # Add task to the database
                client_manager_db.add_task_db(client_id, project_name, task_name, deadline, notes)
                st.success(f"Task '{task_name}' added to project '{project_name}' under client '{client_name}'!")
            else:
                st.error("Client not found.")
        else:
            st.error("Please fill all task details.")
    
    # Retrieve and display tasks from the database for the selected project
    conn = client_manager_db.get_db_connection()
    tasks = conn.execute("""
        SELECT * FROM tasks WHERE client_id = (SELECT id FROM clients WHERE name = ?) 
        AND project_name = ?
    """, (client_name, project_name)).fetchall()
    
    if tasks:
        for task in tasks:
            task_name = task['task_name']
            task_deadline = task['deadline']
            task_notes = task['notes']
            task_complete = task['complete']
            task_id = task['id']  # Get the task ID for deleting

            columns = st.columns([0.5, 3, 3, 4, 1])

            task_complete = columns[0].checkbox("", value=task_complete)

            task_deadline = columns[1].date_input("Deadline", value=task_deadline)
            task_name = columns[2].text_input("Task Name", value=task_name)
            task_notes = columns[3].text_area("Notes", value=task_notes, height=100)

            # Delete Task Button
            if columns[4].button("🗑️", key=f"delete{task_id}"):
                # Handle deleting the task from the database
                client_id = None
                clients = client_manager_db.get_all_clients()
                for client in clients:
                    if client['name'] == client_name:
                        client_id = client['id']
                        break

                if client_id:
                    # Call the delete_task_db function with task_id, client_id, and project_name
                    client_manager_db.delete_task_db(task_id, client_id, project_name)
                    st.success(f"Task '{task_name}' deleted successfully!")
                    st.experimental_rerun()  # Re-run the app to reflect the changes
                else:
                    st.error("Client not found for deletion.")
    else:
        st.info(f"No tasks found for project '{project_name}'.")

# -------------- Main Viewing Menu ----------------

selected_client = None

if 'clients' not in st.session_state or not st.session_state.clients:
    st.warning("No clients available. Add some clients first!")
else:
    client_names = []
    for client in st.session_state.clients:
        client_names.append(client['name'])

    selected_client_name = st.selectbox("Select a client", ["All Clients"] + client_names)

    if selected_client_name != "All Clients":
        for client in st.session_state.clients:
            if client['name'] == selected_client_name:
                selected_client = client
                break
        
        st.subheader(f"Client: {selected_client['name']}")
        st.write(f"Hourly Rate: ${selected_client['rate']}/hour")

        if 'projects' not in selected_client or not selected_client['projects']:
            st.info(f"No projects found for {selected_client_name}.")
        else:
            selected_project = st.selectbox(
                f"Projects for {selected_client['name']}", ["All Projects"] + selected_client['projects'])

            if selected_project != "All Projects":  # When a project is selected, display its task table
                task_table(selected_client['name'], selected_project)
            else:
                st.write(f"Projects under {selected_client['name']}:")
                st.write(", ".join(selected_client['projects']))
    else:
        st.subheader("All Clients and Their Projects")
        for client in st.session_state.clients:
            st.write(f"**{client['name']}** (Rate: ${client['rate']}/hour)")
            if 'projects' in client and client['projects']:
                st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;Projects: {', '.join(client['projects'])}")  # The weird code at the start is necessary for indenting
            else:
                st.write("This client has no projects added.")