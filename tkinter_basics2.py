import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("The Beginning of Greatness")
window.geometry('640x740')
window.configure(bg='#0000FF')

#frame is a container - u put everything inside it - s smaller box within a larger box (the window)
frame = tk.Frame(bg='#0000FF')


def login():
    username = "eeeman"
    password = "eeepassword.py"
    if u_input.get() == username and p_input.get() == password:
        messagebox.showinfo(title="LESS GO", message="you successfully logged in") #unlike a print statement, this actually opens a diff window showing the title and message
    else:
        messagebox.showinfo(title="NAH BRUH", message="you successfully didnt log in") #messageboxes are essentially our print statements

#Creating labels - the widgets
login_label = tk.Label(frame, text="Login", bg='#0000FF', fg="#FFA500", font=("Showcard Gothic", 30)) #bbg to match w/ background (text box colour), fg to adjust text colour
username = tk.Label(frame, text="Username", bg='#0000FF', fg="#FFA500", font=("Showcard Gothic", 15))
u_input = tk.Entry(frame, font=("Showcard Gothic", 15), fg="#0000FF") #entry function allows user input
password = tk.Label(frame, text="Password", bg='#0000FF', fg="#FFA500", font=("Showcard Gothic", 15))
p_input = tk.Entry(frame, show="*", font=("Showcard Gothic", 15), fg="#0000FF")#called "show stars" astericks when entering password
login_button = tk.Button(frame, text = "Login", bg='#FFA500', fg="#0000FF", font=("Showcard Gothic", 15), command=login) #calls the login function 

#Placing all the labels - the widgets
                                        #sticky: pls take up space in all 4 directions - north east west south (N E W S)
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=25)#columnspan lets a widget span more than one column 
username.grid(row=1, column=0, pady=10)                          #pad"y" adds space on y axis (padx adds on x axis)
u_input.grid(row=1, column=1)
password.grid(row=2, column=0, pady=10)
p_input.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan=2)

frame.pack()#frame actually resizes the widgets and centers it

window.mainloop() 
