import tkinter as tk
from tkinter import ttk


class XInput(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.label = ttk.Label(self, text="x =")
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(self, width=12, justify='center')
        self.entry.insert(0, "0.0")
        self.entry.pack(side=tk.LEFT, padx=5)

    def get_value(self):
        """Возвращает float значение x или None при ошибке"""
        try:
            val = self.entry.get().strip().replace(",", ".")
            return float(val)
        except ValueError:
            return None

    def set_value(self, x):
        """Устанавливает значение x"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{x:.6f}")