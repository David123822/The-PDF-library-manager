import sqlite3
from tkinter import *
import subprocess  # Importing subprocess module for running external applications
from add import *
from search import *
from view import *


with sqlite3.connect("data.db") as db:
    cursor = db.cursor()

window = Tk()
window.title("Library manager")
window.geometry("300x400")

icon = PhotoImage(file= "4.ppm")
window.iconphoto(True, icon)

Button(window, text= "Add books", command= add_to_database).place(x= 105,y = 150)
Button(window, text= "Search for books", command= search_the_database).place(x= 80,y = 185)
Button(window, text= "View all books", command= view_all_data).place(x= 90,y = 220)
Button(window, text= "Exit", command= window.destroy, background= "red", foreground= "white").place(x= 125,y = 255)

window.mainloop()