import streamlit as st

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

# Sidebar - Main menu
with st.sidebar:
    st.header("EasyManage")

    # clients dropdown
    #i asked chatgpt for help with this part is it fine? (i understand what it means tho)
    client_select = st.selectbox("Add a client", ["-- Add a client --"] + st.session_state.clients)

    #drop down for each client and project
    if client_select != "-- Add a client --": 
        if client_select in st.session_state.projects and st.session_state.projects[client_select]:
            project_select = st.selectbox(f"Add a project under {client_select}", ["-- Add a project --"] + st.session_state.projects[client_select]) 
        else:
            project_select = None
            st.write(f"No projects available for {client_select}.")

#home page(adding clients)
if client_select == "-- Add a client --":
    st.title("Welcome to EasyManage!")

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
            st.session_state.projects[client_name] = []  #creating a projects list for that specific client (will be useful later for diff tabs)
            st.success(f"Client {client_name} added!")
        else:
            st.error("Please enter both a client name and a billing rate.")

# diff page for each client
if client_select != "-- Add a client --":
    st.title(f"Projects for {client_select}")

    # adding projcet
    project_name = st.text_input(f"Enter the name of the project for {client_select}")
    add_project_button = st.button(f"Add Project for {client_select}")

    if add_project_button and project_name:
        st.session_state.projects[client_select].append(project_name) 
        st.success(f"Added project {project_name} for client {client_select}!")

    # display projects for that selected client
    if st.session_state.projects[client_select]:
        st.write("Projects:")
        for project in st.session_state.projects[client_select]:
            st.write(f"- {project}")
    else:
        st.write(f"No projects yet for {client_select}.")
