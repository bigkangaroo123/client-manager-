import streamlit as st
import client_manager_db

# ---------- Add client section: -------------
st.title(" ➕🤝 Add a client:")

client_name = st.text_input("Enter the name of the client:", placeholder="Type client's name here")
billing_rate = st.text_input("Add hourly billing rate with this client", placeholder="Type billing rate here") 

add_client_button = st.button("Add Client")

if add_client_button:
    if not client_name:
        st.error("Please input the client's name to proceed...")
    elif client_manager_db.get_client_by_name(client_name):
        st.error("Please input a client that does not already exist")
    elif not billing_rate:
        st.error("Please also input the billing rate to proceed...")
    elif not billing_rate.isdigit():
        st.error("Please enter a valid positive integer for the billing rate.")
    else:
        billing_rate = int(billing_rate)
        if billing_rate <= 0:
            st.error("Please enter a positive integer for the billing rate")
        else:
            client_manager_db.add_client_db(client_name, billing_rate)
            st.success(f"Client {client_name} with hourly rate of ${billing_rate} added!")

# ---------- Add project section: -------------
st.title("➕📊 Add a project:")

clients = client_manager_db.get_all_clients()  # Fetch clients directly from database

if clients:
    client_names = [client['client_name'] for client in clients]
    selected_client_name = st.selectbox("Select a client", client_names)

    selected_client = None
    for client in clients:
        if client['client_name'] == selected_client_name:
            selected_client = client
            break

    # Fetch projects for the selected client
    projects = client_manager_db.get_all_projects(selected_client['id'])

    project_names = [project['project_name'] for project in projects]

    project_name = st.text_input("Enter the name of the project:", placeholder="Type project's name here")
    add_project_button = st.button("Add Project")
    
    if add_project_button:
        if project_name and project_name not in project_names:
            client_manager_db.add_project_db(selected_client['id'], project_name)
            st.success(f"Project '{project_name}' added to {selected_client_name}!")
        else:
            st.error("Please enter a valid project name that doesn't already exist.")
else:
    st.write("No clients available. Add a client first.")