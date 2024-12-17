"""Account book main screen implementation"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
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
            text=self.account_data.today_date,
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
            text=f"${self.account_data.total_saving:.2f}",
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
            text=f"${self.account_data.income:.2f}",
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
            text=f"${self.account_data.paid:.2f}",
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
        
        # Monthly summary frame
        monthly_frame = tk.Frame(self, bg="#E75480")
        monthly_frame.pack(fill="x", padx=20, pady=10)
        
        # Year label
        tk.Label(
            monthly_frame,
            text="2024",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(fill="x", pady=5)
        
        # Monthly range and amount
        month_info_frame = tk.Frame(monthly_frame, bg="#E75480")
        month_info_frame.pack(fill="x", pady=5)
        
        self.monthly_range_label = tk.Label(
            month_info_frame,
            text=self.account_data.monthly_range,
            font=("Arial", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_range_label.pack(side="left", padx=20)
        
        self.monthly_amount_label = tk.Label(
            month_info_frame,
            text=f"${self.account_data.monthly_total:.2f}",
            font=("Arial", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_amount_label.pack(side="right", padx=20)
        
        # Transaction history
        self.create_history_view()
    
    def create_history_view(self):
        """Create the transaction history view"""
        # Headers
        headers_frame = tk.Frame(self, bg="#E75480")
        headers_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        headers = ["DATE", "INCOME/PAID", "DESCRIPTION"]
        for header in headers:
            tk.Label(
                headers_frame,
                text=header,
                font=("Arial", 10, "bold"),
                bg="#E75480",
                fg="white",
                width=15
            ).pack(side="left", padx=5, pady=5)
        
        # Scrollable transaction list
        self.transactions_frame = tk.Frame(self, bg="white")
        self.transactions_frame.pack(fill="both", expand=True, padx=20)
        
        self.update_history()
    
    def update_history(self):
        """Update the transaction history display"""
        # Clear existing transactions
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        
        # Add current transactions
        for transaction in reversed(self.account_data.monthly_transactions):
            row = tk.Frame(self.transactions_frame, bg="white")
            row.pack(fill="x", pady=1)
            
            # Date
            tk.Label(
                row,
                text=transaction['date'].strftime("%Y-%m-%d"),
                bg="white",
                width=15
            ).pack(side="left", padx=5)
            
            # Amount with sign
            amount_text = f"+${transaction['amount']:.2f}" if transaction['category'] == 'Income' else f"-${transaction['amount']:.2f}"
            tk.Label(
                row,
                text=amount_text,
                bg="white",
                width=15,
                fg="#E75480" if transaction['category'] == 'Income' else "#666666"
            ).pack(side="left", padx=5)
            
            # Description
            tk.Label(
                row,
                text=transaction['description'],
                bg="white",
                width=15
            ).pack(side="left", padx=5)
    
    def show_entry_dialog(self):
        """Show dialog for entering new transaction"""
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
        """Update all display labels with current data"""
        self.saving_label.config(text=f"${self.account_data.total_saving:.2f}")
        self.income_label.config(text=f"${self.account_data.income:.2f}")
        self.paid_label.config(text=f"${self.account_data.paid:.2f}")
        self.monthly_range_label.config(text=self.account_data.monthly_range)
        self.monthly_amount_label.config(text=f"${self.account_data.monthly_total:.2f}")
        self.update_history()