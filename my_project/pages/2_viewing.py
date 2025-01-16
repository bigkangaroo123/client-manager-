import streamlit as st
import client_management_db
import datetime

st.title("📂 Your Clients")

# Function to display the task table
def display_task_table(client_name, project_name, project_id):
    st.subheader(f"📋 Task Table for {project_name} under {client_name}")

    client = client_management_db.get_client_by_name(client_name)
    client_rate = client['rate']  # To calculate money earned

    tasks = client_management_db.get_tasks_by_client_and_project(client['id'], project_id)
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
            columns = st.columns([0.5, 3, 3, 4, 1, 1, 1])

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
            if columns[6].button("🗑️", key=f"delete_{task_id}"):
                client_management_db.delete_task_db(client['id'], project_id, task_id)
                st.success(f"Task '{task_name}' deleted successfully!")
                st.rerun()

        st.markdown(f"### 💰 Total Money Earned: ${total_money_earned:.2f}")
    else:
        st.info(f"No tasks found for project '{project_name}'.")

#--------------------Main Viewing Menu-----------------------
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
            project_options = [{"name": project['project_name'], "id": project['id']} for project in projects]

            # Create a dropdown showing only project names
            project_names = [project['name'] for project in project_options]
            selected_project_name = st.selectbox("Select a project", project_names)

            if selected_project_name:
                # Get the ID of the selected project
                selected_project_id = next(
                    project['id'] for project in project_options if project['name'] == selected_project_name
                )

                # Pass both the client name and project ID to the display_task_table function
                display_task_table(selected_client_name, selected_project_name, selected_project_id)
