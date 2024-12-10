"""UI utility functions for the application"""
import tkinter as tk
from typing import Tuple

def center_window(window: tk.Tk, width: int, height: int) -> None:
    """Center a window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int(screen_width/2 - width/2)
    y = int(screen_height/2 - height/2)
    window.geometry(f'{width}x{height}+{x}+{y}')