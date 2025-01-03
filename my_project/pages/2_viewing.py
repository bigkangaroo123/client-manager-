import streamlit as st

st.title("View Clients")

#---------------------side bar --------------------
if 'clients' not in st.session_state or not st.session_state.clients:
    st.warning("No clients available. Add some clients first!")
else:
    st.sidebar.title("📂 Your Clients")
    
    # dropdown for clients:
    for client in st.session_state.clients:
        client_names = client['name']

    selected_client_name = st.sidebar.selectbox("Select a client", ["All Clients"], + client_names)

    if selected_client_name != "All Clients": #if a client is selected:
        selected_client = None
        for client in st.session_state.clients:
            if client['name'] == selected_client_name:
                selected_client = client
                break
        
        st.subheader(f"Client: {selected_client['name']}")
        st.write(f"Hourly Rate: ${selected_client['rate']}/hour")

        #if client has no proejcts:
        if 'projects' not in selected_client or not selected_client['projects']:
            st.info(f"No projects found for {selected_client_name}.")
        else:
            selected_project = st.sidebar.selectbox(
                f"Projects for {selected_client['name']}",
                ["All Projects"] + selected_client['projects']
            )

            if selected_project != "All Projects": #if a project is selected:
                st.write(f"Viewing details for **{selected_project}** under **{selected_client['name']}**.")
            else:
                # displayign all projects:
                st.write(f"Projects under {selected_client['name']}:")
                st.write(", ".join(selected_client['projects']))
    else:
        st.subheader("All Clients and Their Projects")
        for client in st.session_state.clients:
            st.write(f"**{client['name']}** (Rate: ${client['rate']}/hour)")
            if 'projects' in client and client['projects']:
                st.write(f"Projects: {', '.join(client['projects'])}")
            else:
                st.write("This client has no projects added")

