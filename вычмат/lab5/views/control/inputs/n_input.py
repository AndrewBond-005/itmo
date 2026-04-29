import tkinter as tk
from tkinter import ttk


class NInput(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.label = ttk.Label(self, text="точек n =")
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(self, width=6, justify='center')
        self.entry.insert(0, "10")
        self.entry.pack(side=tk.LEFT, padx=5)

    def get_value(self):
        try:
            return int(self.entry.get().strip())
        except ValueError:
            return None