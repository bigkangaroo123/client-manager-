import streamlit as st

#------------------- Side Bar ---------------------------
st.sidebar.title("Your Clients:")

if 'clients' not in st.session_state:
    st.session_state.clients = []
    
# Display the clients in the sidebar dropdown
client_names = [client['name'] for client in st.session_state.clients]

if client_names:
    selected_client_name = st.sidebar.selectbox("Select a client", client_names)

    selected_client = next(client for client in st.session_state.clients if client['name'] == selected_client_name)

    if 'projects' not in selected_client:
        selected_client['projects'] = []

    # Display the projects in the sidebar dropdown
    if selected_client['projects']:
        selected_project = st.sidebar.selectbox("Select a Project", selected_client['projects'])
    else:
        st.sidebar.write("No projects added for this client.")
else:
    st.sidebar.write("No clients available. Add clients to get started.")

if 'clients' not in st.session_state:
    st.session_state.clients = []  

if st.session_state.clients:
    #for loop iterating over the cient
    for client in enumerate(st.session_state.clients):
        #'client' is a dictionary

        if "projects" not in client:
            client["projects"] = []

        st.subheader(f"Client: {client['name']} (Rate: {client['rate']}/hour)")
        st.write(f"Projects for {client['name']}:")

        if client["projects"]:
            st.write(", ".join(client["projects"]))
        else:
            st.write("No projects added for this client.")
else:
    st.write("No clients have been added yet. Add clients to get started.")