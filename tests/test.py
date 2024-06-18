import tkinter as tk
from tkinter import filedialog
import sqlite3

# Function to handle the file upload process
def upload_pdf():
    # Open file dialog to select a PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    if file_path:
        # Read the PDF file
        with open(file_path, "rb") as f:
            pdf_data = f.read()

        # Connect to SQLite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS pdf_files
                          (id INTEGER PRIMARY KEY, file_name TEXT, file_data BLOB)''')

        # Insert PDF file into the database
        cursor.execute('''INSERT INTO pdf_files (file_name, file_data)
                          VALUES (?, ?)''', (file_path, pdf_data))
        conn.commit()

        # Close connection
        conn.close()
        print("PDF file uploaded successfully.")

# Create Tkinter window
root = tk.Tk()
root.title("PDF Uploader")

# Create a button to upload PDF file
upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
