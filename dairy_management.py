import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb  # Modern UI themes
from PIL import Image, ImageTk  # Image handling
import os  # To check file existence

# Get script folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set image file name
IMAGE_FILE = "background.jpg"  # Use a correctly saved JPEG file

# Get full path of image
IMAGE_PATH = os.path.join(BASE_DIR, IMAGE_FILE)

# Check if the image exists and is valid
try:
    bg_image = Image.open(IMAGE_PATH)  # Try opening the image
except (FileNotFoundError, Image.UnidentifiedImageError):
    messagebox.showerror("Error", f"Background image not found or corrupted!\n\nPlease place a valid 'background.jpg' in:\n{BASE_DIR}")
    exit()  # Stop execution if the image is missing or invalid

# Function for login verification
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "admin" and password == "password":  # Dummy check
        messagebox.showinfo("Login Success", "Welcome to Dairy Management System!")
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Function to open Dashboard
def open_dashboard():
    login_window.destroy()  # Close login window
    dashboard = tk.Tk()
    dashboard.title("Dairy Management System")
    dashboard.geometry("900x600")
    tb.Style(theme="morph")  # Modern theme

    # Load and resize background image
    bg_image_resized = bg_image.resize((900, 600))
    bg_photo = ImageTk.PhotoImage(bg_image_resized)

    bg_label = tk.Label(dashboard, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference
    bg_label.place(relwidth=1, relheight=1)

    # Title
    ttk.Label(dashboard, text="🐄 Dairy Management System", font=("Helvetica", 20, "bold"), background="white").pack(pady=20)

    # Dashboard Buttons
    btn_frame = ttk.Frame(dashboard, padding=20, style="light.TFrame")
    btn_frame.pack()

    ttk.Button(btn_frame, text="📋 Milk Collection", command=lambda: show_message("Milk Collection"), style="primary.TButton").grid(row=0, column=0, padx=10, pady=10)
    ttk.Button(btn_frame, text="🛒 Product Management", command=lambda: show_message("Product Management"), style="success.TButton").grid(row=0, column=1, padx=10, pady=10)
    ttk.Button(btn_frame, text="📊 Reports & Sales", command=lambda: show_message("Reports & Sales"), style="info.TButton").grid(row=1, column=0, padx=10, pady=10)
    ttk.Button(btn_frame, text="🔐 Logout", command=dashboard.destroy, style="danger.TButton").grid(row=1, column=1, padx=10, pady=10)

    dashboard.mainloop()

# Function to show feature messages
def show_message(module_name):
    messagebox.showinfo(module_name, f"{module_name} Module Coming Soon!")

# Main Login Window
login_window = tk.Tk()
login_window.title("Dairy Management System - Login")
login_window.geometry("600x400")
tb.Style(theme="litera")  # Modern theme

# Load and resize Background Image
bg_image_resized = bg_image.resize((600, 400))
bg_photo = ImageTk.PhotoImage(bg_image_resized)

bg_label = tk.Label(login_window, image=bg_photo)
bg_label.image = bg_photo  # Keep a reference
bg_label.place(relwidth=1, relheight=1)

# Login Frame
frame = ttk.Frame(login_window, padding=20, style="light.TFrame")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Login Title
ttk.Label(frame, text="Dairy Management Login", font=("Helvetica", 14, "bold")).pack(pady=10)

# Username Input
ttk.Label(frame, text="Username").pack()
entry_username = ttk.Entry(frame, width=30)
entry_username.pack(pady=5)

# Password Input
ttk.Label(frame, text="Password").pack()
entry_password = ttk.Entry(frame, width=30, show="*")
entry_password.pack(pady=5)

# Login Button
ttk.Button(frame, text="Login", command=login, style="primary.TButton").pack(pady=10)

login_window.mainloop()
