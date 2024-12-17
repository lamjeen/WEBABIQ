"""Monthly statistics component"""
import tkinter as tk
from datetime import datetime, date, timedelta

class MonthlyStats(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#E75480")
        self.create_stats_view()
    
    def create_stats_view(self):
        # Year label
        tk.Label(
            self,
            text=str(datetime.now().year),
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(fill="x", pady=5)
        
        # Monthly range and amount
        month_info_frame = tk.Frame(self, bg="#E75480")
        month_info_frame.pack(fill="x", pady=5)
        
        self.monthly_range_label = tk.Label(
            month_info_frame,
            text=self.get_monthly_range(),
            font=("Arial", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_range_label.pack(side="left", padx=20)
        
        self.monthly_amount_label = tk.Label(
            month_info_frame,
            text="$0.00",
            font=("Arial", 12),
            bg="#E75480",
            fg="white"
        )
        self.monthly_amount_label.pack(side="right", padx=20)
    
    def get_monthly_range(self):
        """Calculate the current month's date range"""
        today = date.today()
        first_day = date(today.year, today.month, 1)
        
        # Calculate last day of current month
        if today.month == 12:
            next_month = date(today.year + 1, 1, 1)
        else:
            next_month = date(today.year, today.month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        
        return f"{today.month}/1 - {today.month}/{last_day}"
    
    def update_stats(self, amount):
        """Update the monthly amount display"""
        self.monthly_amount_label.config(text=f"${amount:.2f}")