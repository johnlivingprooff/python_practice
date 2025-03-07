import tkinter as tk
from tkinter import ttk
import sqlite3 as db
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter.font as font
import os

# Set up database
conn = db.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        amount REAL,
        date TEXT
    )
""")
conn.commit()

def add_expense():
    category = category_var.get()
    amount = amount_entry.get()
    date = date_var.get()

    if not amount or amount == "Enter amount":
        messagebox.showerror("Input Error", "Please enter a valid amount.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, amount, date))
    conn.commit()
    messagebox.showinfo("Success", "Expense added successfully!")

    # Reset the fields
    amount_entry.delete(0, 'end')
    amount_entry.insert(0, "Enter amount")
    amount_entry.config(fg="grey")

    date_entry.config(state=tk.DISABLED)
    date_var.set(datetime.now().strftime("%Y-%m-%d"))

def show_expenses():
    expenses_window = tk.Toplevel(root)
    expenses_window.title("Expenses")
    # expenses_window.geometry("1000x300")

    tree = ttk.Treeview(expenses_window, columns=("ID", "Category", "Amount", "Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    tree.heading("Date", text="Date")
    tree.pack(fill=tk.BOTH, expand=True)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def visualize_expenditure():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()

    categories = [row[0] for row in rows]
    amounts = [row[1] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expenditure by Category')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

# Main Window
root = tk.Tk()
root.title("Budget Tracker (v1.0)")
# root.geometry("500x600")

# Window styling

# Adding an icon (Fixed for Linux)
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file="/home/johnlivingprooff/python_practice/imgs/icon.png"))

# Load Custom Fonts
nueue_font_path = os.path.join(os.path.dirname(__file__), "fonts", "neue_mach.otf")
neue_font = font.Font(family="Neue Machina", size=15, weight="normal")

alata_font_path = os.path.join(os.path.dirname(__file__), "fonts", "alata.ttf")
alata_font = font.Font(family="Alata", size=10, weight="normal")

btn_font = font.Font(family="Alata", size=8, weight="bold")
label_font = font.Font(family="Alata", size=7, weight="bold")
label_font2 = font.Font(family="Alata", size=10, weight="bold")


# Load and resize the image
image = Image.open("/home/johnlivingprooff/python_practice/imgs/icon.png")
image = image.resize((70, 70))
icon_image = ImageTk.PhotoImage(image)
ttk.Label(root, image=icon_image).pack(pady=20)

# ttk.Label(root, text="Budget Tracker", font=alata_font).pack(pady=5)
# ttk.Label(root, text="_____________________").pack()

# User Inputs
category_frame = tk.Frame(root)
category_frame.pack(pady=5)

category_label = ttk.Label(category_frame, text="Expense Category", font=label_font2)
category_label.pack(side=tk.LEFT, padx=5)

# Fetch categories from the database
cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
conn.commit()

# Insert default categories if they don't exist
default_categories = ["Food", "Transport", "Entertainment", "Utilities", "Other"]
for category in default_categories:
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
conn.commit()

# Fetch all categories from the database
cursor.execute("SELECT name FROM categories")
categories = [row[0] for row in cursor.fetchall()]

category_var = tk.StringVar(root)
category_var.set(categories[0])  # set the default option
# 0993158315
category_menu = tk.OptionMenu(category_frame, category_var, *categories)
category_menu.config(font=label_font2, bg="#ffffc5", fg="#575757", relief="solid", borderwidth=2)
category_menu.pack(side=tk.LEFT, padx=5)

def add_category():
    new_category = category_entry.get()
    if new_category and new_category not in categories:
        categories.append(new_category)
        category_menu['menu'].add_command(label=new_category, command=tk._setit(category_var, new_category))
        category_entry.delete(0, 'end')
    else:
        messagebox.showwarning("Warning", "Category already exists or is empty")

category_entry_frame = tk.Frame(root)
category_entry_frame.pack(pady=5)

category_entry = tk.Entry(category_entry_frame, width=15, font=label_font2, justify='center', relief="solid", borderwidth=2)
category_entry.insert(0, "Add new category")  # Adding placeholder
category_entry.pack(pady=5, padx=5, ipady=5, ipadx=5, side=tk.LEFT)

def on_category_entry_click(event):
    if category_entry.get() == "Add new category":
        category_entry.delete(0, "end")  # delete all the text in the entry
        category_entry.insert(0, "")  # Insert blank for user input
        category_entry.config(fg="black")

def on_category_focusout(event):
    if category_entry.get() == "":
        category_entry.insert(0, "Add new category")
        category_entry.config(fg="grey")

category_entry.bind("<FocusIn>", on_category_entry_click)
category_entry.bind("<FocusOut>", on_category_focusout)
category_entry.config(fg="grey")

add_category_button = tk.Button(category_entry_frame, text="Add Category", font=btn_font, command=add_category, bg="#444444", fg="white", relief="solid")
add_category_button.pack(pady=5, side=tk.LEFT)

amount_label = ttk.Label(root, text="Amount", font=label_font)
amount_label.pack(pady=5)
amount_entry = tk.Entry(root, width=25, font=neue_font, justify='center', relief="solid", borderwidth=2)
amount_entry.insert(0, "Enter amount")  # Adding placeholder
amount_entry.pack(pady=5, padx=5, ipady=5, ipadx=5)

def on_entry_click(event):
    if amount_entry.get() == "Enter amount":
        amount_entry.delete(0, "end")  # delete all the text in the entry
        amount_entry.insert(0, "")  # Insert blank for user input
        amount_entry.config(fg="black")

def on_focusout(event):
    if amount_entry.get() == "":
        amount_entry.insert(0, "Enter amount")
        amount_entry.config(fg="grey")

amount_entry.bind("<FocusIn>", on_entry_click)
amount_entry.bind("<FocusOut>", on_focusout)
amount_entry.config(fg="grey")

# Date Entry
date_label = ttk.Label(root, text="Date (YYYY-MM-DD)", font=label_font)
date_label.pack(pady=5)

# Set default date to current date
current_date = datetime.now().strftime("%Y-%m-%d")
date_var = tk.StringVar(value=current_date)

date_entry = tk.Entry(root, textvariable=date_var, width=25, font=neue_font, justify='center', relief="solid", borderwidth=2)
date_entry.pack(pady=5, padx=5, ipady=5, ipadx=5)

def enable_custom_date():
    date_entry.config(state=tk.NORMAL)
    date_entry.delete(0, "end")
    date_entry.insert(0, "Enter date")
    date_entry.config(fg="grey")

def on_date_entry_click(event):
    if date_entry.get() == "Enter date":
        date_entry.delete(0, "end")  # delete all the text in the entry
        date_entry.insert(0, "")  # Insert blank for user input
        date_entry.config(fg="black")

def on_date_focusout(event):
    if date_entry.get() == "":
        date_entry.insert(0, "Enter date")
        date_entry.config(fg="grey")

date_entry.bind("<FocusIn>", on_date_entry_click)
date_entry.bind("<FocusOut>", on_date_focusout)
date_entry.config(fg="grey", state=tk.DISABLED)

custom_date_button = tk.Button(root, text="Enter Custom Date", font=btn_font, command=enable_custom_date, bg="#444444", fg="white", relief="solid")
custom_date_button.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Expense", font=btn_font, command=add_expense, bg="green", fg="white", relief="solid")
add_button.pack(pady=0, side=tk.LEFT, padx=10)

show_button = tk.Button(button_frame, text="Show Expenses", font=btn_font, command=show_expenses, bg="#ffffc5", fg="#575757", relief="solid")
show_button.pack(pady=0, side=tk.LEFT, padx=10)

visualize_button = tk.Button(button_frame, text="Visualize", font=btn_font, command=visualize_expenditure, bg="#444444", fg="white", relief="solid")
visualize_button.pack(pady=0, side=tk.LEFT, padx=10)

root.mainloop()
conn.close()
