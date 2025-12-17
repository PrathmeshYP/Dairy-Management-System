import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb  # Modern UI themes

# Function to connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            port=4306,
            database="dairy_management"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to insert milk receipt data
def save_milk_data():
    association = entry_association.get()
    quantity = entry_quantity.get()
    fat_content = entry_fat.get()
    snf = entry_snf.get()
    received_date = entry_date.get()

    if not association or not quantity or not fat_content or not snf or not received_date:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        quantity = float(quantity)
        fat_content = float(fat_content)
        snf = float(snf)
    except ValueError:
        messagebox.showerror("Input Error", "Quantity, Fat %, and SNF must be numbers!")
        return

    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO milk_receipt (association_name, quantity, fat_content, snf, received_date) VALUES (%s, %s, %s, %s, %s)",
        (association, quantity, fat_content, snf, received_date)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Milk receipt data saved successfully!")
    entry_association.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_fat.delete(0, tk.END)
    entry_snf.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# Function to view received milk records
def view_records():
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM milk_receipt")
    records = cursor.fetchall()
    conn.close()

    records_window = tb.Toplevel()
    records_window.title("Milk Receipt Records")
    records_window.geometry("650x350")
    tb.Label(records_window, text="Milk Receipt Records", font=("Arial", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(records_window, columns=("ID", "Association", "Quantity", "Fat", "SNF", "Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Association", text="Milk Association")
    tree.heading("Quantity", text="Quantity (L)")
    tree.heading("Fat", text="Fat %")
    tree.heading("SNF", text="SNF %")
    tree.heading("Date", text="Received Date")

    for col in ("ID", "Association", "Quantity", "Fat", "SNF", "Date"):
        tree.column(col, anchor="center", width=100)

    for record in records:
        tree.insert("", tk.END, values=record)

    tree.pack(expand=True, fill="both")

# Tkinter GUI Setup
root = tb.Window(themename="superhero")  # Modern theme
root.title("Milk Receipt Entry - Dairy Management")
root.geometry("500x500")

# Header
tb.Label(root, text="Milk Receipt Entry", font=("Arial", 18, "bold"), bootstyle="primary").pack(pady=10)

# Form Inputs
input_frame = tb.Frame(root)
input_frame.pack(pady=10)

tb.Label(input_frame, text="Milk Association Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_association = tb.Entry(input_frame, width=30, font=("Arial", 12))
entry_association.grid(row=0, column=1, pady=5)

tb.Label(input_frame, text="Quantity (L):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_quantity = tb.Entry(input_frame, width=30, font=("Arial", 12))
entry_quantity.grid(row=1, column=1, pady=5)

tb.Label(input_frame, text="Fat Content (%):", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_fat = tb.Entry(input_frame, width=30, font=("Arial", 12))
entry_fat.grid(row=2, column=1, pady=5)

tb.Label(input_frame, text="SNF (%):", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_snf = tb.Entry(input_frame, width=30, font=("Arial", 12))
entry_snf.grid(row=3, column=1, pady=5)

tb.Label(input_frame, text="Received Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_date = tb.Entry(input_frame, width=30, font=("Arial", 12))
entry_date.grid(row=4, column=1, pady=5)

# Buttons
btn_frame = tb.Frame(root)
btn_frame.pack(pady=20)

tb.Button(btn_frame, text="Save Data", command=save_milk_data, bootstyle="success", width=15).grid(row=0, column=0, padx=10)
tb.Button(btn_frame, text="View Records", command=view_records, bootstyle="info", width=15).grid(row=0, column=1, padx=10)

root.mainloop()
