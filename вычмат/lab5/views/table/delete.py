import tkinter as tk
from utils.const import DELETE_BUTTON_TEXT, RED, CELL_FONT_SIZE

class DeleteButton(tk.Button):
    def __init__(self, parent, core_module, row_index, **kwargs):
        super().__init__(parent, text=DELETE_BUTTON_TEXT, command=self._delete,
                         fg="red", relief="solid", borderwidth=1, bg="white",
                         font=('Arial', CELL_FONT_SIZE - 1), width=3, **kwargs)
        self.core = core_module
        self.row_index = row_index

    def _delete(self):
        self.core.delete_point(self.row_index)