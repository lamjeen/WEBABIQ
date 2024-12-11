import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os

transactions = []

def add_transaction(amount, category):
    transactions.append({
        'amount': amount,
        'category': category,
        'date': datetime.now()
    })

def get_today_date():
    return datetime.now().strftime("%B %d, %Y")

def get_income():
    return sum(t['amount'] for t in transactions 
              if t['category'] == 'Income')

def get_paid():
    return sum(t['amount'] for t in transactions 
              if t['category'] == 'Paid')

def get_total_saving():
    return get_income() - get_paid()

def update_displays():
    saving_label.config(text=f"${get_total_saving():.2f}")
    income_label.config(text=f"${get_income():.2f}")
    paid_label.config(text=f"${get_paid():.2f}")

def show_entry_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("New Entry")
    dialog.geometry("300x200")
    
    tk.Label(dialog, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(dialog)
    amount_entry.pack(pady=5)
    
    tk.Label(dialog, text="Category:").pack(pady=5)
    category_var = tk.StringVar(value="Income")
    tk.Radiobutton(dialog, text="Income", variable=category_var, 
                  value="Income").pack()
    tk.Radiobutton(dialog, text="Paid", variable=category_var, 
                  value="Paid").pack()
    
    def save_entry():
        try:
            amount = float(amount_entry.get())
            add_transaction(amount, category_var.get())
            update_displays()
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    tk.Button(dialog, text="Save", command=save_entry).pack(pady=20)

def show_history():
    dialog = tk.Toplevel(root)
    dialog.title("Book History")
    dialog.geometry("400x300")
    
    tree = ttk.Treeview(dialog, columns=("Date", "Category", "Amount"))
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    
    for transaction in transactions:
        tree.insert("", "end", values=(
            transaction['date'].strftime("%Y-%m-%d"),
            transaction['category'],
            f"${transaction['amount']:.2f}"
        ))
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

def create_main_window():
    global root, saving_label, income_label, paid_label
    
    root = tk.Tk()
    root.title("Account Book")
    
    window_width = 400
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int(screen_width/2 - window_width/2)
    y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    main_frame = tk.Frame(root, bg="#FFB6C1")
    main_frame.pack(fill="both", expand=True)
    
    tk.Label(
        main_frame,
        text="account book",
        font=("Arial", 32, "bold"),
        bg="#FFB6C1",
        fg="#E75480"
    ).pack(pady=(20, 10))
    
    tk.Label(
        main_frame,
        text=get_today_date(),
        font=("Arial", 14),
        bg="#FFB6C1",
        fg="#666666"
    ).pack(pady=(0, 20))
    
    month_frame = tk.Frame(main_frame, bg="white", padx=30, pady=15)
    month_frame.pack(fill="x", padx=20)
    
    tk.Label(
        month_frame,
        text="THIS MONTH",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#E75480"
    ).pack(side="left")
    
    saving_label = tk.Label(
        month_frame,
        text=f"${get_total_saving():.2f}",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#E75480"
    )
    saving_label.pack(side="right")
    
    buttons_frame = tk.Frame(main_frame, bg="#FFB6C1")
    buttons_frame.pack(pady=20)
    
    income_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
    income_frame.pack(side="left", padx=10)
    
    tk.Label(
        income_frame,
        text="INCOME",
        font=("Arial", 12, "bold"),
        bg="#E75480",
        fg="white"
    ).pack(side="left", padx=5)
    
    income_label = tk.Label(
        income_frame,
        text=f"${get_income():.2f}",
        font=("Arial", 12, "bold"),
        bg="#E75480",
        fg="white"
    )
    income_label.pack(side="right", padx=5)

    paid_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
    paid_frame.pack(side="left", padx=10)
    
    tk.Label(
        paid_frame,
        text="PAID",
        font=("Arial", 12, "bold"),
        bg="#E75480",
        fg="white"
    ).pack(side="left", padx=5)
    
    paid_label = tk.Label(
        paid_frame,
        text=f"${get_paid():.2f}",
        font=("Arial", 12, "bold"),
        bg="#E75480",
        fg="white"
    )
    paid_label.pack(side="right", padx=5)
    
    tk.Button(
        main_frame,
        text="Enter!",
        font=("Arial", 16, "bold"),
        bg="#FFE4E1",
        fg="#E75480",
        relief="flat",
        padx=40,
        pady=10,
        command=show_entry_dialog
    ).pack(pady=20)
    
    tk.Button(
        main_frame,
        text="book history",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#E75480",
        relief="flat",
        padx=40,
        pady=10,
        command=show_history
    ).pack(side="bottom", pady=20)

def main():
    create_main_window()
    root.mainloop()

if __name__ == "__main__":
    main()