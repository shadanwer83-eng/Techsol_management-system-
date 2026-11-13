"""
Main Application Entry Point for Techsol Student Management System
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ensure current directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import database
from dashboard import TechsolDashboard


def enable_windows_dpi_awareness():
    """Enables sharp text and UI rendering on Windows High-DPI screens."""
    try:
        import ctypes
        # Try Per-Monitor DPI awareness (Windows 8.1+)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            # Fallback to system DPI aware (Windows Vista+)
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def main():
    # Set Windows High-DPI awareness
    enable_windows_dpi_awareness()

    # Initialize SQLite database schema and sample records
    try:
        database.init_db()
    except Exception as e:
        # If running without GUI yet, print error
        print(f"Database Initialization Error: {e}", file=sys.stderr)

    # Initialize Tkinter root window
    root = tk.Tk()

    # Global uncaught exception handler for Tkinter callbacks
    def report_callback_exception(exc_type, exc_val, exc_tb):
        import traceback
        err_msg = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
        print("Application Error:\n", err_msg, file=sys.stderr)
        messagebox.showerror(
            "Application Error",
            f"An unexpected error occurred:\n\n{str(exc_val)}\n\nCheck terminal logs for details.",
            parent=root
        )

    root.report_callback_exception = report_callback_exception

    # Create Dashboard Application
    app = TechsolDashboard(root)

    # Responsively fit screen (accounting for taskbar and titlebar)
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = min(1280, max(980, screen_width - 40))
    height = min(680, max(560, screen_height - 90))
    x = max(0, int((screen_width - width) / 2))
    y = max(0, int((screen_height - height) / 2) - 15)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(960, 540)

    # Maximize window cleanly on Windows to ensure 100% full visibility of all controls
    try:
        root.state("zoomed")
    except Exception:
        pass

    # Launch application loop
    root.mainloop()


if __name__ == "__main__":
    main()
