import tkinter as tk
from tkinter import ttk


class BInput(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.label = ttk.Label(self, text="b =")
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(self, width=8, justify='center')
        self.entry.insert(0, "5")
        self.entry.pack(side=tk.LEFT, padx=5)

    def get_value(self):
        try:
            val = self.entry.get().strip().replace(",", ".")
            return float(val)
        except ValueError:
            return None