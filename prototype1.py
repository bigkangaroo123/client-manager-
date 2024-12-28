import customtkinter as ctk
from tkinter import messagebox as mb
from datetime import datetime

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
        update_client_buttons()
        mb.showinfo(title="Add Client", message=f"Successfully added the client '{client_name}'")
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
    else:
        if client_name not in client_projects:
            client_projects[client_name] = []
        client_projects[client_name].append(project_name)
        update_project_buttons(client_name, project_frame)
        mb.showinfo(title="Add Project", message=f"Successfully added the project '{project_name}'")
        add_project_window.destroy()

def add_project(client_name, project_frame):
    add_project_window = ctk.CTkToplevel(window)
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
    add_button = ctk.CTkButton(add_project_window, text="Add Project", font=("Arial", 10), 
                               command=lambda: final_add_project(p_input, add_project_window, client_name, project_frame))

    enter_label.grid(row=0, column=0, pady=10, padx=10)
    p_input.grid(row=0, column=1, pady=10, padx=10)
    add_button.grid(row=1, column=1, pady=10)

def update_project_buttons(client_name, project_frame):
    for widget in project_frame.winfo_children():
        widget.destroy()

    if client_name in client_projects:
        for project in client_projects[client_name]:
            project_button = ctk.CTkButton(project_frame, text=project, font=("Arial", 10), 
                                           command=lambda p=project: open_project_portal(p, client_name))
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

def open_project_portal(project_name, client_name):
    project_portal = ctk.CTkToplevel(window)
    project_portal.geometry('400x400')
    project_portal.title(project_name)

    project_portal.focus()
    project_portal.grab_set()

    portal_label = ctk.CTkLabel(project_portal, text=f"Project {project_name} of {client_name}", font=("Arial", 16))
    add_task_button = ctk.CTkButton(project_portal, text=f"+", font=("Arial", 16), command=lambda :add_task(project_portal, client_name))
#need help creating table in the project portal
    portal_label.pack(pady=20)
    add_task_button.pack(pady=5)

tasks = []

def add_task(project_portal, client_name):
    add_task_window = ctk.CTkToplevel(project_portal)
    add_task_window.geometry('400x200')
    add_task_window.title("Add Task")


frame = ctk.CTkFrame(window, fg_color="transparent")  
welcome_label = ctk.CTkLabel(frame, text="Welcome!", font=("Arial", 30))
add_client_button = ctk.CTkButton(frame, text="Add Client", font=("Arial", 10), command=add_client)

welcome_label.grid(row=0, column=0, pady=25)
add_client_button.grid(row=1, column=0)

frame.pack()

client_frame = ctk.CTkFrame(window, fg_color="transparent") 
client_frame.pack(pady=20)

window.mainloop()
