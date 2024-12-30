import streamlit as st

st.set_page_config(
    page_title="EasyManage",
    page_icon="🗿",
)
st.sidebar.success("Select a page above")

#initializing variables is they dont exist
if 'clients' not in st.session_state:
    st.session_state.clients = [] #list that stores clients
if 'project' not in st.session_state:
    st.session_state.projects = {}
if 'current_page' not in st.session_state:
    st.session_state.page = 'Home' #a variable that tracks the current page

#if the page we are on is home:
if st.session_state.page == 'Home':
    st.title("EasyManage")
    st.write("This is a user-friendly client manager.")

    #adding a client:
    client_name = st.text_input("Enter the name of the client")

    #creating button to add the lcient:
    add_client_button = st.button("Add Client")
    if not client_name and add_client_button:
        st.error("Please enter a valid client name")
    elif client_name and add_client_button:
        st.session_state.clients.append(client_name)
        st.success(f"Client {client_name} added!")
    
    #clients as buttons that lead to a diff tab for each client
    if st.session_state.clients:
        st.write("Click on a client to see their projects:")
        for client in st.session_state.clients:
            if st.button(client):
                st.session_state.selected_client = client
                st.session_state.page = client  # change page to the selected client's name. i did this but idk how to open a whole different page when I click a client




