import sqlite3
from tkinter import *
import subprocess  # Importing subprocess module for running external applications
from tkinter import ttk # need this for the Treeview widget
from search import open_with_okular


def view_all_data(): 
    global view_window, tree
    view_window = Toplevel()
    view_window.title("View all data")
    view_window.geometry("600x500")

    # Define and place the buttons using grid
    # this is a list of tuplets and it seems to be more efficient and upgradable as well

# THIS IS SOO FUCKING COOOLLL!!!!!

    buttons = [
    ("View all data", viewAll, "lightblue", "black"),

    ("View favorites", viewFav, "lightgreen", "black"),

    ("View reading", lambda: viewAS("Reading"), "lightpink", "black"),

    ("View completed", lambda: viewAS("Completed"), "lightyellow", "black"),

    ("View not started", lambda: viewAS("Not started"), "lightcoral", "black"),  # Different bg color

    ("Mark as completed", lambda: mark_as_read("Completed"), "lightcyan", "black"),  # Different bg color

    ("Mark as reading", lambda: mark_as_read("Reading"), "lightseagreen", "black"),  # Different bg color

    ("Add to favorite", add_favorite, "orange", "black"),

    ("Remove favorite", removeFav, "lightsteelblue", "black"),  # Different bg color

    ("Exit", view_window.destroy, "red", "white")  # Red bg and white fg for the Exit button
]

    for i, (text, command, bg_color, fg_color) in enumerate(buttons):
        Button(view_window, text=text, command=command, width=15, bg=bg_color, fg=fg_color).grid(row=i//3, column=i%3, padx=5, pady=5)

    
    # Create the Treeview display widget
    tree = ttk.Treeview(view_window)
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

    tree.place(y=190, x=10, height=300, width=570)

    tree.bind("<Double-1>", double_click)

    view_window.mainloop()


def viewAll(): # view all data
    tree.delete(*tree.get_children())
    cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files")
    for item in cursor.fetchall():
            file = item[0]
            category= item[1]
            level= item[2]
            tags= item[3]
            status= item[4]
            row_data = (file, category, level, tags, status)
            tree.insert("", END, values=row_data)

def viewFav():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files WHERE is_favorite = 1")
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

def mark_as_read(status):
    item = tree.selection()[0]  # Get the selected item
    values = tree.item(item, "values") 
    selected_path = values[0]

    cursor.execute('''UPDATE pdf_files SET status = ? WHERE file_path = ?''', (status, selected_path,))
    db.commit()
    viewAll()

def double_click(event): # opening the file in okular and setting the status to Reading
    item = tree.selection()[0]  # Get the selected item
    values = tree.item(item, "values") 
    selected_path = values[0]

    open_with_okular(selected_path)

    cursor.execute('''UPDATE pdf_files SET status = ? WHERE file_path = ?''', ("Reading", selected_path,))
    db.commit()

"""item = tree.selection()[0]: This line retrieves the ID of the selected item in the Treeview widget. tree.selection() returns a list of selected items, and [0] is used to get the first (and presumably only) selected item.

values = tree.item(item, "values"): This line retrieves the values associated with the selected item. The tree.item() method takes the ID of the item and the string "values" as arguments and returns a dictionary containing the values of the item."""

def removeFav():
    item = tree.selection()[0]  # Get the selected item
    values = tree.item(item, "values") 
    selected_path = values[0]
    cursor.execute('''UPDATE pdf_files SET is_favorite = 0 WHERE file_path = ?''', (selected_path,))
    db.commit()
    viewFav()

def viewAS(status):
    tree.delete(*tree.get_children())
    cursor.execute("SELECT file_path, Categoria, level, tag, status FROM pdf_files WHERE status= ?", (status,))
    for item in cursor.fetchall():
            file = item[0]
            category= item[1]
            level= item[2]
            tags= item[3]
            status= item[4]
            row_data = (file, category, level, tags, status)
            tree.insert("", END, values=row_data)


with sqlite3.connect("data.db") as db:
    cursor = db.cursor()
