from tkinter import ttk
from views.control.buttons.exit import ExitButton

class ControlContainer(ttk.Frame):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, **kwargs)
        self.root_window = root_window
        exit_btn = ExitButton(self, self.root_window)
        exit_btn.pack(pady=20, padx=10, anchor="center")
        ttk.Frame(self).pack(expand=True)