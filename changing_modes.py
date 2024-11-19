import tkinter as tk

def modes():
    # Check current background color to toggle between modes
    if window.cget("bg") == "white":  # If the current mode is light mode
        window.config(bg="black")  # Set the background to dark
        frame.config(bg="black")  # Set frame background to dark
        mode_button.config(bg="grey", fg="white")  # Change button colors
        mode_button.config(text="Switch to Light Mode")  # Update button text
    else:  # If the current mode is dark mode
        window.config(bg="white")  # Set the background to light
        frame.config(bg="white")  # Set frame background to light
        mode_button.config(bg="light grey", fg="black")  # Change button colors
        mode_button.config(text="Switch to Dark Mode")
    

window = tk.Tk()
window.title("EasyManage")
window.geometry('540x640')
window.config(bg='white')

frame = tk.Frame(window, bg="white")
frame.pack(fill="both", expand=True)

mode_button = tk.Button(frame, text="Switch to Dark Mode", command=modes, bg="light grey")
mode_button.pack(pady=20)

window.config(bg="white")
frame.config(bg="white")

window.mainloop()
