<<<<<<< HEAD
import streamlit as st

st.title("View Clients")
st.write("You can view each client's projects in the dropdown!")

# Sidebar - Client Dropdown
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
    # Loop through each client
    for idx, client in enumerate(st.session_state.clients):
        # 'client' is the dictionary containing the client's details.

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
=======
import streamlit as st
from pages import insertion
from streamlit_extras.switch_page_button import switch_page

st.title("View Clients")

if 'clients' not in st.session_state:
    st.session_state.clients = []  

if st.session_state.clients:
    st.write("Here are the added clients:")
    for client in st.session_state.clients:
        st.write(f"- **Name:** {client['name']} | **Billing Rate:** {client['rate']}/hour")
else:
    st.write("No clients have been added yet.")

if not st.session_state.clients:
    st.write("You currently have 0 clients added, click the button below to add a client")
    add_client = st.button("Add Client", key="add_client_in_viewing_page")
    if add_client:
        switch_page(insertion)
>>>>>>> 82a7b8034ee932020eb8626624fcf43d299eac17
