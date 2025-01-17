import streamlit as st
import client_management_db
import datetime

client_management_db.init_db()

st.title("📂 Your Clients")

def add_task(client_id, project_id):
    st.subheader("➕ Add a Task")
    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("Task Name")
        deadline = st.date_input("Deadline", min_value=datetime.date.today())
        notes = st.text_area("Notes")
        hours = st.number_input("Hours", step=0.5, min_value=0.0)
        submitted = st.form_submit_button("Save Task")
        if submitted:
            if not task_name.strip():
                st.error("Task Name is required!")
            else:
                # Add task to database if the above cases are false
                client_management_db.add_task_db(client_id, project_id, task_name, deadline, notes, hours)
                st.success("Task added successfully!")
                st.rerun()

def display_tasks(client_id, project_id):
    tasks = client_management_db.get_tasks_by_client_and_project(client_id, project_id)

    client_rate = client_management_db.get_client_by_id(client_id)['rate']

    if tasks:
        st.markdown("### Your Tasks:")
        for task in tasks:
            task_id = task['id']
            task_complete = task['complete']
            task_name = task['task_name']
            task_deadline = task['deadline']
            task_notes = task['notes']
            task_hours = task['hours']

            columns = st.columns([1, 3, 3, 3, 2, 1, 1])

            # Status Checkbox
            is_complete = columns[0].checkbox("", value=task_complete, key=f"status_{task_id}")
            if is_complete != task_complete:
                client_management_db.update_task_status(task_id, is_complete)

            # Task Details
            columns[1].text(task_name)
            columns[2].text(task_deadline)
            columns[3].text(task_notes)
            columns[4].text(f"{task_hours} hours")

            # Edit Button
            if columns[5].button("✏️", key=f"edit_{task_id}"):
                with st.form(f"edit_task_form_{task_id}"):
                    new_task_name = st.text_input("New Task Name", value=task_name)
                    new_deadline = st.date_input("New Task Deadline", value=datetime.datetime.strptime(task_deadline, '%Y-%m-%d').date())
                    new_notes = st.text_area("New Task Notes", value=task_notes)
                    new_hours = st.number_input("New Task Hours", value=task_hours, step=0.5, min_value=0.0)
                    edited = st.form_submit_button("Save Changes")

                    if edited:
                        try:
                            client_management_db.update_task_details(
                                client_id=client_id,
                                project_id=project_id,
                                task_id=task_id,
                                task_name=new_task_name,
                                deadline=new_deadline,
                                notes=new_notes,
                                hours=new_hours
                            )
                            st.success(f"Task '{new_task_name}' updated successfully!")
                            st.rerun()  # Refresh the app to show updated values
                        except Exception as e: #the try and except methods help with error handling
                            st.error(f"Failed to update task: {str(e)}")


            # Delete Button
            if columns[6].button("🗑️", key=f"delete_{task_id}"):
                client_management_db.delete_task(client_id, project_id, task_id)
                st.success(f"Task '{task_name}' deleted successfully!")
                st.rerun()

        total_earnings = client_management_db.get_total_money_earned(client_id, project_id)
        st.markdown(f"**💰 Total Earnings for this project:** ${total_earnings:.2f}")

    else:
        st.info("No tasks found for this project.")

# ----------Main Viewing Menu -----------------
clients = client_management_db.get_all_clients()

if not clients:
    st.warning("No clients available. Add some clients first!")
else:
    client_names = [client['client_name'] for client in clients]
    selected_client_name = st.selectbox("Select a client", client_names)

    if selected_client_name:
        selected_client = client_management_db.get_client_by_name(selected_client_name)
        st.subheader(f"Client: {selected_client['client_name']}")
        st.write(f"Hourly Rate: ${selected_client['rate']}/hour")

        projects = client_management_db.get_all_projects(selected_client['id'])

        if not projects:
            st.info(f"No projects found for {selected_client['client_name']}.")
        else:
            project_options = [{"name": project['project_name'], "id": project['id']} for project in projects]
            project_names = [project['name'] for project in project_options]
            selected_project_name = st.selectbox("Select a project", project_names)

            if selected_project_name:
                selected_project_id = next(project['id'] for project in project_options if project['name'] == selected_project_name)

                # Display both Add Task and Display Tasks functions
                add_task(selected_client['id'], selected_project_id)
                display_tasks(selected_client['id'], selected_project_id)
