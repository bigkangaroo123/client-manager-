import tkinter as tk

#window = tk.Tk() #literally just a black window
#window.title("Page name goes here")
#window.geometry('1920x1080')#the res
#window.configure(bg='#555555') #background

#label = tk.Label(window, text="Login")
#3 geometry manager: pack, place, grid
#label.pack()#placeing the 'label' widget
#label.grid(row=0, column=0) #diving screen - think of this as coordinates 0,0 is at top left

#window.mainloop()  #a loop thta'll run continuously. closing app means mainloop will stop executing
#this is also a blocking function anything after mainloop() can run


#Creating an actual applicationL
window = tk.Tk()
window.title("The Beginning of Greatness")
window.geometry('1920x1080')

#Creating labels - the widgets
login = tk.Label(window, text="Login")
username = tk.Label(window, text="Username")
u_input = tk.Entry(window) #entry function allows user input
password = tk.Label(window, text="Password")
p_input = tk.Entry(window, show="*")#called "show stars" astericks when entering password
login_button = tk.Button(window, text = "Login") #a user clickable button

#Placing all the labels - the widgets
login.grid(row=0, column=0, columnspan=2)#columnspan lets a widget span more than one column
username.grid(row=1, column=0)
u_input.grid(row=1, column=1)
password.grid(row=2, column=0)
p_input.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan=2)

window.mainloop() 
