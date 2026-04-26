import tkinter as tk
from tkinter import ttk
from utils.const import INNER_LEFT_PERCENT
from views.control.container import ControlContainer
from views.table.widget import DataTable
import data.core as core

class LeftPanel(ttk.PanedWindow):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, orient=tk.HORIZONTAL, **kwargs)
        self.root_window = root_window
        self._create_panes()
        self._set_initial_sash_position()

    def _create_panes(self):
        self.left_inner = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.add(self.left_inner, weight=INNER_LEFT_PERCENT)

        table_container = ttk.Frame(self.left_inner)
        table_container.pack(fill="both", expand=True, padx=5, pady=5)

        title_label = ttk.Label(table_container, text="Таблица узлов интерполяции",
                                font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        self.table = DataTable(table_container, core)
        self.table.pack(fill="both", expand=True)

        self.right_inner = ControlContainer(self, self.root_window, relief="sunken", borderwidth=1)
        self.add(self.right_inner, weight=100 - INNER_LEFT_PERCENT)

    def _set_initial_sash_position(self):
        self.after(100, self._update_sash)

    def _update_sash(self):
        total_width = self.winfo_width()
        if total_width > 10:
            self.sashpos(0, int(total_width * INNER_LEFT_PERCENT / 100))