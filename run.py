import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import logging
from datetime import datetime, date, timedelta

# Configuration
CREDENTIALS = {
    "1": "1",
    "user": "1"
}

# Logging setup
def setup_logger():
    """Set up logging configuration"""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

logger = setup_logger()

# Authentication utilities
def validate_credentials(credentials, username, password):
    """
    Validate user credentials
    Returns tuple (is_valid, error_message)
    """
    if not username or not password:
        return False, "Username and password are required"
    
    if username not in credentials:
        logger.info(f"Login attempt: Username '{username}' not found")
        return False, "Invalid credentials"
        
    if credentials[username] != password:
        logger.info(f"Login attempt: Invalid password for user '{username}'")
        return False, "Invalid credentials"
    
    logger.info(f"Login successful for user: {username}")
    return True, None

# Account Data Management
class AccountData:
    def __init__(self):
        self.transactions = []
    
    def add_transaction(self, amount: float, category: str, description: str):
        """Add a new transaction"""
        self.transactions.append({
            'amount': amount,
            'category': category,
            'description': description,
            'date': datetime.now()
        })
    
    @property
    def today_date(self):
        """Get formatted current date"""
        return datetime.now().strftime("%B %d, %Y")
    
    @property
    def income(self):
        """Calculate total income"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Income')
    
    @property
    def paid(self):
        """Calculate total paid amount"""
        return sum(t['amount'] for t in self.transactions 
                  if t['category'] == 'Paid')
    
    @property
    def total_saving(self):
        """Calculate total savings"""
        return self.income - self.paid
    
    @property
    def monthly_range(self):
        """Get current month range (e.g., '10/1 - 10/31')"""
        today = date.today()
        first_day = date(today.year, today.month, 1)
        if today.month == 12:
            next_month = date(today.year + 1, 1, 1)
        else:
            next_month = date(today.year, today.month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
        return f"{today.month}/1 - {today.month}/{last_day}"
    
    @property
    def monthly_transactions(self):
        """Get transactions for current month"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        return [t for t in self.transactions 
                if t['date'].month == current_month 
                and t['date'].year == current_year]
    
    @property
    def monthly_total(self):
        """Calculate total for current month"""
        monthly = self.monthly_transactions
        income = sum(t['amount'] for t in monthly if t['category'] == 'Income')
        paid = sum(t['amount'] for t in monthly if t['category'] == 'Paid')
        return income - paid

# UI Components
class SplashScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        # Configure pink background
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        # Create assets directory if it doesn't exist
        os.makedirs("assets", exist_ok=True)
        
        # Bind resize event
        self.bind('<Configure>', self.on_resize)
        
        # Create and display the logo
        self.create_logo()
    
    def create_logo(self):
        self.logo_path = os.path.join("assets/logo.png")
        
        if os.path.exists(self.logo_path):
            try:
                # Load original image
                self.original_image = Image.open(self.logo_path)
                self.update_logo_size()
            except Exception as e:
                print(f"Error loading image: {e}")
                self.show_fallback_text()
        else:
            print(f"Logo file not found at: {self.logo_path}")
            self.show_fallback_text()
    
    def update_logo_size(self):
        try:
            # Get current frame size
            frame_width = self.winfo_width()
            frame_height = self.winfo_height()
            
            if frame_width > 1 and frame_height > 1:  # Ensure valid dimensions
                # Resize image to fill frame
                resized_image = self.resize_image(self.original_image, (frame_width, frame_height))
                photo = ImageTk.PhotoImage(resized_image)
                
                # Remove old label if exists
                for widget in self.winfo_children():
                    widget.destroy()
                
                # Create new label with updated image
                logo_label = tk.Label(self, image=photo, bg="#FFB6C1")
                logo_label.image = photo  # Keep a reference!
                logo_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error updating logo size: {e}")
            self.show_fallback_text()
    
    def on_resize(self, event):
        """Handle window resize events"""
        if hasattr(self, 'original_image'):
            self.update_logo_size()
    
    def resize_image(self, image, size):
        """Resize image to fill frame while maintaining aspect ratio"""
        target_width, target_height = size
        original_width, original_height = image.size
        
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        
        ratio = max(width_ratio, height_ratio)
        
        new_size = (int(original_width * ratio), int(original_height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    def show_fallback_text(self):
        """Show fallback text when image cannot be loaded"""
        for widget in self.winfo_children():
            widget.destroy()
            
        label = tk.Label(
            self,
            text="webabiq",
            font=("Arial", 24, "bold"),
            bg="#FFB6C1",
            fg="#FF69B4"
        )
        label.pack(expand=True)

class LoginScreen(tk.Frame):
    def __init__(self, parent, credentials):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.credentials = credentials
        self.login_success_callback = None
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.login_container = tk.Frame(
            self,
            bg="white",
            highlightthickness=0
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = tk.Label(
            self.login_container,
            text="webabiq",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#E75480"
        )
        title.pack(pady=(20, 30))
        
        # Username
        tk.Label(
            self.login_container,
            text="USERNAME",
            font=("Arial", 12),
            bg="white",
            fg="#E75480"
        ).pack(anchor="w", padx=20)
        
        self.username_entry = tk.Entry(
            self.login_container,
            font=("Arial", 12),
            bg="#FFE4E1",
            relief="flat",
            width=30
        )
        self.username_entry.pack(padx=20, pady=(0, 20), ipady=8)
        
        # Password
        tk.Label(
            self.login_container,
            text="PASSWORD",
            font=("Arial", 12),
            bg="white",
            fg="#E75480"
        ).pack(anchor="w", padx=20)
        
        self.password_entry = tk.Entry(
            self.login_container,
            font=("Arial", 12),
            bg="#FFE4E1",
            relief="flat",
            width=30,
            show="•"
        )
        self.password_entry.pack(padx=20, pady=(0, 20), ipady=8)
        
        # Bindings
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        
        # Remember me
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            self.login_container,
            text="REMEMBER ME",
            variable=self.remember_var,
            bg="white",
            font=("Arial", 10)
        )
        remember_check.pack(pady=(0, 20))
        
        # Login button
        tk.Button(
            self.login_container,
            text="LOG IN",
            command=self.login,
            bg="#E75480",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            width=25,
            cursor="hand2"
        ).pack(pady=(0, 20), ipady=8)
        
        # Forgot password
        forgot_link = tk.Label(
            self.login_container,
            text="FORGOT MY PASSWORD?",
            font=("Arial", 10, "underline"),
            fg="#666666",
            cursor="hand2",
            bg="white"
        )
        forgot_link.pack(pady=(0, 20))
        forgot_link.bind("<Button-1>", self.forgot_password)
        
        # Add bottom logo
        self.add_bottom_logo()
        
        # Set initial focus
        self.username_entry.focus()
    
    def add_bottom_logo(self):
        logo_path = os.path.join("assets/loginlogo.png")
        if os.path.exists(logo_path):
            try:
                image = Image.open(logo_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                logo_label = tk.Label(
                    self,
                    image=photo,
                    bg="#FFB6C1"
                )
                logo_label.image = photo
                logo_label.pack(side="bottom", pady=20)
            except Exception as e:
                print(f"Error loading bottom logo: {e}")
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        is_valid, error_message = validate_credentials(self.credentials, username, password)
        
        if is_valid:
            if self.login_success_callback:
                self.login_success_callback()
        else:
            messagebox.showerror("Error", error_message)
    
    def forgot_password(self, event):
        messagebox.showinfo("Forgot Password", "Coming soon")

class AccountScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.account_data = AccountData()
        
        self.configure(bg="#FFB6C1")
        self.pack(fill="both", expand=True)
        
        self.create_widgets()
        self.update_displays()
    
    def create_widgets(self):
        # Header
        tk.Label(
            self,
            text="account book",
            font=("Arial", 32, "bold"),
            bg="#FFB6C1",
            fg="#E75480"
        ).pack(pady=(20, 10))
        
        tk.Label(
            self,
            text=self.account_data.today_date,
            font=("Arial", 14),
            bg="#FFB6C1",
            fg="#666666"
        ).pack(pady=(0, 20))
        
        # Monthly overview
        month_frame = tk.Frame(self, bg="white", padx=30, pady=15)
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
        
        # Transaction buttons
        buttons_frame = tk.Frame(self, bg="#FFB6C1")
        buttons_frame.pack(pady=20)
        
        # Income button
        income_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
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
        paid_frame = tk.Frame(buttons_frame, bg="#E75480", padx=20, pady=10)
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
        monthly_frame = tk.Frame(self, bg="#E75480")
        monthly_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            monthly_frame,
            text=str(datetime.now().year),
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#E75480"
        ).pack(fill="x", pady=5)
        
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
        
        self.transactions_frame = tk.Frame(self, bg="white")
        self.transactions_frame.pack(fill="both", expand=True, padx=20)
    
    def show_entry_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("New Entry")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="Amount:").pack(pady=5)
        amount_entry = tk.Entry(dialog)
        amount_entry.pack(pady=5)
        
        tk.Label(dialog, text="Category:").pack(pady=5)
        category_var = tk.StringVar(value="Income")
        tk.Radiobutton(dialog, text="Income", variable=category_var, 
                      value="Income").pack()
        tk.Radiobutton(dialog, text="Paid", variable=category_var, 
                      value="Paid").pack()
        
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
        self.saving_label.config(text=f"${self.account_data.total_saving:.2f}")
        self.income_label.config(text=f"${self.account_data.income:.2f}")
        self.paid_label.config(text=f"${self.account_data.paid:.2f}")
        self.monthly_amount_label.config(text=f"${self.account_data.monthly_total:.2f}")
        
        # Update history
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
            
        for transaction in reversed(self.account_data.monthly_transactions):
            row = tk.Frame(self.transactions_frame, bg="white")
            row.pack(fill="x", pady=1)
            
            sign = "+" if transaction['category'] == "Income" else "-"
            
            tk.Label(
                row,
                text=transaction['date'].strftime("%Y-%m-%d"),
                bg="white",
                width=15
            ).pack(side="left", padx=5)
            
            tk.Label(
                row,
                text=f"{sign}${transaction['amount']:.2f}",
                bg="white",
                width=15,
                fg="#E75480" if sign == "+" else "#666666"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row,
                text=transaction['description'],
                bg="white",
                width=15
            ).pack(side="left", padx=5)

def main():
    root = tk.Tk()
    root.title("Webabiq")
    
    window_width = 400
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    splash = SplashScreen(root)
    
    def show_login():
        splash.destroy()
        login_screen = LoginScreen(root, CREDENTIALS)
        login_screen.login_success_callback = lambda: show_account(login_screen)
    
    def show_account(login_screen):
        login_screen.destroy()
        AccountScreen(root)
    
    root.after(3000, show_login)
    root.mainloop()

if __name__ == "__main__":
    main()