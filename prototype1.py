import customtkinter as ctk
from tkinter import messagebox as mb 
from tkinter import ttk
from tkinter import *

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.geometry('640x740')
window.title("EasyManage")

clients = []

def update_client_buttons():
    for widget in client_frame.winfo_children():
        widget.destroy()

    for client in clients:
        button = ctk.CTkButton(client_frame, text=client, font=("Arial", 10),
                               command=lambda c=client: open_client_portal(c))
        button.pack(pady=5)

def final_add(c_input, add_client_window):
    client_name = c_input.get().strip()
    if not client_name:
        mb.showinfo(title="Add Client", message="Please enter a client name before adding")
    else:
        clients.append(client_name)
        mb.showinfo(title="Add Client", message=f"Successfully added the client '{client_name}'")
        update_client_buttons()
        add_client_window.destroy()

def add_client():
    add_client_window = ctk.CTkToplevel(window)
    add_client_window.geometry('400x200')
    add_client_window.title("Add Client")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (200 // 2)
    add_client_window.geometry(f'400x200+{x}+{y}')

    add_client_window.focus()
    add_client_window.grab_set()

    enter_label = ctk.CTkLabel(add_client_window, text="Enter client name", font=("Arial", 10))
    c_input = ctk.CTkEntry(add_client_window, font=("Arial", 10))
    add_button = ctk.CTkButton(add_client_window, text="Add Client", font=("Arial", 10), command=lambda: final_add(c_input, add_client_window))

    enter_label.grid(row=0, column=0, pady=10, padx=10)
    c_input.grid(row=0, column=1, pady=10, padx=10)
    add_button.grid(row=1, column=1, pady=10)

client_projects = {}

def final_add_project(p_input, add_project_window, client_name, project_frame):
    project_name = p_input.get().strip()
    if not project_name:
        mb.showinfo(title="Add Project", message="Please enter a project name before adding")
    elif project_name in client_projects.get(client_name, []):
        mb.showinfo(title="Add Project", message=f"The project '{project_name}' already exists.")
    else:
        if client_name not in client_projects:
            client_projects[client_name] = []
        client_projects[client_name].append(project_name)  # Ensure it is stored properly
        update_project_buttons(client_name, project_frame)  # Refresh the project buttons
        mb.showinfo(title="Add Project", message=f"Successfully added the project '{project_name}'")
        add_project_window.destroy()

def add_project(client_name, project_frame):
    add_project_window = ctk.CTkToplevel(window)
    add_project_window.geometry('400x200')
    add_project_window.title("Add Project")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (200 // 2)
    add_project_window.geometry(f'400x200+{x}+{y}')

    add_project_window.focus()
    add_project_window.grab_set()

    enter_label = ctk.CTkLabel(add_project_window, text="Enter project name", font=("Arial", 10))
    p_input = ctk.CTkEntry(add_project_window, font=("Arial", 10))
    add_button = ctk.CTkButton(
        add_project_window,
        text="Add Project",
        font=("Arial", 10),
        command=lambda: final_add_project(p_input, add_project_window, client_name, project_frame)
    )

    enter_label.grid(row=0, column=0, pady=10, padx=10)
    p_input.grid(row=0, column=1, pady=10, padx=10)
    add_button.grid(row=1, column=1, pady=10)


def update_project_buttons(client_name, project_frame):
    for widget in project_frame.winfo_children():
        widget.destroy()

  
    if client_name in client_projects:
        for project in client_projects[client_name]:
            if project not in client_projects:
                project_button = ctk.CTkButton(
                    project_frame,
                    text=project,
                    font=("Arial", 10),
                    command=lambda p=project: open_project_portal(p, client_name)
                )
                project_button.pack(pady=5)

def open_client_portal(client_name):
    client_portal = ctk.CTkToplevel(window)
    client_portal.geometry('400x400')
    client_portal.title(client_name)

    client_portal.focus()
    client_portal.grab_set()

    top_frame = ctk.CTkFrame(client_portal, fg_color="transparent")
    top_frame.pack(pady=20)  

    portal_label = ctk.CTkLabel(top_frame, text=f"{client_name}", font=("Arial", 16))
    portal_label.pack(pady=5) 

    add_project_button = ctk.CTkButton(top_frame, text="Add Project", font=("Arial", 10), 
                                       command=lambda: add_project(client_name, project_frame))
    add_project_button.pack(pady=5) 

    project_frame = ctk.CTkFrame(client_portal, fg_color="transparent")
    project_frame.pack(pady=10, fill="both", expand=True)

    update_project_buttons(client_name, project_frame)

def open_client_portal(client_name):
    client_portal = ctk.CTkToplevel(window)
    client_portal.geometry('400x400')
    client_portal.title(client_name)

    client_portal.focus()
    client_portal.grab_set()

    top_frame = ctk.CTkFrame(client_portal, fg_color="transparent")
    top_frame.pack(pady=20)  

    portal_label = ctk.CTkLabel(top_frame, text=f"{client_name}", font=("Arial", 16))
    portal_label.pack(pady=5) 

    add_project_button = ctk.CTkButton(top_frame, text="Add Project", font=("Arial", 10), 
                                       command=lambda: add_project(client_name, project_frame))
    add_project_button.pack(pady=5) 

    project_frame = ctk.CTkFrame(client_portal, fg_color="transparent")
    project_frame.pack(pady=10, fill="both", expand=True)

    update_project_buttons(client_name, project_frame)

def open_project_portal(project_name, client_name):
    project_portal = ctk.CTkToplevel(window)
    project_portal.geometry('600x400')
    project_portal.title(project_name)

    project_portal.focus()
    project_portal.grab_set()

    portal_label = ctk.CTkLabel(project_portal, text=f"Project {project_name} of {client_name}", font=("Arial", 16))
    portal_label.pack(pady=10)

    # Add task button
    add_task_button = ctk.CTkButton(
        project_portal,
        text="Add Task",
        font=("Arial", 10),
        command=lambda: add_task(project_portal, task_table, project_name)
    )
    add_task_button.pack(pady=10)

    task_table_frame = ctk.CTkFrame(project_portal)
    task_table_frame.pack(pady=10, fill="both", expand=True)

    task_table = ttk.Treeview(task_table_frame, columns=("Task", "Deadline", "Status", "Notes"), show="headings", height=10)
    task_table.pack(fill="both", expand=True)

    task_table.heading("Task", text="Task")
    task_table.heading("Deadline", text="Deadline")
    task_table.heading("Status", text="Status")
    task_table.heading("Notes", text="Notes")

    task_table.column("Task", anchor="w", width=150)
    task_table.column("Deadline", anchor="w", width=120)
    task_table.column("Status", anchor="center", width=80)
    task_table.column("Notes", anchor="w", width=200)

    # Populate table with existing tasks for the project (if any)
    if project_name in client_projects:
        for task in client_projects[project_name]:
            if task != project_name:  # Prevent the project name from being added as a task
                task_table.insert("", "end", values=(task, "No Deadline", "Incomplete", "No Notes"))


tasks = []

def finaladd_task(n_input, d_input, task_table, project_name, add_task_window):
    task_name = n_input.get().strip()
    deadline = d_input.get().strip()
    if not task_name or not deadline:
        mb.showinfo(title="Add Task", message="Please name the task and deadline before adding")
    else:
        if project_name not in client_projects:
            client_projects[project_name] = []
        client_projects[project_name].append(task_name)
        task_table.insert("", "end", values=(task_name, deadline, "Incomplete", "No Notes"))  # Add task to table
        mb.showinfo(title="Add Task", message=f"Successfully added the task '{task_name}'")
        add_task_window.destroy()

def add_task(project_portal, task_table, project_name):
    add_task_window = ctk.CTkToplevel(project_portal)
    add_task_window.geometry('400x200')
    add_task_window.title("Add Task")

    name_label = ctk.CTkLabel(add_task_window, text="Enter Task", font=("Arial", 16))
    dd_label = ctk.CTkLabel(add_task_window, text="Enter Deadline", font=("Arial", 16))
    n_input = ctk.CTkEntry(add_task_window, font=("Arial", 16))
    d_input = ctk.CTkEntry(add_task_window, font=("Arial", 16))

    finaladd_button = ctk.CTkButton(
        add_task_window,
        text="Add Task",
        font=("Arial", 10),
        command=lambda: finaladd_task(n_input, d_input, task_table, project_name, add_task_window)
    )

    name_label.grid(row=0, column=0, padx=10, pady=10)
    n_input.grid(row=0, column=1, padx=10, pady=10)
    dd_label.grid(row=1, column=0, padx=10, pady=10)
    d_input.grid(row=1, column=1, padx=10, pady=10)
    finaladd_button.grid(row=2, column=1, padx=10, pady=10)


frame = ctk.CTkFrame(window, fg_color="transparent")  
welcome_label = ctk.CTkLabel(frame, text="Welcome!", font=("Arial", 30))
add_client_button = ctk.CTkButton(frame, text="Add Client", font=("Arial", 10), command=add_client)

welcome_label.grid(row=0, column=0, pady=25)
add_client_button.grid(row=1, column=0)

frame.pack()

client_frame = ctk.CTkFrame(window, fg_color="transparent") 
client_frame.pack(pady=20)

window.mainloop()
