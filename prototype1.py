import tkinter as tk
from tkinter import messagebox as mb

window = tk.Tk()
window.geometry('640x740')
window.title("EasyManage")
window.configure(bg='white')

def final_add(c_input):
    if not c_input.get():
        mb.showinfo(title="Add Client", message="Please enter a client name before adding")
    else:
        mb.showinfo(title="Add Client", message=f"Successfully added the client {c_input.get()}")

def add_client():
    client_window = tk.Toplevel(window) #just creates a new window inside the main window "window"
    client_window.geometry('400x540')
    client_window.title("Add Client")
    client_window.configure(bg='white')

    enter_label = tk.Label(client_window, text="Enter client name", bg='white', fg="black", font=("Arial", 10))
    c_input = tk.Entry(client_window, font=("Arial", 10), bg='white', fg='black')
    add_button = tk.Button(client_window, text="Add Client", bg='white', fg="black", font=("Arial",10), command=lambda:final_add(c_input))

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
