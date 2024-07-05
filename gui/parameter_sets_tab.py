# gui/parameter_sets_tab.py
import tkinter as tk
from tkinter import ttk, messagebox

class ParameterSetsTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Parameter Sets")
        self.create_widgets()

    def create_widgets(self):
        # Style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[('selected', '#CCE5FF')])

        # Treeview
        columns = ("Name", "Description", "Default", "Start", "Step", "End", "Best")
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', style="Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')  # Added anchor for center alignment
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)

        # Scrollbars
        yscrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        yscrollbar.pack(side='right', fill='y')
        xscrollbar = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        xscrollbar.pack(side='bottom', fill='x')
        self.tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        # Alternating row colors
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#F0F0F0')

        # Bind events
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind('<Button-1>', self.on_click)

        # Save button
        tk.Button(self.frame, text="Save Changes", command=self.save_changes).pack(pady=10)

        # Initial rows
        for i in range(10):
            self.tree.insert("", "end", values=("", "", "", "", "", "", ""), tags=('oddrow',) if i % 2 else ('evenrow',))

    def on_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            self.tree.selection_set(self.tree.identify_row(event.y))

    def on_double_click(self, event):
        item = self.tree.identify("item", event.x, event.y)
        column = self.tree.identify("column", event.x, event.y)

        if item and column:
            value = self.tree.set(item, column)

            # Entry widget for editing
            entry = ttk.Entry(self.tree, width=20)
            entry.insert(0, value)
            entry.select_range(0, tk.END)
            entry.focus()

            # Save the edited value
            def save_edited_value(event=None):  # Added event parameter
                self.tree.set(item, column, entry.get())
                entry.destroy()

            # Bind save function to Return key and focus out event
            entry.bind("<Return>", save_edited_value)
            entry.bind("<FocusOut>", save_edited_value)

            # Place entry widget on treeview
            bbox = self.tree.bbox(item, column)
            entry.place(x=bbox[0], y=bbox[1], width=bbox[2])

    def save_changes(self):
        data = self.get_parameter_data()
        print("Saving parameter data:", data)  # Added print statement for debugging
        messagebox.showinfo("Success", "Changes saved successfully!")

    def get_parameter_data(self):
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if values[0]:  # Only include rows with a parameter name
                data.append(values)
        return data