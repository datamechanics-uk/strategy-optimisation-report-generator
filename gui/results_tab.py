# gui/results_tab.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io

class ResultsTab:
    def __init__(self, notebook, market_data):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Results")
        self.market_data = market_data
        self.create_widgets()
        # Populate the market dropdown
        self.update_market_dropdown(self.market_data.get_markets())

    def create_widgets(self):
        # Market selection
        tk.Label(self.frame, text="Select Market:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.market_var = tk.StringVar()
        self.market_dropdown = ttk.Combobox(self.frame, textvariable=self.market_var)
        self.market_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.market_dropdown.bind("<<ComboboxSelected>>", self.load_market_data)

        # Image upload buttons
        tk.Button(self.frame, text="Upload Equity Curve", command=lambda: self.upload_image('equity_curve')).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.frame, text="Upload Performance Metrics", command=lambda: self.upload_image('performance_metrics')).grid(row=1, column=1, padx=5, pady=5)

        # Image display areas
        self.equity_curve_label = tk.Label(self.frame)
        self.equity_curve_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.performance_metrics_label = tk.Label(self.frame)
        self.performance_metrics_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Notes for each market
        tk.Label(self.frame, text="Market Notes:").grid(row=4, column=0, sticky="nw", padx=5, pady=5)
        self.market_notes = tk.Text(self.frame, width=60, height=10)
        self.market_notes.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Save button
        tk.Button(self.frame, text="Save Market Data", command=self.save_market_data).grid(row=5, column=1, padx=5, pady=5)

        # Configure row and column weights
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Initial population of the dropdown
    def update_market_dropdown(self, markets):
        self.market_dropdown['values'] = markets
        if markets and not self.market_var.get():
            self.market_var.set(markets[0])
        # Load data for the initially selected market in intro tab
        self.load_market_data(None)

    def on_market_change(self, action, markets):
        if action == 'update':
            self.update_market_dropdown(markets)
    
    def upload_image(self, image_type):
        market = self.market_var.get()
        if not market:
            messagebox.showerror("Error", "Please select a market first.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            with Image.open(file_path) as image:
                # Create a thumbnail for display
                display_image = image.copy()
                display_image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(display_image)
                
                if image_type == 'equity_curve':
                    self.equity_curve_label.config(image=photo)
                    self.equity_curve_label.image = photo
                else:
                    self.performance_metrics_label.config(image=photo)
                    self.performance_metrics_label.image = photo

                # Save original image data
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format)
                self.market_data.set_market_data(market, image_type, img_byte_arr.getvalue())

    def save_market_data(self):
        market = self.market_var.get()
        if market:
            notes = self.market_notes.get("1.0", tk.END).strip()
            self.market_data.set_market_data(market, 'notes', notes)
            messagebox.showinfo("Success", f"Data for {market} saved successfully!")
        else:
            messagebox.showerror("Error", "Please select a market first.")

    def load_market_data(self, event):
        market = self.market_var.get()
        if market:
            data = self.market_data.get_market_data(market)
            if data:
                # Load notes
                self.market_notes.delete("1.0", tk.END)
                self.market_notes.insert(tk.END, data.get('notes', ''))

                # Load images
                self.load_image(data.get('equity_curve'), self.equity_curve_label)
                self.load_image(data.get('performance_metrics'), self.performance_metrics_label)
            else:
                self.clear_market_data()
        else:
            self.clear_market_data()

    def load_image(self, img_data, label):
        if img_data:
            image = Image.open(io.BytesIO(img_data))
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
        else:
            label.config(image='')

    def clear_market_data(self):
        self.market_notes.delete("1.0", tk.END)
        self.equity_curve_label.config(image='')
        self.performance_metrics_label.config(image='')

    def get_results_data(self):
        return self.market_data.get_all_data()