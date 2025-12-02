import tkinter as tk
from tkinter import ttk
from ui import TrackProfilingApp

def main():
    root = tk.Tk()
    root.title("Track Profiling System (Modernized)")
    root.geometry("1200x800")
    
    # Set theme
    style = ttk.Style()
    style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
    
    app = TrackProfilingApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
