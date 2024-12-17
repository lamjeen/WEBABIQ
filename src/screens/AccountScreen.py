"""Main account screen implementation"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from ..components.AccountHeader import AccountHeader
from ..components.MonthlyOverview import MonthlyOverview
from ..components.TransactionButtons import TransactionButtons
from ..components.TransactionHistory import TransactionHistory
from ..components.MonthlyStats import MonthlyStats
from ..utils.account_data import AccountData

class AccountScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.account_data = AccountData()
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.create_widgets()
        self.update_displays()
    
    def create_widgets(self):
        # Header with title and date
        self.header = AccountHeader(self)
        self.header.pack(fill="x")
        
        # Monthly overview
        self.overview = MonthlyOverview(self)
        self.overview.pack(fill="x")
        
        # Transaction buttons
        self.buttons = TransactionButtons(self)
        self.buttons.pack(fill="x")
        
        # Enter button
        tk.Button(
            self,
            text="Enter!",
            font=("Arial", 16, "bold"),
            bg="#FFE4E1",
            fg="#E75480",
            relief="flat",
            padx=40,
            pady=10,
            command=self.show_entry_dialog
        ).pack(pady=20)
        
        # Monthly stats
        self.monthly_stats = MonthlyStats(self)
        self.monthly_stats.pack(fill="x", padx=20, pady=10)
        
        # Transaction history
        self.history = TransactionHistory(self)
        self.history.pack(fill="both", expand=True)
    
    def show_entry_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("New Entry")
        dialog.geometry("300x250")
        
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
        
        # Description entry
        tk.Label(dialog, text="Description:").pack(pady=5)
        desc_entry = tk.Entry(dialog)
        desc_entry.pack(pady=5)
        
        def save_entry():
            try:
                amount = float(amount_entry.get())
                description = desc_entry.get().strip()
                if not description:
                    raise ValueError("Description is required")
                
                self.account_data.add_transaction(
                    amount,
                    category_var.get(),
                    description
                )
                self.update_displays()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(
            dialog,
            text="Save",
            command=save_entry,
            bg="#E75480",
            fg="white",
            relief="flat",
            padx=20,
            pady=5
        ).pack(pady=20)
    
    def update_displays(self):
        """Update all display components with current data"""
        self.overview.update_amount(self.account_data.total_saving)
        self.buttons.update_amounts(self.account_data.income, self.account_data.paid)
        self.monthly_stats.update_stats(self.account_data.monthly_total)
        
        # Update history
        self.history.clear_history()
        for transaction in reversed(self.account_data.monthly_transactions):
            sign = "+" if transaction['category'] == "Income" else "-"
            self.history.add_transaction(
                transaction['date'].strftime("%Y-%m-%d"),
                f"{sign}${transaction['amount']:.2f}",
                transaction['description']
            )