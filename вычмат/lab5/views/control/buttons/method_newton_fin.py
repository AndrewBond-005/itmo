import tkinter as tk
from tkinter import ttk
from utils.const import COLOR_NEWTON_FIN
from views.plot.methods_state import methods_state
from utils.const import *


class NewtonFinButton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self.state_var = tk.BooleanVar(value=methods_state.is_newton_fin_enabled())
        super().__init__(parent, text="Ньютон (кон)", variable=self.state_var,
                         command=self._toggle, **kwargs)
        # Создаём стиль для цветного текста
        style = ttk.Style()
        style.configure("NewtonFin.TCheckbutton", foreground=COLOR_NEWTON_FIN)
        self.configure(style="NewtonFin.TCheckbutton")

    def _toggle(self):
        methods_state.set_newton_fin_enabled(self.state_var.get())