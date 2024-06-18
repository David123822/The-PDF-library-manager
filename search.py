import sqlite3
from tkinter import *
import subprocess  # Importing subprocess module for running external applications
from tkinter import ttk # need this for the Treeview widget

def search_the_database():  # the display
    global search, s_window, catVar, tagVar, tree, levVar

    s_window = Toplevel()
    s_window.title("Searching the database")
    s_window.geometry("600x500")

    Label(s_window, text= "Search").place(x=30, y= 30)

    search = Entry(s_window)
    search.place(x= 30, y= 60, width= 150, height= 30)

    Button(s_window, text= "Search", command= searching,bg= "light green", fg= "black").place(y= 60, x= 200)

    Button(s_window, text= "Add to favorite", command= add_favorite, bg= "orange", fg= "black").place(y= 60, x= 250)

    Button(s_window, text= "Exit", command= s_window.destroy, bg= "red", fg= "black").place(y= 60, x= 345)

    Button(s_window, text= "Reset", command= clearData).place(y= 60, x= 400)

# setting the available category meniu
    cat = set()

    cursor.execute("SELECT Categoria FROM pdf_files")

    for item in cursor.fetchall():
        cat.add(item[0]) # i make sure that each category only appears once

    catVar = StringVar(s_window)
    catVar.set("Choose a category")
    OptionMenu(s_window, catVar, *cat).place(x= 30, y= 100)

# setting the available tags meniu
# here i also have a list of lists and so i had to split them in individual elements

    utag = set()

    cursor.execute("SELECT status FROM pdf_files")

    tag_list= [item[0] for item in cursor.fetchall()]

    for item in tag_list:
        for elemant in item.split(", "):
            utag.add(elemant.strip())
    
    tagVar = StringVar(s_window)
    tagVar.set("Choose status")
    OptionMenu(s_window, tagVar, *utag).place(y= 100, x= 180)

# choosing the level

    levVar = StringVar(s_window)
    levVar.set("Choose level")

    levels = set()

    cursor.execute("SELECT level FROM pdf_files")
    for item in cursor.fetchall():
        levels.add(item[0])
    
    OptionMenu(s_window, levVar, *levels).place(y= 100, x= 310)
    

# the Treeview display widget

    tree = ttk.Treeview(s_window)
    tree["columns"] = ("File Path", "Category", "Level", "Tag", "Status")
    tree.column("#0", width=0, stretch=NO)  # Hide the first column
    tree.column("File Path", width=150)
    tree.column("Category", width=25)
    tree.column("Level", width=25)
    tree.column("Tag", width=150)
    tree.column("Status", width=30)

    tree.heading("File Path", text="File Path")
    tree.heading("Category", text="Category")
    tree.heading("Level", text="Level")
    tree.heading("Tag", text="Tag")
    tree.heading("Status", text="Status")

    tree.place(y= 190, x= 10, height= 300, width= 570)

    tree.bind("<Double-1>", double_click)

    s_window.mainloop()



def searching(): # searching engine
    
    txt= search.get()
    cat= catVar.get()
    s= tagVar.get()
    l= levVar.get()

    tree.delete(*tree.get_children())

    if txt:
        
        cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files WHERE file_path LIKE ?", ('%' + txt + '%',))
        for item in cursor.fetchall():
            file = item[0]
            category= item[1]
            level= item[2]
            tags= item[3]
            status= item[4]
            row_data = (file, category, level, tags, status)
            tree.insert("", END, values=row_data)
    if cat:
        cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files WHERE Categoria LIKE ?", ('%' + cat + '%',))
        for item in cursor.fetchall():
            file = item[0]
            category= item[1]
            level= item[2]
            tags= item[3]
            status= item[4]
            row_data = (file, category, level, tags, status)
            tree.insert("", END, values=row_data)
# the tag row needs to be debugged :(
    if s:
        cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files WHERE status= ?", (s,))
        for item in cursor.fetchall():
            file = item[0]
            category= item[1]
            level= item[2]
            tags= item[3]
            status= item[4]
            row_data = (file, category, level, tags, status)
            tree.insert("", END, values=row_data)
    if l:
        cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files WHERE level= ?", (l,))
        for item in cursor.fetchall():
            file = item[0]
            category= item[1]
            level= item[2]
            tags= item[3]
            status= item[4]
            row_data = (file, category, level, tags, status)
            tree.insert("", END, values=row_data)


def add_favorite(): # adding to favorite
    item = tree.selection()[0]  # Get the selected item
    values = tree.item(item, "values") 
    selected_path = values[0]
    cursor.execute('''UPDATE pdf_files SET is_favorite = 1 WHERE file_path = ?''', (selected_path,))
    db.commit()
"""item = tree.selection()[0]: This line retrieves the ID of the selected item in the Treeview widget. tree.selection() returns a list of selected items, and [0] is used to get the first (and presumably only) selected item.

values = tree.item(item, "values"): This line retrieves the values associated with the selected item. The tree.item() method takes the ID of the item and the string "values" as arguments and returns a dictionary containing the values of the item."""


def double_click(event): # opening the file in okular and setting the status to Reading
    item = tree.selection()[0]  # Get the selected item
    values = tree.item(item, "values") 
    selected_path = values[0]

    open_with_okular(selected_path)

    cursor.execute('''UPDATE pdf_files SET status = ? WHERE file_path = ?''', ("Reading", selected_path,))
    db.commit()

def open_with_okular(file_path):
    subprocess.Popen(["okular", file_path])

def clearData():
    catVar.set("Choose a category")
    tagVar.set("Choose status")
    levVar.set("Choose level")
    search.delete(0,END)
# Clear all items from the Treeview
    tree.delete(*tree.get_children())
#tree.get_children() retrieves the IDs of all items in the Treeview.
#The * before tree.get_children() unpacks the list of item IDs, allowing them to be passed as individual arguments to the delete method.
#This effectively deletes all items from the Treeview widget.



with sqlite3.connect("data.db") as db:
    cursor = db.cursor()

