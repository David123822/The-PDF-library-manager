import tkinter as tk
from tkinter import ttk

def on_double_click(event):
    item = tree.selection()[0]  # Get the selected item
    values = tree.item(item, "values")
    # Extracting the values of the selected item
    name = values[0]
    age = values[1]
    
    # Creating a new window
    new_window = tk.Toplevel(root)
    new_window.title("Details")
    
    # Displaying the details in the new window
    tk.Label(new_window, text="Name: " + name).pack()
    tk.Label(new_window, text="Age: " + age).pack()

root = tk.Tk()

tree = ttk.Treeview(root)
tree["columns"] = ("Name", "Age")
tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column
tree.column("Name", width=100)
tree.column("Age", width=50)
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.insert("", tk.END, text="1", values=("John", "30"))
tree.insert("", tk.END, text="2", values=("Alice", "25"))
tree.grid(row=7, column=2, padx=5, pady=5)

# Bind double click event to the Treeview
tree.bind("<Double-1>", on_double_click)

root.mainloop()
