import tkinter as tk
from tkinter import ttk


class DrawModeButton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self.mode_on = False
        self.state_var = tk.BooleanVar(value=False)
        super().__init__(parent, text=" Рисовать", variable=self.state_var,
                         command=self._toggle, **kwargs)

    def _toggle(self):
        self.mode_on = self.state_var.get()
        print(f"[DrawModeButton] Режим рисования {'ВКЛЮЧЁН' if self.mode_on else 'ВЫКЛЮЧЁН'}")

    def is_active(self):
        return self.mode_on