import tkinter as tk
from tkinter import ttk
import data.core as core


class AutoUpdateButton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self.state_var = tk.BooleanVar(value=core.get_auto_update())
        super().__init__(parent, text="Авто", variable=self.state_var,
                         command=self._toggle, **kwargs)

    def _toggle(self):
        core.set_auto_update(self.state_var.get())