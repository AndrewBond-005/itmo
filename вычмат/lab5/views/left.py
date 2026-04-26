import tkinter as tk
from tkinter import ttk
from utils.const import (
    INNER_LEFT_PERCENT,
    INNER_RIGHT_PERCENT,
    TOP_PANEL_PERCENT,
    BOTTOM_PANEL_PERCENT
)
from views.control.container import ControlContainer
from views.table.widget import DataTable
import data.core as core

class LeftPanel(ttk.PanedWindow):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, orient=tk.VERTICAL, **kwargs)
        self.root_window = root_window
        self._create_panes()
        self._set_initial_sash_position()

    def _create_panes(self):
        # Верхняя часть (левая верхняя + правая верхняя) - 60% высоты
        self.top_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.add(self.top_paned, weight=TOP_PANEL_PERCENT)

        # Левая верхняя — таблица (40% ширины top_paned)
        self.table_frame = ttk.Frame(self.top_paned, relief="sunken", borderwidth=1)
        self.top_paned.add(self.table_frame, weight=INNER_LEFT_PERCENT)

        # Правая верхняя — кнопки управления (60% ширины top_paned)
        self.control_frame = ControlContainer(self.top_paned, self.root_window, relief="sunken", borderwidth=1)
        self.top_paned.add(self.control_frame, weight=INNER_RIGHT_PERCENT)

        # Нижняя часть — для результатов (40% высоты)
        self.bottom_frame = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.add(self.bottom_frame, weight=BOTTOM_PANEL_PERCENT)

        # Заглушка в нижней части
        bottom_label = ttk.Label(self.bottom_frame, text="Здесь будут результаты", font=("Arial", 12))
        bottom_label.pack(expand=True)

        # Таблица
        self.table = DataTable(self.table_frame, core)

    def _set_initial_sash_position(self):
        """Устанавливает начальное положение разделителей"""
        self.after(100, self._update_vertical_sash)
        self.after(100, self._update_horizontal_sash)

    def _update_vertical_sash(self):
        """Обновляет вертикальный разделитель (верх/низ)"""
        total_height = self.winfo_height()
        if total_height > 10:
            sash_pos = int(total_height * TOP_PANEL_PERCENT / 100)
            self.sashpos(0, sash_pos)

    def _update_horizontal_sash(self):
        """Обновляет горизонтальный разделитель (левая верхняя/правая верхняя)"""
        total_width = self.top_paned.winfo_width()
        if total_width > 10:
            sash_pos = int(total_width * INNER_LEFT_PERCENT / 100)
            self.top_paned.sashpos(0, sash_pos)