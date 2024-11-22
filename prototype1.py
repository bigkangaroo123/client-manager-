import tkinter as tk
from tkinter import messagebox as mb

window = tk.Tk()
window.geometry('640x740')
window.title("EasyManage")
window.configure(bg='white')

clients = []

def open_client_portal(client_name):
    client_portal = tk.Toplevel(window)
    client_portal.geometry('400x400')
    client_portal.title(f"Portal for {client_name}")
    client_portal.configure(bg='white')

    portal_label = tk.Label(client_portal, text=f"Welcome to the portal for {client_name}", bg='white', fg="black", font=("Arial", 16))
    portal_label.pack(pady=20)

    portal_details = tk.Label(client_portal, text=f"Details about {client_name} can be displayed here.", bg='white', fg="black", font=("Arial", 12))
    portal_details.pack(pady=10)

def update_client_buttons():
    for widget in client_frame.winfo_children():
        widget.destroy()

    for client in clients:
        button = tk.Button(client_frame, text=client, bg='white', fg="black", font=("Arial", 10), 
                           command=lambda c=client: open_client_portal(c))
        button.pack(pady=5)

def final_add(c_input):
    if not c_input.get():
        mb.showinfo(title="Add Client", message="Please enter a client name before adding")
    else:
        mb.showinfo(title="Add Client", message=f"Successfully added the client {c_input.get()}")

def add_client():
    add_client_window = tk.Toplevel(window) #just creates a new window inside the main window "window"
    add_client_window.geometry('400x540')
    add_client_window.title("Add Client")
    add_client_window.configure(bg='white')

    enter_label = tk.Label(add_client_window, text="Enter client name", bg='white', fg="black", font=("Arial", 10))
    c_input = tk.Entry(add_client_window, font=("Arial", 10), bg='white', fg='black')
    add_button = tk.Button(add_client_window, text="Add Client", bg='white', fg="black", font=("Arial",10), command=lambda:final_add(c_input))

    enter_label.grid(row=0, column=0)
    c_input.grid(row=0, column=1)
    add_button.grid(row=1, column=1)

frame = tk.Frame(bg='white')

#Creating widgets
welcome_label = tk.Label(frame, text="Welcome!", bg='white', fg="black", font=("Arial",30))
add_client_button = tk.Button(frame, text="Add Client", bg='white', fg="black", font=("Arial",10), command=add_client)

#Packing widgets
welcome_label.grid(row=0, column=0, pady=25)
add_client_button.grid(row=1, column=0)

frame.pack()

window.mainloop()
