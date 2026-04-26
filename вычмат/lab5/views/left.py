import tkinter as tk
from tkinter import ttk
from utils.const import (
    INNER_LEFT_PERCENT, INNER_RIGHT_PERCENT,
    TOP_PANEL_PERCENT, BOTTOM_PANEL_PERCENT
)
from views.control.container import ControlContainer
from views.table.widget import DataTable
import data.core as core

class LeftPanel(ttk.PanedWindow):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, orient=tk.VERTICAL, **kwargs)
        self.root_window = root_window
        self._create_panes()

    def _create_panes(self):
        self.top_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.add(self.top_paned, weight=TOP_PANEL_PERCENT)

        self.table_frame = ttk.Frame(self.top_paned, relief="sunken", borderwidth=1)
        self.top_paned.add(self.table_frame, weight=INNER_LEFT_PERCENT)

        self.control_frame = ControlContainer(self.top_paned, self.root_window, relief="sunken", borderwidth=1)
        self.top_paned.add(self.control_frame, weight=INNER_RIGHT_PERCENT)

        self.bottom_frame = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.add(self.bottom_frame, weight=BOTTOM_PANEL_PERCENT)

        bottom_label = ttk.Label(self.bottom_frame, text="Здесь будут результаты", font=("Arial", 12))
        bottom_label.pack(expand=True)

        self.table = DataTable(self.table_frame, core)