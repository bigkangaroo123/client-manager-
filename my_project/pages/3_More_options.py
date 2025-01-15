import streamlit as st
from streamlit_option_menu import option_menu
import client_manager_db

# Option menu for More Options
selected = option_menu(
    menu_title="More Options",
    options=["✏️Edit", "📦Archive", "🗑️Delete"],
    orientation="horizontal",
)

# ---------- editing -------------
def edit(): 
    if not client_manager_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")
    else:
        client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to edit", client_names)

        selected_client = client_manager_db.get_client_by_name(selected_client_name)

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
            projects = client_manager_db.get_all_projects(selected_client['id'])

            if not projects:
                st.write("No projects available for this client.")
            else:
                project_names = [project['project_name'] for project in projects]
                project_name = st.selectbox("Select a project to edit", project_names)

                new_project_name = st.text_input("Edit project name:", value=project_name)

                if st.button(f"Save Changes to Project '{project_name}'"):
                    if new_project_name and new_project_name != project_name:
                        project_id = next(project['id'] for project in projects if project['project_name'] == project_name)
                        client_manager_db.update_project_db(project_id, new_project_name)
                        st.success(f"Project name updated to '{new_project_name}'!")
                    else:
                        st.error("Please enter a valid and different project name.")

# ---------- archiving / unarchiving -------------
def archive():
    if not client_manager_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")

    st.subheader("Archive / Unarchive Options")

    action_type = st.radio("What would you like to do?", ("Archive", "Unarchive"))

    if action_type == "Archive":
        archive_type = st.radio("What would you like to archive?", ("Client", "Project"))

        if archive_type == "Client":
            client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
            selected_client_name = st.selectbox("Select a client to archive", client_names)

            if selected_client_name:
                selected_client = client_manager_db.get_client_by_name(selected_client_name)
                if selected_client:
                    if st.button(f"Archive Client '{selected_client_name}'"):
                        client_manager_db.archive_client(selected_client['id'])
                        st.success(f"Client '{selected_client_name}' has been archived!")

        elif archive_type == "Project":
            client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
            selected_client_name = st.selectbox("Select a client", client_names)

            selected_client = client_manager_db.get_client_by_name(selected_client_name)

            if selected_client:
                projects = client_manager_db.get_all_projects(selected_client['id'])
                if not projects:
                    st.write("No projects available for this client.")
                else:
                    project_names = [project['project_name'] for project in projects]
                    project_name = st.selectbox("Select a project to archive", project_names)

                    if st.button(f"Archive Project '{project_name}'"):
                        project_id = next(project['id'] for project in projects if project['project_name'] == project_name)
                        client_manager_db.archive_project(selected_client['id'], project_id)
                        st.success(f"Project '{project_name}' has been archived!")

    elif action_type == "Unarchive":
        unarchive_type = st.radio("What would you like to unarchive?", ("Client", "Project"))

        if unarchive_type == "Client":
            archived_clients = client_manager_db.get_all_clients()
            archived_client_names = [client['client_name'] for client in archived_clients if client['status'] == 'archived']
            if not archived_client_names:
                st.warning("No archived clients.")
            else:
                selected_client_name = st.selectbox("Select a client to unarchive", archived_client_names)

                if selected_client_name:
                    if st.button(f"Unarchive Client '{selected_client_name}'"):
                        selected_client = client_manager_db.get_client_by_name(selected_client_name)
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

                if selected_client_name and selected_project_name:
                    selected_client = client_manager_db.get_client_by_name(selected_client_name)
                    if st.button(f"Unarchive Project '{selected_project_name}'"):
                        selected_client = client_manager_db.get_client_by_name(selected_client_name)
                        selected_project = next(project for project in client_manager_db.get_all_projects(selected_client['id']) if project['project_name'] == selected_project_name)
                        client_manager_db.unarchive_project(selected_client['id'], selected_project['id'])
                        st.success(f"Project '{selected_project_name}' has been unarchived!")

# ---------- deleting -------------
def delete():
    if not client_manager_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")

    action_type = st.radio("What would you like to delete?", ("Client", "Project"))

    if action_type == "Client":
        client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to delete", client_names)

        if selected_client_name:
            # Confirm Deletion Button
            if st.button("Delete Client"):
                # Ask for confirmation
                st.warning(f"Are you sure you want to permanently delete the client {selected_client_name}?")

                # Create a confirmation state to manage flow
                if "confirm_delete" not in st.session_state:
                    st.session_state.confirm_delete = False

                # Buttons to confirm the action
                if not st.session_state.confirm_delete:
                    yes_button = st.button("Yes, Delete", key="yes")
                    no_button = st.button("No, Cancel", key="no")

                    if yes_button:
                        # Set the session state to confirm deletion
                        st.session_state.confirm_delete = True
                        selected_client = client_manager_db.get_client_by_name(selected_client_name)
                        client_manager_db.delete_client_db(selected_client['id'])
                        st.success(f"Client {selected_client_name} permanently deleted!")
                    elif no_button:
                        st.success("Client deletion cancelled.")
                else:
                    # Confirmation state is set, so confirm and show action result
                    st.success(f"Client {selected_client_name} permanently deleted!")


    elif action_type == "Project":
        client_names = [client['client_name'] for client in client_manager_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to delete", client_names)

        selected_client = client_manager_db.get_client_by_name(selected_client_name)

        if selected_client and "projects" in selected_client:
            project_names = [project['project_name'] for project in client_manager_db.get_all_projects(selected_client['id'])]
            project_name = st.selectbox("Select a project to delete", project_names)

            if st.button("Delete Project"):
                project_id = next(project['id'] for project in client_manager_db.get_all_projects(selected_client['id']) if project['project_name'] == project_name)

                client_manager_db.delete_project_db(selected_client['id'], project_id)
                st.success(f"Project '{project_name}' has been deleted!")

# Call the appropriate function based on the selected option
if selected == "✏️Edit":
    edit()

if selected == "📦Archive":
    archive()

if selected == "🗑️Delete":
    delete()