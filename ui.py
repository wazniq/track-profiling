import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import get_session, TrackPoint
import sys
import os

class TrackProfilingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Track Profiling")
        
        # Determine DB path (compatible with PyInstaller and Dev)
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        self.db_path = os.path.join(application_path, 'track_profiling.db')
        self.session = get_session(self.db_path)
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_separator()
        file_menu.add_command(label="Import Excel...", command=self.import_excel)
        file_menu.add_command(label="Export Excel...", command=self.export_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Save Changes", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Validate", command=self.validate_all)
        tools_menu.add_command(label="Calculate Profile", command=self.run_calculations)
        tools_menu.add_separator()
        tools_menu.add_command(label="Generate Distribution Report...", command=self.generate_distribution_report)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Track Profiling\nVersion 1.0\n\nDeveloped by: Athul Vasnik Rahman"))

        # Toolbar (Limits only)
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Label(toolbar, text="Max Lift (mm):").pack(side=tk.LEFT, padx=2)
        self.max_lift_var = tk.StringVar(value="100")
        ttk.Entry(toolbar, textvariable=self.max_lift_var, width=5).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="Max Lower (mm):").pack(side=tk.LEFT, padx=2)
        self.max_lower_var = tk.StringVar(value="50")
        ttk.Entry(toolbar, textvariable=self.max_lower_var, width=5).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        ttk.Button(toolbar, text="Calculate", command=self.run_calculations).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="(Double-click to edit)").pack(side=tk.RIGHT, padx=5)

        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel: Data Grid
        left_panel = ttk.LabelFrame(main_frame, text="Vertical Profile")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Treeview for Data
        self.columns = ('Station', 'Existing Rail Levels', 'Proposed Rail Levels', 'Lift (mm)')
        self.tree = ttk.Treeview(left_panel, columns=self.columns, show='headings')
        
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
            
        # Configure tags for validation
        self.tree.tag_configure('error', background='#ffcccc')
        self.tree.tag_configure('ok', background='white')

        scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bindings
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu) # Right-click
        self.root.bind('<Control-c>', self.copy_selection)
        self.root.bind('<Control-v>', self.paste_selection)
        
        # Context Menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy Row(s)", command=lambda: self.copy_selection(None))
        self.context_menu.add_command(label="Copy Station", command=self.copy_station_column)
        self.context_menu.add_command(label="Copy Proposed Rail Levels", command=self.copy_prl_column)
        self.context_menu.add_command(label="Copy Lift (mm)", command=self.copy_lift_column)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Paste into Station", command=lambda: self.paste_column(0))
        self.context_menu.add_command(label="Paste into Existing Rail Levels", command=lambda: self.paste_column(1))
        self.context_menu.add_command(label="Paste into Proposed Rail Levels", command=lambda: self.paste_column(2))
        
        # Right Panel: Plot
        right_panel = ttk.LabelFrame(main_frame, text="Profile Plot")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.figure, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            col_idx = int(column[1:]) - 1
            # Allow editing Station (0), ERL (1), and PRL (2)
            if col_idx not in [0, 1, 2]:
                return
                
            x, y, width, height = self.tree.bbox(item, column)
            val = self.tree.item(item, "values")[col_idx]
            
            entry = ttk.Entry(self.tree)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, val)
            entry.focus()
            
            def save_edit(event):
                new_val = entry.get()
                current_values = list(self.tree.item(item, "values"))
                current_values[col_idx] = new_val
                self.tree.item(item, values=current_values)
                entry.destroy()
                self.recalc_row(item)
                
            entry.bind('<Return>', save_edit)
            entry.bind('<FocusOut>', lambda e: entry.destroy())

    def recalc_row(self, item):
        # Recalculate Lift and check limits
        vals = list(self.tree.item(item, "values"))
        try:
            erl = float(vals[1])
            prl = float(vals[2])
            diff = prl - erl # In meters
            lift_mm = diff * 1000.0
            vals[3] = f"{lift_mm:.1f}"
            
            # Check limits (Limits are now in mm)
            max_lift_mm = float(self.max_lift_var.get())
            max_lower_mm = float(self.max_lower_var.get())
            
            is_valid = True
            if lift_mm > 0 and lift_mm > max_lift_mm: # Lift
                is_valid = False
            elif lift_mm < 0 and abs(lift_mm) > max_lower_mm: # Lower
                is_valid = False
                
            self.tree.item(item, values=vals, tags=('ok' if is_valid else 'error',))
            self.update_plot() # Refresh plot
        except ValueError:
            pass

    def copy_selection(self, event):
        selection = self.tree.selection()
        if not selection: return
        
        data = []
        for item in selection:
            vals = self.tree.item(item)['values']
            data.append("\t".join(map(str, vals)))
            
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(data))
        self.root.update()

    def validate_all(self):
        for item in self.tree.get_children():
            self.recalc_row(item)

    def paste_selection(self, event):
        self.paste_column(1)

    def paste_column(self, col_idx):
        try:
            data = self.root.clipboard_get()
            rows = data.split('\n')
            selection = self.tree.selection()
            
            if not selection:
                children = self.tree.get_children()
                if children:
                    selection = [children[0]]
                else:
                    return

            start_item = selection[0]
            start_idx = self.tree.index(start_item)
            all_items = self.tree.get_children()
            
            for i, row_data in enumerate(rows):
                if start_idx + i >= len(all_items): break
                
                val = row_data.strip()
                if '\t' in val:
                    val = val.split('\t')[0]
                
                item = all_items[start_idx + i]
                curr_vals = list(self.tree.item(item, "values"))
                
                if col_idx < len(curr_vals):
                    curr_vals[col_idx] = val
                    self.tree.item(item, values=curr_vals)
                    self.recalc_row(item)
                    
        except Exception as e:
            print(f"Paste error: {e}")

    def save_data(self):
        try:
            items = self.tree.get_children()
            for item in items:
                vals = self.tree.item(item, "values")
                stn = float(vals[0])
                erl = float(vals[1])
                prl = float(vals[2])
                
                record = self.session.query(TrackPoint).filter_by(STN=stn).first()
                if record:
                    record.ERL = erl
                    record.PRL = prl
            
            self.session.commit()
            messagebox.showinfo("Success", "Data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Save error: {e}")

    def run_calculations(self):
        print("Running iterative optimization...")
        
        items = self.tree.get_children()
        if not items: return
        
        erls = []
        prls = []
        
        for item in items:
            vals = self.tree.item(item, "values")
            erls.append(float(vals[1]))
            curr_prl = float(vals[2])
            if curr_prl == 0:
                prls.append(float(vals[1]))
            else:
                prls.append(curr_prl)
                
        iterations = 50
        try:
            # Limits in mm, convert to m for calculation
            max_lift = float(self.max_lift_var.get()) / 1000.0
            max_lower = float(self.max_lower_var.get()) / 1000.0
        except ValueError:
            messagebox.showerror("Error", "Invalid limits")
            return

        n = len(prls)
        if n < 3: return
        
        new_prls = prls[:]
        
        for _ in range(iterations):
            temp_prls = new_prls[:]
            for i in range(1, n-1):
                smoothed = (temp_prls[i-1] + temp_prls[i+1]) / 2.0
                
                upper_limit = erls[i] + max_lift
                lower_limit = erls[i] - max_lower
                
                if smoothed > upper_limit:
                    smoothed = upper_limit
                elif smoothed < lower_limit:
                    smoothed = lower_limit
                    
                new_prls[i] = smoothed
                
        for i, item in enumerate(items):
            vals = list(self.tree.item(item, "values"))
            vals[2] = f"{new_prls[i]:.3f}"
            self.tree.item(item, values=vals)
            self.recalc_row(item)
            
        self.update_plot()
        messagebox.showinfo("Success", "Optimization complete.")

    def update_plot(self):
        items = self.tree.get_children()
        stns = []
        erls = []
        prls = []
        
        for item in items:
            vals = self.tree.item(item, "values")
            stns.append(float(vals[0]))
            erls.append(float(vals[1]))
            prls.append(float(vals[2]))
            
        self.ax.clear()
        self.ax.plot(stns, erls, label='Existing', color='blue', alpha=0.7)
        self.ax.plot(stns, prls, label='Proposed', color='red', linestyle='--')
        self.ax.set_xlabel('Station')
        self.ax.set_ylabel('Level (m)')
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()
        
    def generate_distribution_report(self):
        from tkinter import simpledialog, Toplevel
        
        # Ask for number of sub-stations
        sub_count = simpledialog.askinteger("Distribution Report", "Enter number of sub stations between stations:", minvalue=1, maxvalue=20, initialvalue=4)
        if not sub_count: return
        
        items = self.tree.get_children()
        if len(items) < 2:
            messagebox.showerror("Error", "Not enough data to generate report.")
            return
            
        # Create Report Window
        report_win = Toplevel(self.root)
        report_win.title("Lift Distribution Report")
        report_win.geometry("600x400")
        
        # Treeview
        cols = ('Station', 'Sub-Stn', 'Lift (mm)')
        tree = ttk.Treeview(report_win, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        scrollbar = ttk.Scrollbar(report_win, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Calculate Interpolation
        report_data = []
        
        for i in range(len(items) - 1):
            item1 = items[i]
            item2 = items[i+1]
            
            vals1 = self.tree.item(item1, "values")
            vals2 = self.tree.item(item2, "values")
            
            stn1 = float(vals1[0])
            lift1 = float(vals1[3])
            
            # Add Main Station
            tree.insert('', tk.END, values=(f"{stn1:.0f}", "Main", f"{lift1:.1f}"))
            report_data.append({'Station': stn1, 'Sub-Stn': 'Main', 'Lift (mm)': lift1})
            
            lift2 = float(vals2[3])
            
            # Interpolate
            step = (lift2 - lift1) / (sub_count + 1)
            
            for j in range(1, sub_count + 1):
                interp_lift = lift1 + (step * j)
                tree.insert('', tk.END, values=("", f"Sub {j}", f"{interp_lift:.1f}"))
                report_data.append({'Station': stn1, 'Sub-Stn': f"Sub {j}", 'Lift (mm)': interp_lift})
                
        # Add Last Station
        last_vals = self.tree.item(items[-1], "values")
        tree.insert('', tk.END, values=(f"{float(last_vals[0]):.0f}", "Main", f"{float(last_vals[3]):.1f}"))
        report_data.append({'Station': float(last_vals[0]), 'Sub-Stn': 'Main', 'Lift (mm)': float(last_vals[3])})
        
        # Export Button
        def export_report():
            filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
            if not filename: return
            try:
                pd.DataFrame(report_data).to_excel(filename, index=False)
                messagebox.showinfo("Success", "Report exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        btn_frame = ttk.Frame(report_win)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Export to Excel", command=export_report).pack()

    def copy_prl_column(self):
        items = self.tree.get_children()
        data = []
        for item in items:
            vals = self.tree.item(item, "values")
            # PRL is at index 2
            data.append(str(vals[2]))
            
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(data))
        self.root.update()

    def copy_lift_column(self):
        items = self.tree.get_children()
        data = []
        for item in items:
            vals = self.tree.item(item, "values")
            # Lift is at index 3
            data.append(str(vals[3]))
            
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(data))
        self.root.update()

    def copy_station_column(self):
        items = self.tree.get_children()
        data = []
        for item in items:
            vals = self.tree.item(item, "values")
            # Station is at index 0
            data.append(str(vals[0]))
            
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(data))
        self.root.update()

    def show_user_guide(self):
        from tkinter import Toplevel, Text
        
        guide_win = Toplevel(self.root)
        guide_win.title("User Guide")
        guide_win.geometry("600x500")
        
        text_area = Text(guide_win, wrap=tk.WORD, padx=10, pady=10)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        guide_text = """Track Profiling - User Guide

1. Start a New Project
   - Go to File > New Project.
   - Enter the **Starting Station Number** (e.g., 100).
   - Enter the number of stations.

2. Import Data
   - Go to File > Import Excel... to load Station and Existing Rail Levels.
   - Or copy data from Excel and use Right-Click > Paste into Station / Existing Rail Levels.

3. Calculate Profile
   - Click the **"Calculate"** button in the toolbar.
   - This will smooth the profile based on the Max Lift/Lower limits.

4. Validate Limits
   - Set "Max Lift" and "Max Lower" in the toolbar (in mm).
   - Go to Tools > Validate to check for violations (highlighted in RED).

5. Distribution Report
   - Go to Tools > Generate Distribution Report...
   - Enter the number of sub stations between stations.
   - View interpolated lift values and Export to Excel.

6. Copy Results
   - Right-Click > Copy Station / Proposed Rail Levels / Lift (mm).
   - File > Export Excel... to save full results.

7. Save
   - File > Save Changes to save to database.
"""
        text_area.insert(tk.END, guide_text)
        text_area.config(state=tk.DISABLED)
            
    def new_project(self):
        from tkinter import simpledialog
        
        if not messagebox.askyesno("New Project", "This will clear all current data. Continue?"):
            return
            
        start_stn = simpledialog.askfloat("New Project", "Enter Starting Station Number:", initialvalue=0.0)
        if start_stn is None: return
        
        count = simpledialog.askinteger("New Project", "Enter Number of Stations:", minvalue=1, maxvalue=10000)
        if not count:
            return
            
        try:
            self.session.query(TrackPoint).delete()
            for i in range(count):
                stn_val = start_stn + i
                p = TrackPoint(id=i+1, STN=stn_val, ERL=0.0, PRL=0.0)
                self.session.add(p)
                
            self.session.commit()
            self.load_data()
            messagebox.showinfo("Success", f"Created project with {count} stations starting from {start_stn}.")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_data(self):
        try:
            points = self.session.query(TrackPoint).order_by(TrackPoint.STN).all()
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for p in points:
                erl = p.ERL if p.ERL is not None else 0
                prl = p.PRL if p.PRL is not None else 0
                diff = prl - erl
                lift_mm = diff * 1000.0
                
                self.tree.insert('', tk.END, values=(p.STN, erl, prl, f"{lift_mm:.1f}"), tags=('ok',))
                
            self.validate_all()
            self.update_plot()
            
        except Exception as e:
            self.tree.insert('', tk.END, values=(f"Error: {e}",))

    def import_excel(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not filename: return
        
        try:
            df = pd.read_excel(filename)
            # Expecting 'Station' and 'ERL' columns, or just first two columns
            if len(df.columns) < 2:
                raise ValueError("Excel file must have at least 2 columns (Station, Existing Rail Levels)")
                
            self.session.query(TrackPoint).delete()
            
            for i, row in df.iterrows():
                stn = float(row.iloc[0])
                erl = float(row.iloc[1])
                p = TrackPoint(id=i+1, STN=stn, ERL=erl, PRL=0.0)
                self.session.add(p)
                
            self.session.commit()
            self.load_data()
            messagebox.showinfo("Success", "Imported data from Excel.")
            
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    def export_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if not filename: return
        
        try:
            items = self.tree.get_children()
            data = []
            for item in items:
                vals = self.tree.item(item, "values")
                data.append({
                    'Station': float(vals[0]),
                    'Existing Rail Levels': float(vals[1]),
                    'Proposed Rail Levels': float(vals[2]),
                    'Lift (mm)': float(vals[3])
                })
                
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            messagebox.showinfo("Success", "Exported data to Excel.")
            
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

