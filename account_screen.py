"""Account book main screen implementation"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from account_data import AccountData

class AccountScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.account_data = AccountData()
        
        # Configure gradient background
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title "account book"
        title = tk.Label(
            self,
            text="account book",
            font=("Arial", 32, "bold"),
            bg="#FFB6C1",
            fg="#E75480"
        )
        title.pack(pady=(20, 10))
        
        # Today's date
        date_label = tk.Label(
            self,
            text=self.account_data.get_today_date(),
            font=("Arial", 14),
            bg="#FFB6C1",
            fg="#666666"
        )
        date_label.pack(pady=(0, 20))
        
        # White container for "THIS MONTH" and amount
        month_frame = tk.Frame(
            self,
            bg="white",
            padx=30,
            pady=15
        )
        month_frame.pack(fill="x", padx=20)
        
        tk.Label(
            month_frame,
            text="THIS MONTH",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(side="left")
        
        self.saving_label = tk.Label(
            month_frame,
            text=f"${self.account_data.get_total_saving():.2f}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#E75480"
        )
        self.saving_label.pack(side="right")
        
        # Income and Paid buttons frame
        buttons_frame = tk.Frame(self, bg="#FFB6C1")
        buttons_frame.pack(pady=20)
        
        # Income button
        income_frame = tk.Frame(
            buttons_frame,
            bg="#E75480",
            padx=20,
            pady=10
        )
        income_frame.pack(side="left", padx=10)
        
        tk.Label(
            income_frame,
            text="INCOME",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=5)
        
        self.income_label = tk.Label(
            income_frame,
            text=f"${self.account_data.get_income():.2f}",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        )
        self.income_label.pack(side="right", padx=5)
        
        # Paid button
        paid_frame = tk.Frame(
            buttons_frame,
            bg="#E75480",
            padx=20,
            pady=10
        )
        paid_frame.pack(side="left", padx=10)
        
        tk.Label(
            paid_frame,
            text="PAID",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        ).pack(side="left", padx=5)
        
        self.paid_label = tk.Label(
            paid_frame,
            text=f"${self.account_data.get_paid():.2f}",
            font=("Arial", 12, "bold"),
            bg="#E75480",
            fg="white"
        )
        self.paid_label.pack(side="right", padx=5)
        
        # Enter button
        enter_button = tk.Button(
            self,
            text="Enter!",
            font=("Arial", 16, "bold"),
            bg="#FFE4E1",
            fg="#E75480",
            relief="flat",
            padx=40,
            pady=10,
            command=self.show_entry_dialog
        )
        enter_button.pack(pady=20)
        
        # Book history button
        history_button = tk.Button(
            self,
            text="book history",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#E75480",
            relief="flat",
            padx=40,
            pady=10,
            command=self.show_history
        )
        history_button.pack(side="bottom", pady=20)
    
    def show_entry_dialog(self):
        """Show dialog for entering new transaction"""
        dialog = tk.Toplevel(self)
        dialog.title("New Entry")
        dialog.geometry("300x200")
        
        # Amount entry
        tk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(dialog)
        amount_entry.pack(pady=5)
        
        # Category selection
        tk.Label(dialog, text="Category:").pack(pady=5)
        category_var = tk.StringVar(value="Income")
        tk.Radiobutton(dialog, text="Income", variable=category_var, 
                      value="Income").pack()
        tk.Radiobutton(dialog, text="Paid", variable=category_var, 
                      value="Paid").pack()
        
        def save_entry():
            try:
                amount = float(amount_entry.get())
                self.account_data.add_transaction(amount, category_var.get())
                self.update_displays()
                dialog.destroy()
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid amount")
        
        tk.Button(dialog, text="Save", command=save_entry).pack(pady=20)
    
    def show_history(self):
        """Show transaction history"""
        dialog = tk.Toplevel(self)
        dialog.title("Book History")
        dialog.geometry("400x300")
        
        # Create treeview
        tree = ttk.Treeview(dialog, columns=("Date", "Category", "Amount"))
        tree.heading("Date", text="Date")
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")
        
        for transaction in self.account_data.transactions:
            tree.insert("", "end", values=(
                transaction['date'].strftime("%Y-%m-%d"),
                transaction['category'],
                f"${transaction['amount']:.2f}"
            ))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_displays(self):
        """Update all display labels with current data"""
        self.saving_label.config(text=f"${self.account_data.get_total_saving():.2f}")
        self.income_label.config(text=f"${self.account_data.get_income():.2f}")
        self.paid_label.config(text=f"${self.account_data.get_paid():.2f}")