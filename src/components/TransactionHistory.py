"""Transaction history component"""
import tkinter as tk

class TransactionHistory(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#FFB6C1")
        self.create_history_view()
    
    def create_history_view(self):
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
    
    def clear_history(self):
        """Clear all transactions from the history view"""
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
    
    def add_transaction(self, date, amount, description):
        """Add a transaction to the history view"""
        row = tk.Frame(self.transactions_frame, bg="white")
        row.pack(fill="x", pady=1)
        
        # Date
        tk.Label(
            row,
            text=date,
            bg="white",
            width=15
        ).pack(side="left", padx=5)
        
        # Amount
        tk.Label(
            row,
            text=amount,
            bg="white",
            width=15,
            fg="#E75480" if amount.startswith("+") else "#666666"
        ).pack(side="left", padx=5)
        
        # Description
        tk.Label(
            row,
            text=description,
            bg="white",
            width=15
        ).pack(side="left", padx=5)