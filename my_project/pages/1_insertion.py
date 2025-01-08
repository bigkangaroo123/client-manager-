import streamlit as st

if 'clients' not in st.session_state:
    st.session_state.clients = [] 
if 'client_name' not in st.session_state:
    st.session_state.client_name = ''
if 'billing_rate' not in st.session_state:
    st.session_state.billing_rate = ''

# ---------- Add client section: -------------
st.title(" ➕🤝 Add a client:")

client_name = st.text_input("Enter the name of the client:", key="client_name", placeholder="Type client's name here") #value change (try resetting input field)
billing_rate = st.text_input("Add hourly billing rate with this client", key="billing_rate", placeholder="Type billing rate here", min_value=1, step=1) 

add_client_button = st.button("Add Client", key="add_client_button")


if add_client_button:
    if not client_name:
        st.error("Please input the client's name to proceed...")
    elif not billing_rate:
        st.error("Please also input the billing rate to proceed...")
    elif not billing_rate.isdigit():
        st.error("Please enter a valid positive integer for the billing rate.")
    else:
        billing_rate = int(billing_rate)
        if billing_rate <= 0:
            st.error("Please enter a positive integer for thhe billing rate")
        else:
            client = {
                'name' : client_name,
                'rate' : billing_rate,
                'projects' : []
            }
            st.session_state.clients.append(client)
            st.success(f"Client {client_name} with hourly rate of ${billing_rate} added!")

# ---------- Add project section: -------------

st.title("➕📊 Add a project:")

if st.session_state.clients:
    client_names = []
    for client in st.session_state.clients:
        client_names.append(client["name"])

    selected_client_name = st.selectbox("Select a client", client_names)

    selected_client = None
    # Loop through the clients to find the selected client
    for client in st.session_state.clients:
        if client['name'] == selected_client_name:
            selected_client = client
            break

    project_name = st.text_input("Enter the name of the project:", placeholder="Type project's name here")
    add_project_button = st.button("Add Project")
    
    if add_project_button:
        if project_name and project_name not in selected_client['projects']:
            selected_client['projects'].append(project_name)
            st.success(f"Project '{project_name}' added to {selected_client_name}!")
        else:
            st.error("Please enter a valid project name that doesn't already exist.")
else:
    st.write("No clients available. Add a client first.")
