import streamlit as st
import pandas as pd

# Setting up the page configuration
st.set_page_config(
    page_title="EasyManage",
    page_icon="🗿",
)

# Initializing session state variables if they don't exist
if 'clients' not in st.session_state:
    st.session_state.clients = []  # List to store client names
if 'projects' not in st.session_state:
    st.session_state.projects = {}  # Dictionary to store projects for each client
if 'tasks' not in st.session_state:
    st.session_state.tasks = {} #dict. to store tasks for each project of that client

#initiliazing this variable cuz we need it later for the tasks page
project_select = None

# Sidebar - Main menu
with st.sidebar:
    st.header("EasyManage")

    # Clients dropdown
    client_select = st.selectbox("Select a client", ["-- Add a client --"] + st.session_state.clients)

    if client_select != "-- Add a client --":
        # Client-specific dropdown to select a project for the selected client
        if client_select in st.session_state.projects and st.session_state.projects[client_select]:
            project_select = st.selectbox(f"Select a project under {client_select}", ["-- Select a project --"] + st.session_state.projects[client_select])
        else:
            project_select = None
            st.write(f"No projects yet for {client_select}.")

# Home page - For adding clients
if client_select == "-- Add a client --":
    st.title("Welcome to EasyManage!")

    # Adding a client
    client_name = st.text_input("Enter the name of the client")
    billing_rate = st.text_input("Add hourly billing rate with this client")

    add_client_button = st.button("Add Client")

    if add_client_button:
        if client_name:
            billing_rate = int(billing_rate)
            if billing_rate <= 0:
                st.error("Billing rate should be a positive integer value")
        if client_name and billing_rate:
            st.session_state.clients.append(client_name)
            st.session_state.projects[client_name] = []  # Initialize an empty list of projects for the client
            st.success(f"Client '{client_name}' added!")
        else:
            st.error("Please enter both a client name and a billing rate.")

# Client-specific page (for each client)
if client_select != "-- Add a client --":
    st.title(f"Projects for {client_select}")

    # Add project
    project_name = st.text_input(f"Enter the name of the project for {client_select}")
    add_project_button = st.button(f"Add Project for {client_select}")

    if add_project_button and project_name:
        st.session_state.projects[client_select].append(project_name)  # Add the project to the client's list
        st.success(f"Added project '{project_name}' for client '{client_select}'!")

    # Display the list of projects for the selected client
    if st.session_state.projects[client_select]:
        st.write("Projects:")
        for project in st.session_state.projects[client_select]:
            st.write(f"- {project}")
    else:
        st.write(f"No projects yet for {client_select}.")

#project specific page:
if project_select and project_select != "-- Select a project --":
    st.title(f"Tasks for {project_select} (Client: {client_select})")

    # Adding a task
    task_name = st.text_input("Task Name")
    personal_deadline = st.date_input("Personal Deadline")
    notes = st.text_area("Notes")
    add_task_button = st.button("Add Task")

    # Handle adding tasks
    if add_task_button:
        if task_name:
            task = {
                "Task Name": task_name,
                "Personal Deadline": str(personal_deadline),
                "Notes": notes,
                "Completed": False,
            }
            st.session_state.tasks[f"{client_select}_{project_select}"].append(task)
            st.success(f"Task '{task_name}' added!")
        else:
            st.error("Please enter a task name.")

    # Display tasks in a table
    if f"{client_select}_{project_select}" in st.session_state.tasks:
        tasks = st.session_state.tasks[f"{client_select}_{project_select}"]

        if tasks:
            st.write("Tasks:")
            task_df = pd.DataFrame(tasks)
            for i, task in enumerate(tasks):
                cols = st.columns([3, 2, 3, 1])  # Adjust column widths
                cols[0].write(task["Task Name"])
                cols[1].write(task["Personal Deadline"])
                cols[2].write(task["Notes"])
                completed = cols[3].checkbox("Done", value=task["Completed"], key=f"task_{i}")

                # Update task completion status
                if completed != task["Completed"]:
                    task["Completed"] = completed
                    st.success(f"Task '{task['Task Name']}' marked as {'completed' if completed else 'not completed'}.")
        else:
            st.write("No tasks added yet.")
    