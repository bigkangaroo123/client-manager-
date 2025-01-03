import streamlit as st

st.title("Add a client:")

if 'clients' not in st.session_state:
    st.session_state.clients = [] 
if 'client_name' not in st.session_state:
    st.session_state.client_name = ''
if 'billing_rate' not in st.session_state:
    st.session_state.billing_rate = ''


client_name = st.text_input("Enter the name of the client:", key="client_name", value=st.session_state.client_name)
billing_rate = st.text_input("Add hourly billing rate with this client", key="billing_rate", value=st.session_state.billing_rate)

add_client_button = st.button("Add Client", key="add_client_button")


if add_client_button:
    if not client_name:
        st.error("Please input the client's name to proceed...")
    elif not billing_rate:
        st.error("Please also input the billing rate to proceed...")
    else:
        #chat gpt suggested the "try" method
        try:
            billing_rate = int(billing_rate)
            if billing_rate <= 0:
                st.error("Please enter a positive integer for the billing rate.")
            else:
                st.session_state.clients.append({"name": client_name, "rate": billing_rate})
                st.success(f"Client '{client_name}' with rate ${billing_rate}/hour added!")
        except ValueError:
            st.error("Please enter a valid integer for the billing rate.")

# ---------- Add project section: -------------

st.title("Add a project:")

if 'clients' not in st.session_state:
    st.session_state.clients = []

if st.session_state.clients:
    # Dropdown to select which client to add a project to
    client_names = [client['name'] for client in st.session_state.clients]
    selected_client_name = st.selectbox("Select a client", client_names)

    selected_client = None
    # Loop through the clients to find the selected client
    for client in st.session_state.clients:
        if client['name'] == selected_client_name:
            selected_client = client
            break  # Stop once the client is found

    if selected_client:
        if 'projects' not in selected_client:
            selected_client['projects'] = []
        
        project_name = st.text_input("Enter the name of the project:")
        add_project_button = st.button("Add Project")
        
        if add_project_button:
            if project_name and project_name not in selected_client['projects']:
                selected_client['projects'].append(project_name)
                st.success(f"Project '{project_name}' added to {selected_client_name}!")
            else:
                st.error("Please enter a valid project name that doesn't already exist.")
else:
    st.write("No clients available. Add a client first.")