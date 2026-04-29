import tkinter as tk
from tkinter import ttk


class FuncInput(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.label = ttk.Label(self, text="Функция f(x) =")
        self.label.pack(side=tk.TOP, anchor="w", padx=5, pady=2)

        self.entry = tk.Entry(self, width=30, font=("Courier", 10))
        self.entry.insert(0, "sin(x)")
        self.entry.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

    def get_value(self):
        return self.entry.get().strip()