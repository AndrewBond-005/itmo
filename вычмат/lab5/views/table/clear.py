import tkinter as tk
from utils.const import CLEAR_ALL_TEXT, RED, DEFAULT_ROWS, CELL_FONT_SIZE

class ClearAllButton(tk.Button):
    def __init__(self, parent, core_module, **kwargs):
        super().__init__(parent, text=CLEAR_ALL_TEXT, command=self._clear_all,
                         bg=RED, fg="white", font=('Arial', CELL_FONT_SIZE, 'bold'),
                         relief="raised", bd=1, cursor="hand2", width=3, **kwargs)
        self.core = core_module

    def _clear_all(self):
        self.core.clear_all()
        # Создаём 10 пустых строк
        for _ in range(DEFAULT_ROWS):
            self.core.add_point(None, None)