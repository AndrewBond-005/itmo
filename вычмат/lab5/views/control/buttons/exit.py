import tkinter as tk
from utils.const import RED

class ExitButton(tk.Button):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, text="Выход", command=self._exit_app,
                         bg=RED, fg="white", font=("Arial", 10, "bold"),
                         relief="raised", bd=2, activebackground="darkred",
                         activeforeground="white", cursor="hand2", **kwargs)
        self.root_window = root_window

    def _exit_app(self):
        if self.root_window:
            self.root_window.destroy()