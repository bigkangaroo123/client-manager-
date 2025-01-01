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
