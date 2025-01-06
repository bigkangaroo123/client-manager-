import streamlit as st

st.title("📂 Your Clients:")
#-------------- task table -----------------
# 1st column: task name
# 2nd: deadline
# 3rd: checkbox
# 4th: notes
 
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def add_task():
    task = {
        'task_name' : '',
        'deadline' : None,
        'complete' : False, 
        'notes' : ''
    }
    st.session_state.tasks.append(task)

def task_table(client_name, project_name):
    st.subheader(f"📋 Task Table for {project_name} under {client_name}")

    if st.button("Add Task"):
        add_task()

    if st.session_state.tasks:
        for i, task in enumerate(st.session_state.tasks):
            columns = st.columns([3, 3, 2, 3])

            #the 4 columns:
            task['task_name'] = columns[0].text_input("Task Name", value=task['task_name'], key=f"task_name_{i}")

            task['deadline'] = columns[1].date_input("Deadline", value=task['deadline'], key=f"deadline_task_{i}")

            task['complete'] = columns[2].checkbox("Done", value=task['complete'], key=f"status_task_{i}")

            task['notes'] = columns[3].text_input("Notes", value=task['notes'], key=f"notes_task_{i}")

#-------------- main viewing manu ----------------
selected_client = None

if 'clients' not in st.session_state or not st.session_state.clients:
    st.warning("No clients available. Add some clients first!")
else:
    client_names = []
    for client in st.session_state.clients:
        client_names.append(client['name'])

    selected_client_name = st.selectbox("Select a client", ["All Clients"] + client_names)

    if selected_client_name != "All Clients":
        for client in st.session_state.clients:
            if client['name'] == selected_client_name:
                selected_client = client
                break
        
        st.subheader(f"Client: {selected_client['name']}")
        st.write(f"Hourly Rate: ${selected_client['rate']}/hour")

        if 'projects' not in selected_client or not selected_client['projects']:
            st.info(f"No projects found for {selected_client_name}.")
        else:
            selected_project = st.selectbox(
                f"Projects for {selected_client['name']}", ["All Projects"] + selected_client['projects'])

            if selected_project != "All Projects": #when a project is selected, display its task table
                task_table(selected_client['name'], selected_project)
            else:
                st.write(f"Projects under {selected_client['name']}:")
                st.write(", ".join(selected_client['projects']))
    else:
        st.subheader("All Clients and Their Projects")
        for client in st.session_state.clients:
            st.write(f"**{client['name']}** (Rate: ${client['rate']}/hour)")
            if 'projects' in client and client['projects']:
                st.write(f"Projects: {', '.join(client['projects'])}")
            else:
                st.write("This client has no projects added.")
