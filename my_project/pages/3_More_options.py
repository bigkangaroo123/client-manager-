import streamlit as st
from streamlit_option_menu import option_menu


selected = option_menu(
        menu_title="More Options",
        options=["Edit", "Archive", "Delete"],
        orientation="horizontal",
)
def edit(): #editing a client
    if 'clients' not in st.session_state or not st.session_state.clients:
        st.warning("No clients or projects available. Add some first!")

    else:
        client_names = []
        for client in st.session_state.clients:
            client_names.append(client['name'])
        
        selected_client_name = st.selectbox("Select a client to edit", client_names)

        selected_client = None
        for client in st.session_state.clients:
            if client["name"] == selected_client_name:
                selected_client = client
                break

        if selected_client:
            st.subheader(f"Editing Client: {selected_client_name}")

            new_client_name = st.text_input("Edit client name:", value=selected_client["name"])
            new_billing_rate = st.text_input("Edit hourly billing rate:", value=str(selected_client["rate"]))

            if st.button("Save Changes to Client"):
                try:
                    new_billing_rate = int(new_billing_rate)
                    if new_billing_rate > 0:
                        selected_client["name"] = new_client_name
                        selected_client["rate"] = new_billing_rate
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


if selected == "Edit":
    edit()

def archive():
    if 'clients' not in st.session_state or not st.session_state.clients:
        st.warning("No clients or projects available. Add some first!")

if selected == "Archive":
    archive()
