import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk

# Initialize main window
window = tk.Tk()
window.geometry('640x740')
window.title("EasyManage")
window.configure(bg='white')

clients = []

def update_client_buttons():
    for widget in client_frame.winfo_children():
        widget.destroy() 

    for client in clients:
        button = tk.Button(client_frame, text=client, bg='white', fg="black", font=("Arial", 10), 
                           command=lambda c=client: open_client_portal(c))
        button.pack(pady=5)

def final_add(c_input):
    client_name = c_input.get().strip() 
    if not client_name:
        mb.showinfo(title="Add Client", message="Please enter a client name before adding")
    else:
        clients.append(client_name) 
        update_client_buttons()
        mb.showinfo(title="Add Client", message=f"Successfully added the client '{client_name}'")

def add_client():
    add_client_window = tk.Toplevel(window)
    add_client_window.geometry('400x200')
    add_client_window.title("Add Client")
    add_client_window.configure(bg='white')

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (200 // 2)
    add_client_window.geometry(f'400x200+{x}+{y}')

    enter_label = tk.Label(add_client_window, text="Enter client name", bg='white', fg="black", font=("Arial", 10))
    c_input = tk.Entry(add_client_window, font=("Arial", 10), bg='white', fg='black')
    add_button = tk.Button(add_client_window, text="Add Client", bg='white', fg="black", font=("Arial", 10), command=lambda: final_add(c_input))

    enter_label.grid(row=0, column=0, pady=10, padx=10)
    c_input.grid(row=0, column=1, pady=10, padx=10)
    add_button.grid(row=1, column=1, pady=10)

def open_client_portal(client_name):
    client_portal = tk.Toplevel(window)
    client_portal.geometry('400x400')
    client_portal.title(client_name)
    client_portal.configure(bg='white')

    portal_label = tk.Label(client_portal, text=f"Welcome to the portal for {client_name}", bg='white', fg="black", font=("Arial", 16))
    portal_label.pack(pady=20)

    portal_details = tk.Label(client_portal, text=f"LESS GOOO", bg='white', fg="black", font=("Arial", 12))
    portal_details.pack(pady=10)

    '''
    UN DOCUMENT THIS AFTER WRITING CODE FOR ADDING PROJECT
    table_frame = tk.Frame(client_portal, bg='white')
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    task_table = ttk.Treeview(client_portal)
    #defining columns:
    task_table['columns'] = ("Task Name", "Due Date", "Date of Completion")

    task_table.column("#0", width=120, minwidth=25) #this is a phantom column (have to have this)
    task_table.column("Task Name", anchor=tk.W, width=120)
    task_table.column("Due Date", anchor=tk.CENTER, width=80)
    task_table.column("Date of Completion", anchor=tk.CENTER, width=120)
    '''


frame = tk.Frame(bg='white')

welcome_label = tk.Label(frame, text="Welcome!", bg='white', fg="black", font=("Arial", 30))
add_client_button = tk.Button(frame, text="Add Client", bg='white', fg="black", font=("Arial", 10), command=add_client)

welcome_label.grid(row=0, column=0, pady=25)
add_client_button.grid(row=1, column=0)

frame.pack()

client_frame = tk.Frame(window, bg='white')
client_frame.pack(pady=20)

window.mainloop()