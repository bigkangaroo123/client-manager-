import streamlit as st
from streamlit_option_menu import option_menu
import client_manager_db
client_manager_db.init_db()

# Option menu for More Options
selected = option_menu(
    menu_title="More Options",
    options=["✏️Edit", "📦Archive", "🗑️Delete"],
    orientation="horizontal",
)

# ---------- editing -------------
def edit(): 
    if 'clients' not in client_manager_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")
    else:
        client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to edit", client_names)

        selected_client = None
        for client in client_manager_db.get_all_clients():
            if client['client_name'] == selected_client_name:
                selected_client = client
                break

        if selected_client:
            st.subheader(f"Editing Client: {selected_client_name}")

            new_client_name = st.text_input("Edit client name:", value=selected_client['client_name'])
            new_billing_rate = st.text_input("Edit hourly billing rate:", value=str(selected_client['rate']))

            if st.button("Save Changes to Client"):
                try:
                    new_billing_rate = int(new_billing_rate)
                    if new_billing_rate > 0:
                        client_manager_db.update_client_db(selected_client['id'], new_client_name, new_billing_rate)
                        st.success("Client details updated successfully!")
                    else:
                        st.error("Please enter a positive integer for the billing rate.")
                except ValueError:
                    st.error("Please enter a valid integer for the billing rate.")

            st.subheader(f"Projects for {selected_client_name}")
            if "projects" not in selected_client or not selected_client['projects']: #get projects
                st.write("No projects available for this client.")
            else:
                project_name = st.selectbox("Select a project to edit", selected_client["projects"])
                new_project_name = st.text_input("Edit project name:", value=project_name)

                if st.button(f"Save Changes to Project '{project_name}'"):
                    if new_project_name and new_project_name != project_name:
                        client_manager_db.update_project_db(selected_client['id'], project_name, new_project_name)
                        st.success(f"Project name updated to '{new_project_name}'!")
                    else:
                        st.error("Please enter a valid and different project name.")

# ---------- archiving / unarchiving -------------
def archive():
    if 'clients' not in client_manager_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")

    st.subheader("Archive / Unarchive Options")

    action_type = st.radio("What would you like to do?", ("Archive", "Unarchive"))

    if action_type == "Archive":
        archive_type = st.radio("What would you like to archive?", ("Client", "Project"))

        if archive_type == "Client":
            client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
            selected_client_name = st.selectbox("Select a client to archive", client_names)

            if selected_client_name:
                selected_client = None
                for client in client_manager_db.get_all_clients():
                    if client['client_name'] == selected_client_name:
                        selected_client = client
                        break
                if selected_client:
                    if st.button(f"Archive Client '{selected_client_name}'"):
                        client_manager_db.archive_client(selected_client['id'])
                        st.success(f"Client '{selected_client_name}' has been archived!")

        elif archive_type == "Project":
            client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
            selected_client_name = st.selectbox("Select a client", client_names)

            selected_client = None
            if selected_client_name != "All Clients":
                for client in client_manager_db.get_all_clients():
                    if client['client_name'] == selected_client_name:
                        selected_client = client
                        break

            if selected_client and "projects" in selected_client and selected_client["projects"]:
                project_name = st.selectbox("Select a project to archive", selected_client["projects"])

                if st.button(f"Archive Project '{project_name}'"):
                    project_id = None
                    for project in selected_client["projects"]:
                        if project['client_name'] == project_name:
                            project_id = project['id']
                            break
                    if project_id:
                        client_manager_db.archive_project(selected_client['id'], project_id)
                        st.success(f"Project '{project_name}' has been archived!")

            else:
                st.warning("No projects available for the selected client.")

    elif action_type == "Unarchive":
        unarchive_type = st.radio("What would you like to unarchive?", ("Client", "Project"))

        if unarchive_type == "Client":
            archived_clients = client_manager_db.get_all_clients(status='archived')
            if not archived_clients:
                st.warning("No archived clients.")
            else:
                archived_client_names = [client['client_name'] for client in archived_clients]
                selected_client_name = st.selectbox("Select a client to unarchive", archived_client_names)

                if selected_client_name:
                    if st.button(f"Unarchive Client '{selected_client_name}'"):
                        selected_client = None
                        for client in archived_clients:
                            if client['client_name'] == selected_client_name:
                                selected_client = client
                                break
                        if selected_client:
                            client_manager_db.unarchive_client(selected_client['id'])
                            st.success(f"Client '{selected_client_name}' has been unarchived!")

        elif unarchive_type == "Project":
            archived_projects = client_manager_db.get_all_archived_projects()
            if not archived_projects:
                st.warning("No archived projects.")
            else:
                archived_project_names = [(client['client_name'], project['project_name']) for client in archived_projects for project in client['projects']]
                selected_client_name, selected_project_name = st.selectbox(
                    "Select a project to unarchive", archived_project_names, format_func=lambda x: f"{x[0]} - {x[1]}"
                )
                #the format_func just makes the projects look like:" client - project " in the dropdown

                if selected_client_name and selected_project_name:
                    if st.button(f"Unarchive Project '{selected_project_name}'"):
                        selected_client = None
                        for client in archived_projects:
                            if client['client_name'] == selected_client_name:
                                selected_client = client
                                break
                        if selected_client:
                            selected_project = None
                            for project in selected_client["projects"]:
                                if project['client_name'] == selected_project_name:
                                    selected_project = project
                                    break
                            if selected_project:
                                client_manager_db.unarchive_project(selected_client['id'], selected_project['id'])
                                st.success(f"Project '{selected_project_name}' has been unarchived!")

# ---------- deleting -------------
def delete():
    if 'clients' not in client_manager_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")

    action_type = st.radio("What would you like to delete?", ("Client", "Project"))

    if action_type == "Client":
        client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to delete", client_names)

        if selected_client_name:
            if st.button("Delete Client"):
                st.warning("Are you sure you want to permanently delete this client?")
                confirm_delete = st.radio("Choose an option: ", ("No", "Yes"))

                if confirm_delete == "Yes":
                    selected_client = None
                    for client in client_manager_db.get_all_clients():
                        if client['name'] == selected_client_name:
                            selected_client = client
                            break
                    client_manager_db.delete_client_db(selected_client['id'])
                    st.success(f"Client {selected_client_name} has been deleted!")

                elif confirm_delete == "No":
                    st.success(f"Client deletion cancelled!")

    elif action_type == "Project":
        client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to delete", client_names)

        selected_client = None
        if selected_client_name != "All Clients":
            for client in client_manager_db.get_all_clients():
                if client['client_name'] == selected_client_name:
                    selected_client = client
                    break

        if selected_client and "projects" in selected_client and selected_client["projects"]:
            project_name = st.selectbox("Select a project to delete", selected_client["projects"])

            if st.button("Delete Project"):
                project_id = None
                for project in selected_client["projects"]:
                    if project['project_name'] == project_name:
                        project_id = project['id']
                        break
                if project_id:
                    client_manager_db.delete_project_db(selected_client['id'], project_id)
                    st.success(f"Project '{project_name}' has been deleted!")

if selected == "✏️Edit":
    edit()

if selected == "📦Archive":
    archive()

if selected == "🗑️Delete":
    delete()