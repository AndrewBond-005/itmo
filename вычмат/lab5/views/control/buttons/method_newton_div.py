import tkinter as tk
from tkinter import ttk
from utils.const import COLOR_NEWTON_DIV
from views.plot.methods_state import methods_state
from utils.const import *


class NewtonDivButton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self.state_var = tk.BooleanVar(value=methods_state.is_newton_div_enabled())
        super().__init__(parent, text="Ньютон (разд)", variable=self.state_var,
                         command=self._toggle, **kwargs)
        # Создаём стиль для цветного текста
        style = ttk.Style()
        style.configure("NewtonDiv.TCheckbutton", foreground=COLOR_NEWTON_DIV)
        self.configure(style="NewtonDiv.TCheckbutton")

    def _toggle(self):
        methods_state.set_newton_div_enabled(self.state_var.get())