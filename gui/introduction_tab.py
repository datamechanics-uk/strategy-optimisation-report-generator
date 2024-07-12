# gui/introduction_tab.py
import tkinter as tk
from tkinter import ttk, messagebox

class IntroductionTab:
    def __init__(self, notebook, market_data):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Introduction")
        self.market_data = market_data
        self.observers = []
        self.create_widgets()

    def create_widgets(self):
        # Strategy Name field
        tk.Label(self.frame, text="Strategy Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.strategy_name = tk.Entry(self.frame, width=50)
        self.strategy_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.frame, text="Specific Goal:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.specific_goal = tk.Entry(self.frame, width=80)
        self.specific_goal.grid(row=1, column=1, padx=5, pady=5)

        # Create a style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.map('Treeview', background=[('selected', '#CCE5FF')])

        # Create the treeview with visible grid lines
        columns = ("Market", "Timeframe", "Data Source", "Optimisation Timespan", "Out-of-Sample Timespan")
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        self.tree.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Add alternating row colors
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#F0F0F0')

        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-1>', self.on_click)

        # Save button
        tk.Button(self.frame, text="Save Changes", command=self.save_changes).grid(row=3, column=0, columnspan=2, pady=10)

        # Additional fields
        tk.Label(self.frame, text="Target Performance Parameter:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.target_performance = tk.Entry(self.frame, width=50)
        self.target_performance.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Optimisation Method:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.optimisation_method = tk.Entry(self.frame, width=50)
        self.optimisation_method.grid(row=5, column=1, padx=5, pady=5)

        # Configure row and column weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Add initial rows
        for i in range(10):
            self.tree.insert('', 'end', values=('', '', '', '', ''), tags=('oddrow',) if i % 2 else ('evenrow',))

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            self.tree.selection_set(self.tree.identify_row(event.y))
            
    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify('column', event.x, event.y)
        
        # If it's the last (empty) row, don't edit
        if item == self.tree.get_children()[-1]:
            return
        
        if item and column:
            # Get column position and item text
            col_num = int(self.tree.identify('column', event.x, event.y).split('#')[1]) - 1
            value = self.tree.set(item, column)
            
            # Create an entry widget for editing
            entry = ttk.Entry(self.tree, width=20)
            entry.insert(0, value)
            entry.select_range(0, tk.END)
            entry.focus()

            # Function to save the edited value
            def save_edit(event):
                self.tree.set(item, column, entry.get())
                entry.destroy()

            # Bind the save function to the Return key and focus out event
            entry.bind('<Return>', save_edit)
            entry.bind('<FocusOut>', save_edit)

            # Place the entry widget on the treeview
            bbox = self.tree.bbox(item, column)
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2])

    def save_changes(self):
        # Clear existing market data
        self.market_data.clear_all_markets()

        # Save all non-empty rows
        markets = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            market_name = values[0]
            if market_name:
                markets.append(market_name)
                self.market_data.add_market(market_name)
                for i, key in enumerate(['timeframe', 'data_source', 'optimisation_timespan', 'out_of_sample_timespan']):
                    self.market_data.set_market_data(market_name, key, values[i+1])

        print("Markets saved in IntroductionTab:", markets)  # Debug print
        print("Markets in market_data after saving:", self.market_data.get_markets())  # Debug print
        
        # Notify observers
        self.notify_observers('update', markets)

        messagebox.showinfo("Success", "Changes saved successfully!")

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, action, markets):
        print("Notifying observers with markets:", markets) # Debug print
        for observer in self.observers:
            observer(action, markets)

    def get_strategy_name(self):
        return self.strategy_name.get()
    
    def get_specific_goal(self):
        return self.specific_goal.get()

    def get_target_performance(self):
        return self.target_performance.get()

    def get_optimisation_method(self):
        return self.optimisation_method.get()

    def get_intro_table_data(self):
        data = []
        for item in self.tree.get_children()[:-1]:  # Exclude the last empty row
            values = self.tree.item(item)['values']
            if values[0]:  # Only include rows with a market name
                data.append(values)
        return data