import tkinter as tk  # Importing the tkinter library for GUI
from tkinter import filedialog  # Importing filedialog module from tkinter for opening file dialogs
import sqlite3  # Importing sqlite3 module for SQLite database operations
import subprocess  # Importing subprocess module for running external applications

# Function to handle the file upload process
def upload_pdf():
    # Open file dialog to select a PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    if file_path:
        # Connect to SQLite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS pdf_files
                          (id INTEGER PRIMARY KEY, file_path TEXT)''')

        # Insert PDF file path into the database
        cursor.execute('''INSERT INTO pdf_files (file_path)
                          VALUES (?)''', (file_path,))
        conn.commit()

        # Close connection
        conn.close()
        print("PDF file path uploaded successfully.")

# Function to open PDF file with Okular
def open_with_okular(file_path):
    subprocess.Popen(["okular", file_path])

# Function to display data from the database
def display_data():
    # Connect to SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch all records from the database
    cursor.execute("SELECT * FROM pdf_files")
    rows = cursor.fetchall()

    # Close connection
    conn.close()

    # Clear previous data in listbox
    file_listbox.delete(0, tk.END)

    # Display fetched data in listbox
    for row in rows:
        file_listbox.insert(tk.END, row[1])

# Create Tkinter window
root = tk.Tk()
root.title("PDF Uploader")  # Setting the title of the window

# Create a button to upload PDF file
upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=20)  # Placing the upload button in the window with some padding

# Create a button to display data from the database
display_button = tk.Button(root, text="Display Data", command=display_data)
display_button.pack(pady=5)  # Placing the display button in the window with some padding

# Function to handle double-click event
def on_double_click(event):
    # Get the path from the listbox
    selected_path = file_listbox.get(tk.ACTIVE)
    open_with_okular(selected_path)  # Open the selected PDF file with Okular

# Create a listbox to display PDF file paths
file_listbox = tk.Listbox(root)
file_listbox.pack(expand=True, fill=tk.BOTH)  # Placing the listbox in the window and configuring to fill both horizontally and vertically

# Bind double-click event to open_with_okular function
file_listbox.bind("<Double-Button-1>", on_double_click)  # Binding double-click event to the listbox

# Run the Tkinter event loop
root.mainloop()
