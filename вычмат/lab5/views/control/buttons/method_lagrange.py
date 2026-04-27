import tkinter as tk
from tkinter import ttk
from utils.const import COLOR_LAGRANGE
from views.plot.methods_state import methods_state
from utils.const import *


class LagrangeButton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self.state_var = tk.BooleanVar(value=methods_state.is_lagrange_enabled())
        super().__init__(parent, text="Лагранж", variable=self.state_var,
                         command=self._toggle, **kwargs)
        # Для ttk.Checkbutton нужно использовать style для цвета
        # Создаём стиль для цветного текста
        style = ttk.Style()
        style.configure("Lagrange.TCheckbutton", foreground=COLOR_LAGRANGE)
        self.configure(style="Lagrange.TCheckbutton")

    def _toggle(self):
        methods_state.set_lagrange_enabled(self.state_var.get())