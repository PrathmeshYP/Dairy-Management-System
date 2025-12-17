import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL root password
            port=4306,
            database="dairy_management"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to fetch milk receipt data
def fetch_milk_data(filter_type="daily"):
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()

    if filter_type == "daily":
        query = "SELECT * FROM milk_receipt WHERE received_date = CURDATE()"
    elif filter_type == "monthly":
        query = "SELECT * FROM milk_receipt WHERE MONTH(received_date) = MONTH(CURDATE()) AND YEAR(received_date) = YEAR(CURDATE())"
    else:
        query = "SELECT * FROM milk_receipt"

    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()

    return records

# Function to display reports in Tkinter
def show_report(filter_type="daily"):
    records = fetch_milk_data(filter_type)
    if not records:
        messagebox.showinfo("No Data", f"No {filter_type} records found!")
        return

    report_window = tb.Toplevel()
    report_window.title(f"{filter_type.capitalize()} Milk Receipt Report")
    report_window.geometry("700x400")

    tb.Label(report_window, text=f"{filter_type.capitalize()} Milk Receipt Report", font=("Arial", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(report_window, columns=("ID", "Association", "Quantity", "Fat", "SNF", "Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Association", text="Milk Association")
    tree.heading("Quantity", text="Quantity (L)")
    tree.heading("Fat", text="Fat %")
    tree.heading("SNF", text="SNF %")
    tree.heading("Date", text="Received Date")

    for col in ("ID", "Association", "Quantity", "Fat", "SNF", "Date"):
        tree.column(col, anchor="center", width=120)

    for record in records:
        tree.insert("", tk.END, values=record)

    tree.pack(expand=True, fill="both")

# Function to export reports to Excel
def export_to_excel():
    records = fetch_milk_data("all")
    if not records:
        messagebox.showinfo("No Data", "No records found for export!")
        return

    df = pd.DataFrame(records, columns=["ID", "Association", "Quantity", "Fat", "SNF", "Date"])
    file_path = "Milk_Receipt_Report.xlsx"
    df.to_excel(file_path, index=False)

    messagebox.showinfo("Export Successful", f"Report saved as {file_path}")

# Function to export reports to PDF
def export_to_pdf():
    records = fetch_milk_data("all")
    if not records:
        messagebox.showinfo("No Data", "No records found for export!")
        return

    file_path = "Milk_Receipt_Report.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, height - 50, "Milk Receipt Report")
    
    c.setFont("Helvetica", 10)
    y_position = height - 80
    headers = ["ID", "Association", "Quantity", "Fat", "SNF", "Date"]
    x_positions = [30, 80, 230, 300, 360, 450]

    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y_position, header)

    c.setFont("Helvetica", 9)
    y_position -= 20

    for record in records:
        for i, data in enumerate(record):
            c.drawString(x_positions[i], y_position, str(data))
        y_position -= 15

    c.save()
    messagebox.showinfo("Export Successful", f"PDF saved as {file_path}")

# Tkinter GUI Setup
root = tb.Window(themename="superhero")  
root.title("Milk Receipt Reports - Dairy Management")
root.geometry("500x400")

tb.Label(root, text="Milk Receipt Reports", font=("Arial", 18, "bold"), bootstyle="primary").pack(pady=10)

btn_frame = tb.Frame(root)
btn_frame.pack(pady=10)

tb.Button(btn_frame, text="View Daily Report", command=lambda: show_report("daily"), bootstyle="info", width=20).grid(row=0, column=0, padx=10, pady=5)
tb.Button(btn_frame, text="View Monthly Report", command=lambda: show_report("monthly"), bootstyle="info", width=20).grid(row=0, column=1, padx=10, pady=5)

tb.Button(root, text="Export to Excel", command=export_to_excel, bootstyle="success", width=25).pack(pady=5)
tb.Button(root, text="Export to PDF", command=export_to_pdf, bootstyle="success", width=25).pack(pady=5)

root.mainloop()
