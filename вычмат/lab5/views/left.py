import tkinter as tk
from tkinter import ttk
from utils.const import (
    INNER_LEFT_PERCENT, INNER_RIGHT_PERCENT,
    TOP_PANEL_PERCENT, BOTTOM_PANEL_PERCENT
)
from views.control.container import ControlContainer
from views.table.widget import DataTable
from views.diffs import DiffsContainer
import data.core as core


class LeftPanel(ttk.PanedWindow):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, orient=tk.VERTICAL, **kwargs)
        self.root_window = root_window
        print("[LeftPanel] Инициализация...")
        self._create_panes()

    def _create_panes(self):
        print("[LeftPanel] Создание панелей...")
        self.top_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.add(self.top_paned, weight=TOP_PANEL_PERCENT)

        self.table_frame = ttk.Frame(self.top_paned, relief="sunken", borderwidth=1)
        self.top_paned.add(self.table_frame, weight=INNER_LEFT_PERCENT)

        self.control_frame = ControlContainer(self.top_paned, self.root_window, relief="sunken", borderwidth=1)
        self.top_paned.add(self.control_frame, weight=INNER_RIGHT_PERCENT)

        # Нижняя панель для таблиц разностей
        self.bottom_frame = ttk.Frame(self, relief="groove", borderwidth=2)
        self.add(self.bottom_frame, weight=BOTTOM_PANEL_PERCENT)

        # Добавляем контейнер таблиц разностей с заполнением
        self.diffs_container = DiffsContainer(self.bottom_frame)
        self.diffs_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.table = DataTable(self.table_frame, core)
        print("[LeftPanel] Создание панелей завершено")