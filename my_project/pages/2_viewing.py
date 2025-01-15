import streamlit as st
import client_management_db
import datetime

st.title("📂 Your Clients")

# Function to display the task table
def display_task_table(client_name, project_name):
    st.subheader(f"📋 Task Table for {project_name} under {client_name}")

    client = client_management_db.get_client_by_name(client_name)
    client_rate = client['rate']  # To calculate money earned

    tasks = client_management_db.get_tasks_by_client_and_project(client_name, project_name)
    total_money_earned = 0  # Initialize total earnings

    if tasks:
        for task in tasks:
            task_id = task['id']
            task_name = task['task_name']
            task_deadline = datetime.datetime.strptime(task['deadline'], '%Y-%m-%d').date()
            task_notes = task['notes']
            task_complete = task['complete']
            task_hours = task['hours']

            money_earned = task_hours * client_rate
            total_money_earned += money_earned

            # Task row with editing capabilities
            columns = st.columns([0.5, 3, 3, 4, 1, 1])

            # Complete checkbox
            task_complete = columns[0].checkbox("", value=task_complete, key=f"complete_{task_id}")

            # Editable fields
            task_name = columns[1].text_input("Task Name", value=task_name, key=f"name_{task_id}")
            task_deadline = columns[2].date_input("Deadline", value=task_deadline, key=f"deadline_{task_id}")
            task_notes = columns[3].text_area("Notes", value=task_notes, key=f"notes_{task_id}")
            task_hours = columns[4].number_input("Hours", value=task_hours, step=0.5, key=f"hours_{task_id}")

            # Update task when any field changes
            if columns[5].button("Save", key=f"save_{task_id}"):
                client_management_db.update_task_db(task_id, task_name, task_deadline, task_complete, task_notes, task_hours)
                st.success(f"Task '{task_name}' updated successfully!")

            # Delete task button
            if columns[5].button("🗑️", key=f"delete_{task_id}"):
                client_management_db.delete_task_db(task_id)
                st.success(f"Task '{task_name}' deleted successfully!")
                st.experimental_rerun()

        st.markdown(f"### 💰 Total Money Earned: ${total_money_earned:.2f}")
    else:
        st.info(f"No tasks found for project '{project_name}'.")

# Main Viewing Menu
clients = client_management_db.get_all_clients()

if not clients:
    st.warning("No clients available. Add some clients first!")
else:
    client_names = [client['client_name'] for client in clients]

    # Select a client from the dropdown
    selected_client_name = st.selectbox("Select a client", client_names)

    if selected_client_name:
        selected_client = client_management_db.get_client_by_name(selected_client_name)

        st.subheader(f"Client: {selected_client['client_name']}")
        st.write(f"Hourly Rate: ${selected_client['rate']}/hour")

        # Fetch projects for the selected client
        projects = client_management_db.get_all_projects(selected_client['id'])

        if not projects:
            st.info(f"No projects found for {selected_client['client_name']}.")
        else:
            project_names = [project['project_name'] for project in projects]

            # Select a project from the dropdown
            selected_project_name = st.selectbox("Select a project", project_names)

            if selected_project_name:
                display_task_table(selected_client_name, selected_project_name)