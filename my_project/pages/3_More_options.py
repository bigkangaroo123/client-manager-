import streamlit as st
from streamlit_option_menu import option_menu
import client_management_db

# Option menu for More Options
selected = option_menu(
    menu_title="More Options",
    options=["✏️Edit", "📦Archive", "🗑️Delete"],
    orientation="horizontal",
)

# ---------- editing -------------
def edit(): 
    if not client_management_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")
    else:
        client_names = [client['client_name'] for client in client_management_db.get_all_clients()]
        selected_client_name = st.selectbox("Select a client to edit", client_names)

        selected_client = client_management_db.get_client_by_name(selected_client_name)

        if selected_client:
            st.subheader(f"Editing Client: {selected_client_name}")

            new_client_name = st.text_input("Edit client name:", value=selected_client['client_name'])
            new_billing_rate = st.text_input("Edit hourly billing rate:", value=str(selected_client['rate']))

            if st.button("Save Changes to Client"):
                if new_billing_rate:
                    try:
                        new_billing_rate = int(new_billing_rate)
                        if new_billing_rate > 0:
                            client_management_db.update_client_db(selected_client['id'], new_client_name, new_billing_rate)
                            st.success("Client details updated successfully!")
                        else:
                            st.error("Please enter a positive integer for the billing rate.")
                    except ValueError:
                        st.error("Please enter a valid integer for the billing rate.")

                else:
                    client_management_db.update_client_db(selected_client['id'], new_client_name, new_billing_rate)
                
            st.subheader(f"Projects for {selected_client_name}")
            projects = client_management_db.get_all_projects(selected_client['id'])

            if not projects:
                st.write("No projects available for this client.")
            else:
                project_names = [project['project_name'] for project in projects]
                project_name = st.selectbox("Select a project to edit", project_names)

                new_project_name = st.text_input("Edit project name:", value=project_name)

                if st.button(f"Save Changes to Project '{project_name}'"):
                    if new_project_name and new_project_name != project_name:
                        project_id = next(project['id'] for project in projects if project['project_name'] == project_name)
                        client_management_db.update_project_db(project_id, new_project_name)
                        st.success(f"Project name updated to '{new_project_name}'!")
                    else:
                        st.error("Please enter a valid and different project name.")

# ---------- archiving / unarchiving -------------
def archive():
    if not client_management_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")

    st.subheader("Archive / Unarchive Options")

    action_type = st.radio("What would you like to do?", ("Archive", "Unarchive"))

    if action_type == "Archive":
        archive_type = st.radio("What would you like to archive?", ("Client", "Project"))

        if archive_type == "Client":
            client_names = [client['client_name'] for client in client_management_db.get_all_clients()]
            selected_client_name = st.selectbox("Select a client to archive", client_names)

            if selected_client_name:
                selected_client = client_management_db.get_client_by_name(selected_client_name)
                if selected_client:
                    if st.button(f"Archive Client '{selected_client_name}'"):
                        client_management_db.archive_client(selected_client['id'])
                        st.success(f"Client '{selected_client_name}' has been archived!")

        elif archive_type == "Project":
            client_names = [client['client_name'] for client in client_management_db.get_all_clients()]
            selected_client_name = st.selectbox("Select a client", client_names)

            selected_client = client_management_db.get_client_by_name(selected_client_name)

            if selected_client:
                projects = client_management_db.get_all_projects(selected_client['id'])
                if not projects:
                    st.write("No projects available for this client.")
                else:
                    project_names = [project['project_name'] for project in projects]
                    project_name = st.selectbox("Select a project to archive", project_names)

                    if st.button(f"Archive Project '{project_name}'"):
                        project_id = next(project['id'] for project in projects if project['project_name'] == project_name)
                        client_management_db.archive_project(selected_client['id'], project_id)
                        st.success(f"Project '{project_name}' has been archived!")

    elif action_type == "Unarchive":
        unarchive_type = st.radio("What would you like to unarchive?", ("Client", "Project"))

        if unarchive_type == "Client":
            archived_clients = client_management_db.get_all_clients()
            archived_client_names = [client['client_name'] for client in archived_clients if client['status'] == 'archived']
            if not archived_client_names:
                st.warning("No archived clients.")
            else:
                selected_client_name = st.selectbox("Select a client to unarchive", archived_client_names)

                if selected_client_name:
                    if st.button(f"Unarchive Client '{selected_client_name}'"):
                        selected_client = client_management_db.get_client_by_name(selected_client_name)
                        if selected_client:
                            client_management_db.unarchive_client(selected_client['id'])
                            st.success(f"Client '{selected_client_name}' has been unarchived!")

        elif unarchive_type == "Project":
            archived_projects = client_management_db.get_all_archived_projects()
            if not archived_projects:
                st.warning("No archived projects.")
            else:
                archived_project_names = [(client['client_name'], project['project_name']) for client in archived_projects for project in client['projects']]
                selected_client_name, selected_project_name = st.selectbox(
                    "Select a project to unarchive", archived_project_names, format_func=lambda x: f"{x[0]} - {x[1]}"
                )

                if selected_client_name and selected_project_name:
                    selected_client = client_management_db.get_client_by_name(selected_client_name)
                    if st.button(f"Unarchive Project '{selected_project_name}'"):
                        selected_client = client_management_db.get_client_by_name(selected_client_name)
                        selected_project = next(project for project in client_management_db.get_all_projects(selected_client['id']) if project['project_name'] == selected_project_name)
                        client_management_db.unarchive_project(selected_client['id'], selected_project['id'])
                        st.success(f"Project '{selected_project_name}' has been unarchived!")

# ---------- deleting -------------
def delete():
    if not client_management_db.get_all_clients():
        st.warning("No clients or projects available. Add some first!")
        return  # Stop execution if no clients are present

    action_type = st.radio("What would you like to delete?", ("Client", "Project"))

    # Deleting a Client
    if action_type == "Client":
        client_names = [client['client_name'] for client in client_management_db.get_all_clients()]
        if not client_names:
            st.warning("No clients available to delete.")
            return

        selected_client_name = st.selectbox("Select a client to delete", client_names)

        if st.button("Delete Client"):
            confirm_delete = st.checkbox(f"Are you sure you want to delete client '{selected_client_name}'?", value=False)
            if confirm_delete:
                selected_client = client_management_db.get_client_by_name(selected_client_name)
                client_management_db.delete_client_db(selected_client['id'])
                st.success(f"Client '{selected_client_name}' has been deleted!")
                st.experimental_rerun()

    # Deleting a Project
    elif action_type == "Project":
        client_names = [client['client_name'] for client in client_management_db.get_all_clients()]
        if not client_names:
            st.warning("No clients available to delete projects from.")
            return

        selected_client_name = st.selectbox("Select a client", client_names)

        # Get selected client's projects
        selected_client = client_management_db.get_client_by_name(selected_client_name)
        projects = client_management_db.get_all_projects(selected_client['id'])

        if not projects:
            st.warning(f"No projects found for client '{selected_client_name}'.")
            return

        project_names = [project['project_name'] for project in projects]
        selected_project_name = st.selectbox("Select a project to delete", project_names)

        if st.button("Delete Project"):
            confirm_delete = st.checkbox(f"Are you sure you want to delete project '{selected_project_name}'?", value=False)
            if confirm_delete:
                project_id = next((project['id'] for project in projects if project['project_name'] == selected_project_name), None)
                client_management_db.delete_project_db(selected_client['id'], project_id)
                st.success(f"Project '{selected_project_name}' has been deleted!")
                st.rerun()

# Call the appropriate function based on the selected option
if selected == "✏️Edit":
    edit()

if selected == "📦Archive":
    archive()

if selected == "🗑️Delete":
    delete()