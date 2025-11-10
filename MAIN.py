import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3 as sq
from PIL import Image
import os

# ---------- SETUP MAIN WINDOW ----------
root = tk.Tk()
root.title("RESTRO")
root.geometry("1680x1050")
root.configure(bg="dark turquoise")

# Optional icon (ignore error if restro.ico not found)
try:
    root.iconbitmap(default='restro.ico')
except:
    pass

custom_font = ("FreeSans", 20)

# ---------- HEADER ----------
header_frame = tk.Frame(root, bg="dark turquoise")
header_frame.pack(fill="x")

title_label = tk.Label(header_frame, text="RESTAURANT MANAGEMENT SYSTEM", font=("FreeSans", 50, "bold"), bg="dark turquoise", fg="Red3")
title_label.pack(side="top", padx=10)

line = tk.Frame(header_frame, height=2, bg="black")
line.pack(fill="x", side="top")

# ---------- MAIN CONTENT ----------
content_frame = tk.Frame(root, bg="dark turquoise")
content_frame.pack(fill="both", expand=True)

# LEFT SIDE MENU
menu_frame = tk.Frame(content_frame, bg="navajo white")
menu_frame.place(relx=0.01, rely=0.05, relwidth=0.25, relheight=0.9)

menu_label = tk.Label(menu_frame, text="MENU", font=("FreeSans", 30, "bold"), bg="navajo white", fg="gray1")
menu_label.pack(pady=10)

menu_items = [
    ("Tea", 20), ("Coffee", 60), ("Any cold drinks", 50), ("Samosas(2 piece)", 50),
    ("Pakoras", 120), ("Panner Tikka", 200), ("Aloo Tikki", 150), ("Veg Manchurian", 150),
    ("Kakori Kebabs", 240), ("Chicken Tikka", 325), ("Dahi Kebabs", 220), ("Fish Pakora", 200),
    ("Raj Kachori", 150), ("Bhajiyas", 80), ("Chana", 250), ("Rajma", 200),
    ("Dal Makhani", 250), ("Dal Tadka", 200), ("Chicken Tikka Masala", 340), ("Butter Chicken", 325),
    ("Palak Panner", 220), ("Veg Briyani", 280), ("Vegetable Korma", 250), ("Chicken Korma", 350),
    ("Chicken Briyani", 220), ("Mutton Briyani", 300), ("Rajasthani Dal Bati", 250),
    ("Butter Naan(Per Piece)", 25), ("Roti(Per Piece)", 12), ("Paratha(per Piece)", 50),
    ("Dosa", 100), ("Kulcha", 65), ("Appam", 165), ("Vegetable salad", 180),
    ("Millet salad", 240), ("Panner Salad", 290), ("Fruit and Nut salad", 320)
]

menu_canvas = tk.Canvas(menu_frame, bg="navajo white")
menu_canvas.pack(side="left", fill="both", expand=True)
menu_scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=menu_canvas.yview)
menu_scrollbar.pack(side="right", fill="y")
menu_canvas.configure(yscrollcommand=menu_scrollbar.set)
menu_inner_frame = tk.Frame(menu_canvas, bg="navajo white")
menu_canvas.create_window((0, 0), window=menu_inner_frame, anchor="nw")

def on_menu_frame_configure(event):
    menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))
menu_inner_frame.bind("<Configure>", on_menu_frame_configure)

# ---------- MENU ITEM LOGIC ----------
selected_items = {}

def add_item(item, price, label):
    if item in selected_items:
        selected_items[item]["quantity"] += 1
    else:
        selected_items[item] = {"price": price, "quantity": 1}
    update_bill()
    label.config(text=f"{item} {price}/- Added")

def remove_item(item, price, label):
    if item in selected_items:
        if selected_items[item]["quantity"] > 1:
            selected_items[item]["quantity"] -= 1
        else:
            del selected_items[item]
        update_bill()
        label.config(text=f"{item} {price}/- Removed")

for item, price in menu_items:
    item_frame = tk.Frame(menu_inner_frame, bg="navajo white")
    item_frame.pack(fill="x")
    item_label = tk.Label(item_frame, text=f"{item} {price}/-", font=(custom_font, 15), bg="navajo white")
    item_label.pack(side="left", padx=10, pady=5, expand=True)

    button_frame = tk.Frame(item_frame, bg="navajo white")
    button_frame.pack(side="right")

    add_button = tk.Button(button_frame, text="+", width=2, height=1, relief="solid", bg="green", font=custom_font)
    add_button.grid(row=0, column=0)
    remove_button = tk.Button(button_frame, text="-", width=2, height=1, relief="solid", bg="red", font=custom_font)
    remove_button.grid(row=0, column=1)

    add_button.config(command=lambda item=item, price=price, label=item_label: add_item(item, price, label))
    remove_button.config(command=lambda item=item, price=price, label=item_label: remove_item(item, price, label))

# ---------- BILLING SECTION ----------
bill_frame = tk.Frame(content_frame, bg="navajo white")
bill_frame.place(relx=0.28, rely=0.05, relwidth=0.7, relheight=0.9)

bill_header = tk.Label(bill_frame, text="Bill", font=("FreeSans", 30, "bold"), bg="navajo white", fg="gray1")
bill_header.pack(pady=10)

welcome_label = tk.Label(bill_frame, text="||---- JAY SHREE RAM ----||\n Welcome to DEVELOPER DHABA ...", font=custom_font, bg="navajo white")
welcome_label.pack()

datetime_label = tk.Label(bill_frame, text=f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=custom_font, bg="navajo white")
datetime_label.pack()

customer_details_frame = tk.Frame(bill_frame, bg="navajo white")
customer_details_frame.pack(fill="x")

customer_name_label = tk.Label(customer_details_frame, text="Customer Name:", font=custom_font, bg="navajo white")
customer_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
customer_name_entry = tk.Entry(customer_details_frame)
customer_name_entry.grid(row=0, column=1, padx=10, pady=5)

mob_no_label = tk.Label(customer_details_frame, text="Mob No:", font=custom_font, bg="navajo white")
mob_no_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
mob_no_entry = tk.Entry(customer_details_frame)
mob_no_entry.grid(row=1, column=1, padx=10, pady=5)

separator = tk.Frame(bill_frame, height=2, bg="black")
separator.pack(fill="x")

billing_items_label = tk.Label(bill_frame, text="Items          Quantity        Price", font=custom_font, bg="navajo white")
billing_items_label.pack(pady=10)

billing_items_frame = tk.Frame(bill_frame, bg="white")
billing_items_frame.pack()

scrollbar = ttk.Scrollbar(billing_items_frame, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="ns")

billing_items_canvas = tk.Canvas(billing_items_frame, bg="white", yscrollcommand=scrollbar.set)
billing_items_canvas.grid(row=0, column=0, sticky="nsew")

scrollbar.config(command=billing_items_canvas.yview)
billing_items_inner_frame = tk.Frame(billing_items_canvas, bg="white")
billing_items_canvas.create_window((0, 0), window=billing_items_inner_frame, anchor="nw")

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))
billing_items_inner_frame.bind("<Configure>", lambda event, canvas=billing_items_canvas: on_frame_configure(billing_items_canvas))

# ---------- BILL UPDATE ----------
def update_bill():
    for widget in billing_items_inner_frame.winfo_children():
        widget.destroy()
    total_price = 0
    for i, (item, details) in enumerate(selected_items.items()):
        tk.Label(billing_items_inner_frame, text=item, font=custom_font, bg="white").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        tk.Label(billing_items_inner_frame, text=details["quantity"], font=custom_font, bg="white").grid(row=i, column=1, padx=10, pady=5)
        tk.Label(billing_items_inner_frame, text=f"{details['price']}/-", font=custom_font, bg="white").grid(row=i, column=2, padx=10, pady=5)
        total_price += details["price"] * details["quantity"]
    tk.Label(billing_items_inner_frame, text=f"Total: {total_price}/-", font=custom_font, bg="white").grid(row=len(selected_items), column=0, columnspan=3, padx=10, pady=5)

# ---------- STORE DATA FUNCTION (SQLite) ----------
def store_billing_data():
    db_path = os.path.abspath("restro.db")
    db = sq.connect(db_path)
    cursor = db.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BILL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            phone_no TEXT,
            ordered_items TEXT,
            total_amount REAL,
            order_datetime TEXT
        )
    ''')

    # Collect data
    customer_name = customer_name_entry.get().strip()
    phone_no = mob_no_entry.get().strip()
    ordered_items = "\n".join([f"{item}: {details['quantity']} @ {details['price']} each"
                               for item, details in selected_items.items()])
    total_amount = sum(details['quantity'] * details['price'] for details in selected_items.values())
    order_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Validate inputs
    if not customer_name or not phone_no or not selected_items:
        messagebox.showwarning("Missing Info", "Please enter customer details and select items.")
        return

    # Insert data
    cursor.execute("""
        INSERT INTO BILL (customer_name, phone_no, ordered_items, total_amount, order_datetime)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_name, phone_no, ordered_items, total_amount, order_datetime))

    db.commit()
    db.close()

    messagebox.showinfo("Data Stored", f"Billing data stored successfully!\nDatabase: {db_path}")

    # -------- BILL WINDOW POPUP --------
    bill_window = tk.Toplevel(root)
    bill_window.title("Customer Bill")
    bill_window.geometry("600x700")
    bill_window.config(bg="white")

    tk.Label(bill_window, text="DEVELOPER DHABA", font=("FreeSans", 30, "bold"), fg="red3", bg="white").pack(pady=10)
    tk.Label(bill_window, text=f"Date: {order_datetime}", font=("FreeSans", 12), bg="white").pack()
    tk.Label(bill_window, text=f"Customer: {customer_name}", font=("FreeSans", 14), bg="white").pack()
    tk.Label(bill_window, text=f"Mobile: {phone_no}", font=("FreeSans", 14), bg="white").pack()

    tk.Label(bill_window, text="\nItems Ordered", font=("FreeSans", 16, "bold"), bg="white").pack()

    bill_text = tk.Text(bill_window, wrap="word", height=20, width=60, font=("FreeSans", 12))
    bill_text.pack(padx=20, pady=10)

    for item, details in selected_items.items():
        bill_text.insert("end", f"{item:<25} x{details['quantity']}  ₹{details['price'] * details['quantity']}\n")

    bill_text.insert("end", f"\n{'-'*40}\n")
    bill_text.insert("end", f"Total Amount: ₹{total_amount}\n")
    bill_text.configure(state="disabled")

    tk.Button(bill_window, text="Close Bill", font=("FreeSans", 14, "bold"),
              bg="deep sky blue", command=bill_window.destroy).pack(pady=15)


# ---------- BUTTONS ----------
store_data_button = tk.Button(bill_frame, text="Generate Bill", command=store_billing_data, bg="deep sky blue", font=custom_font)
store_data_button.pack(pady=10)

separator2 = tk.Frame(bill_frame, height=2, bg="black")
separator2.pack(fill="x")

thank_you_label = tk.Label(bill_frame, text="Thank you, visit again!!", font=("FreeSans", 40, "bold"), bg="navajo white", fg="Red3")
thank_you_label.pack()

root.mainloop()
