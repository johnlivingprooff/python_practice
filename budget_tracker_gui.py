import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

#  Step 1: Set Up Database
conn = sqlite3.connect("expenses.db")
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


#  Step 2: Function to Add Expense
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()

    if not category or not amount:
        messagebox.showerror("Error", "Please enter all fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, amount, date))
    conn.commit()

    messagebox.showinfo("Success", "Expense added successfully!")
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)


#  Step 3: Function to Show Expenses
def show_expenses():
    cursor.execute("SELECT category, amount, date FROM expenses")
    records = cursor.fetchall()

    expense_window = tk.Toplevel(root)
    expense_window.title("Expense Records")

    tk.Label(expense_window, text="Category", width=15, borderwidth=2, relief="solid").grid(row=0, column=0)
    tk.Label(expense_window, text="Amount", width=15, borderwidth=2, relief="solid").grid(row=0, column=1)
    tk.Label(expense_window, text="Date", width=15, borderwidth=2, relief="solid").grid(row=0, column=2)

    for i, (category, amount, date) in enumerate(records, start=1):
        tk.Label(expense_window, text=category, width=15).grid(row=i, column=0)
        tk.Label(expense_window, text=f"${amount:.2f}", width=15).grid(row=i, column=1)
        tk.Label(expense_window, text=date, width=15).grid(row=i, column=2)


#  Step 4: Function to Visualize Spending
def visualize_expenses():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    records = cursor.fetchall()

    if not records:
        messagebox.showwarning("No Data", "No expenses to visualize.")
        return

    categories = [row[0] for row in records]
    amounts = [row[1] for row in records]

    plt.figure(figsize=(6, 4))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", colors=["red", "blue", "green", "yellow"])
    plt.title("Expense Distribution")
    plt.show()


#  Step 5: Build GUI with Tkinter
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("300x300")

tk.Label(root, text="Budget Tracker", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount ($):").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Show Expenses", command=show_expenses).pack(pady=5)
tk.Button(root, text="Visualize Expenses", command=visualize_expenses).pack(pady=5)

root.mainloop()
conn.close()