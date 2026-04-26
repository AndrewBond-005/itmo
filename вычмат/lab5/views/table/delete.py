import tkinter as tk
from utils.const import DELETE_BUTTON_TEXT, RED

class DeleteButton(tk.Button):
    def __init__(self, parent, core_module, row_index, **kwargs):
        super().__init__(parent, text=DELETE_BUTTON_TEXT, command=self._delete,
                         bg=RED, fg="white", font=("Arial", 9, "bold"),
                         relief="raised", bd=1, cursor="hand2", width=3, **kwargs)
        self.core = core_module
        self.row_index = row_index

    def _delete(self):
        self.core.delete_point(self.row_index)