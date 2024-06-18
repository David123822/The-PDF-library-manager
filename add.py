from tkinter import *
from tkinter import filedialog
import sqlite3



def add_to_database(): # display
    global add_pdf, pdf, selCathegory, tag_vars, beg_var, int_var, adv_var, other_var, tags

    add_pdf = Toplevel()
    add_pdf.title("Adding the PDF file")
    add_pdf.geometry("750x500")

    pdf = Button(add_pdf, text="Choose file", command=choose_file)
    pdf.grid(row=0, column=0, padx=15, pady=15)

    Button(add_pdf, text="Add to database", command=addData, bg="blue", fg="white").grid(row=0, column=2, padx=5, pady=5)
    Button(add_pdf, text="Exit", command=add_pdf.destroy, bg="red", fg="white").grid(row=1, column=2, padx=5, pady=5)

# List of available programming languages

    programming_languages = ["Python", "JavaScript", "Java", "BASH", "Hacking", "Naughty", "Other"]

    selCathegory = StringVar()
    selCathegory.set("Select the programming language")  # Set the initial value

# Create the OptionMenu with the programming languages as options
# *programming_languages is used to unpack the list and pass its elements as individual arguments to the OptionMenu constructor

    OptionMenu(add_pdf, selCathegory, *programming_languages).grid(row=1, column=0)

# choosing the level

    Label(add_pdf, text="Choose a level:", font=("Palatino Linotype", 12)).grid(row=4, column=0, pady=10, columnspan=4)

    beg_var = IntVar() # much easyer to check if the checkbox was clicked or not
    int_var = IntVar()
    adv_var = IntVar()
    other_var = IntVar()

    Checkbutton(add_pdf, text="Beginner", variable= beg_var).grid(row=5, column=0, padx=5, pady=5)
    Checkbutton(add_pdf, text="Intermediate", variable= int_var).grid(row=5, column=1, padx=5, pady=5)
    Checkbutton(add_pdf, text="Advanced", variable= adv_var).grid(row=5, column=2, padx=5, pady=5)
    Checkbutton(add_pdf, text="Other", variable= other_var).grid(row=5, column=3, padx=5, pady=5)

    
# adding the tags

    Label(add_pdf, text="Tags:", font=("Garamond", 12)).grid(row=6, column=0, columnspan=4, pady=10)

    tags = [
    "Hacking",
    "Networking",
    "Viruses",
    "Wireless",
    "PEN-testing",
    "WEB-PEN-testing",
    "Automation",
    "WEB-dev",
    "Games",
    "SQL",
    "Administration",
    "Cryptography",
    "Scripting",
    "Software QA testing",
    "Dirty",
    "Other"
]
    
    tag_vars = {tag: IntVar() for tag in tags}  # Dictionary to store IntVars for each tag
    for i, tag in enumerate(tags):
        Checkbutton(add_pdf, text=tag, variable=tag_vars[tag]).grid(row=i // 4 + 7, column=i % 4, padx=5, pady=5)

    add_pdf.mainloop()

def choose_file():
    global path

    path = filedialog.askopenfilename(filetypes=[("PDF files","*.pdf")])
    pdf.config(text="PDF Selected")  # Change the text of the button

def addData(): # data colection 

    sel_tags = []

    categoria = selCathegory.get() # here i get the category

# here i get the level

    if beg_var.get() == 1:
        level = "Beginner"
    elif int_var.get() == 1:
        level = "Intermediate"
    elif adv_var.get() == 1:
        level = "Advanced"
    elif other_var.get() == 1:
        level = "Other"

# here i get the tags

    for tag, var in tag_vars.items():  # Iterate over key-value pairs of tag_vars .items() method will return a tuplet 
        if var.get() == 1:  # Check if the IntVar associated with the tag is set to 1 (checked)
            sel_tags.append(tag)  # Append the tag to the sel_tags list if it is checked
    
    cursor.execute("INSERT INTO pdf_files (file_path, Categoria, level, tag) VALUES (?,?,?,?)", (path, categoria, level,', '.join(sel_tags)))
    db.commit()

    clear_all_data()

def clear_all_data():
    # Clear the selected file path
    path = ""
    pdf.configure(text="Choose file")

    # Reset the category selection
    selCathegory.set("Select the programming language")

    # Reset the level checkboxes
    beg_var.set(0)
    int_var.set(0)
    adv_var.set(0)
    other_var.set(0)

    # Reset all tag checkboxes
# .values() method in Python is used to return a view of all values available in a dictionary

    for var in tag_vars.values(): # .values() will only access the value for each tag in the dictionary and the .keys() will only access the keys from the dictionary
        var.set(0)


with sqlite3.connect("data.db") as db:
    cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS pdf_files(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               file_path TEXT NOT NULL,
               Categoria TEXT NOT NULL,
               level TEXT,
               tag TEXT,
               is_favorite INTEGER DEFAULT 0,
               status TEXT DEFAULT 'Not started');""")