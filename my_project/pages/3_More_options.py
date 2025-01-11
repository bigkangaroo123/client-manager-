import streamlit as st
from streamlit_option_menu import option_menu


selected = option_menu(
    menu_title="More Options",
    options=["✏️Edit", "📦Archive", "🗑️Delete"],
    orientation="horizontal",
)

# ---------- editing-------------
def edit(): 
    if 'clients' not in st.session_state or not st.session_state.clients:
        st.warning("No clients or projects available. Add some first!")
    else:
        client_names = [client['name'] for client in st.session_state.clients]
        selected_client_name = st.selectbox("Select a client to edit", client_names)

        selected_client = None
        for client in st.session_state.clients:
            if client['name'] == selected_client_name:
                selected_client = client
                break

        if selected_client:
            st.subheader(f"Editing Client: {selected_client_name}")

            new_client_name = st.text_input("Edit client name:", value=selected_client['name'])
            new_billing_rate = st.text_input("Edit hourly billing rate:", value=str(selected_client['rate']))

            if st.button("Save Changes to Client"):
                try:
                    new_billing_rate = int(new_billing_rate)
                    if new_billing_rate > 0:
                        selected_client['name'] = new_client_name
                        selected_client['rate'] = new_billing_rate
                        st.success("Client details updated successfully!")
                    else:
                        st.error("Please enter a positive integer for the billing rate.")
                except ValueError:
                    st.error("Please enter a valid integer for the billing rate.")

            st.subheader(f"Projects for {selected_client_name}")
            if "projects" not in selected_client or not selected_client["projects"]:
                st.write("No projects available for this client.")
            else:
                project_name = st.selectbox("Select a project to edit", selected_client["projects"])
                new_project_name = st.text_input("Edit project name:", value=project_name)

                if st.button(f"Save Changes to Project '{project_name}'"):
                    if new_project_name and new_project_name != project_name:
                        project_index = selected_client["projects"].index(project_name)
                        selected_client["projects"][project_index] = new_project_name
                        st.success(f"Project name updated to '{new_project_name}'!")
                    else:
                        st.error("Please enter a valid and different project name.")
                        
# ---------- archiving / unarchiving -------------
def archive():
    if 'clients' not in st.session_state or not st.session_state.clients:
        st.warning("No clients or projects available. Add some first!")

    if 'archived_clients' not in st.session_state:
        st.session_state.archived_clients = []

    if 'archived_projects' not in st.session_state:
        st.session_state.archived_projects = {}  # it will be stored as client: projects
    else:
        st.subheader("Archive / Unarchive Options")

        action_type = st.radio("What would you like to do?", ("Archive", "Unarchive"))

        if action_type == "Archive":
            archive_type = st.radio("What would you like to archive?", ("Client", "Project"))

            if archive_type == "Client":
                client_names = [client['name'] for client in st.session_state.clients]
                selected_client_name = st.selectbox("Select a client to archive", client_names)

                if st.button(f"Archive Client '{selected_client_name}'"):
                    st.session_state.archived_clients.append(selected_client_name)
                    st.session_state.clients = [client for client in st.session_state.clients if client['name'] != selected_client_name]

            elif archive_type == "Project":
                client_names = [client['name'] for client in st.session_state.clients]
                selected_client_name = st.selectbox("Select a client", client_names)

                selected_client = None
                if selected_client_name != "All Clients":
                    for client in st.session_state.clients:
                        if client['name'] == selected_client_name:
                            selected_client = client
                            break

                if selected_client and "projects" in selected_client and selected_client["projects"]:
                    project_name = st.selectbox("Select a project to archive", selected_client["projects"])

                    if st.button(f"Archive Project '{project_name}'"):
                        if selected_client_name not in st.session_state.archived_projects:
                            st.session_state.archived_projects[selected_client_name] = []

                        st.session_state.archived_projects[selected_client_name].append(project_name)
                        selected_client["projects"].remove(project_name)

                        st.success(f"Project '{project_name}' has been archived!")
                        
                else:
                    st.warning("No projects available for the selected client.")

        elif action_type == "Unarchive":
            unarchive_type = st.radio("What would you like to unarchive?", ("Client", "Project"))

            if unarchive_type == "Client":
                if not st.session_state.archived_clients:
                    st.warning("No clients are archived")
                else:
                    archived_client_names = st.session_state.archived_clients
                    selected_client_name = st.selectbox("Select a client to unarchive", archived_client_names)

                    if selected_client_name:
                        if st.button(f"Unarchive Client '{selected_client_name}'"):
                            archived_client = st.session_state.archived_clients.pop(st.session_state.archived_clients.index(selected_client_name))
                            st.session_state.clients.append({'name': archived_client, 'projects': []})  # Add back with empty projects list (adjust accordingly)

                            st.success(f"Client '{selected_client_name}' has been unarchived!")

            elif unarchive_type == "Project":
                if not st.session_state.archived_projects:
                    st.warning("No archived projects")
                else:
                    archived_project_names = []
                    for client_name, projects in st.session_state.archived_projects.items():
                        for project in projects:
                            archived_project_names.append((client_name, project))

                    selected_client_name, selected_project_name = st.selectbox(
                        "Select a project to unarchive", archived_project_names, format_func=lambda x: f"{x[0]} - {x[1]}"
                        #format_func:
                        #x is a tuple of (client name, project name)
                        #it will be displayed like that
                    )

                    if selected_client_name and selected_project_name:
                        if st.button(f"Unarchive Project '{selected_project_name}'"):
                            if selected_client_name in st.session_state.archived_clients:
                                st.warning(f"Client '{selected_client_name}' is archived. Please unarchive the client first.")
                            else:
                                st.session_state.archived_projects[selected_client_name].remove(selected_project_name)

                                if not st.session_state.archived_projects[selected_client_name]:
                                    del st.session_state.archived_projects[selected_client_name]

                                for client in st.session_state.clients:
                                    if client["name"] == selected_client_name:
                                        client["projects"].append(selected_project_name)
                                        break

                                st.success(f"Project '{selected_project_name}' has been unarchived and restored to client '{selected_client_name}'!")
                                
# ---------- deleting -------------
def delete():
    if 'clients' not in st.session_state or not st.session_state.clients:
        st.warning("No clients or projects available. Add some first!")

    action_type = st.radio("What would you like to delete?", ("Client", "Project"))

    if action_type == "Client":
        client_names = [client['name'] for client in st.session_state.clients]
        selected_client_name = st.selectbox("Select a client to delete", client_names)
    
        if selected_client_name:
            if st.button("Delete Client"):
                st.warning("Are you sure you want to permanantly delete this client?")
                confirm_delete = st.radio("Choose an option: ", ("No", "Yes"))
    
                if confirm_delete == "Yes":
                    selected_client = None
                    for client in st.session_state.clients:
                        if client['name'] == selected_client_name:
                            selected_client = client
                            break
                    st.session_state.clients.remove(selected_client)
                    st.success(f"Client {selected_client_name} has been deleted")
    
                elif confirm_delete == "No":
                    st.success(f"Client deletion cancelled")
            

    elif action_type == "Project":
        client_names = [client['name'] for client in st.session_state.clients]
        selected_client_name = st.selectbox("Select a client to delete", client_names)

        selected_client = None
        if selected_client_name != "All Clients":
            for client in st.session_state.clients:
                if client['name'] == selected_client_name:
                    selected_client = client
                    break

        if selected_client and "projects" in selected_client and selected_client["projects"]:
            project_name = st.selectbox("Select a project to delete", selected_client["projects"])

            if st.button("Delete project"):
                #ADD WARNING
                selected_client["projects"].remove(project_name)
                st.success(f"Project: {project_name} for Client: {selected_client_name} successfully deleted.")

if selected == "Edit":
    edit()

if selected == "Archive":
    archive()

if selected == "Delete":
    delete()
