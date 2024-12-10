"""Main application entry point"""
import tkinter as tk
from splash_screen import SplashScreen
from login_screen import LoginScreen
from account_screen import AccountScreen
from config import CREDENTIALS

def main():
    root = tk.Tk()
    root.title("Webabiq")
    
    # Set window size and center it
    window_width = 400
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Create and show splash screen
    splash = SplashScreen(root)
    
    # Schedule the login screen to appear after splash
    root.after(3000, lambda: show_login(root, splash))
    
    root.mainloop()

def show_login(root, splash):
    splash.destroy()
    login_screen = LoginScreen(root, CREDENTIALS)
    login_screen.login_success_callback = lambda: show_account(root, login_screen)

def show_account(root, login_screen):
    login_screen.destroy()
    AccountScreen(root)

if __name__ == "__main__":
    main()