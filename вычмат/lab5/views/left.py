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

        # Вызываем установку разделителей ПОСЛЕ создания всех панелей
        self.root_window.after(200, self._set_sash_positions)

    def _create_panes(self):
        print("[LeftPanel] Создание панелей...")
        print(f"[LeftPanel] TOP_PANEL_PERCENT = {TOP_PANEL_PERCENT}, BOTTOM_PANEL_PERCENT = {BOTTOM_PANEL_PERCENT}")

        # Верхняя панель (горизонтальное разделение внутри неё)
        self.top_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.add(self.top_paned, weight=TOP_PANEL_PERCENT)

        # Таблица узлов (левая часть верхней панели)
        self.table_frame = ttk.Frame(self.top_paned, relief="sunken", borderwidth=1)
        self.top_paned.add(self.table_frame, weight=INNER_LEFT_PERCENT)
        print(f"[LeftPanel] Таблица узлов: weight={INNER_LEFT_PERCENT}")

        # Панель управления с кнопками (правая часть верхней панели)
        self.control_frame = ControlContainer(self.top_paned, self.root_window,
                                              relief="sunken", borderwidth=1)
        self.top_paned.add(self.control_frame, weight=INNER_RIGHT_PERCENT)
        print(f"[LeftPanel] Панель управления: weight={INNER_RIGHT_PERCENT}")

        # Нижняя панель для таблиц разностей
        self.bottom_frame = ttk.Frame(self, relief="groove", borderwidth=2)
        self.add(self.bottom_frame, weight=BOTTOM_PANEL_PERCENT)
        print(f"[LeftPanel] Нижняя панель: weight={BOTTOM_PANEL_PERCENT}")

        # Добавляем контейнер таблиц разностей с заполнением
        self.diffs_container = DiffsContainer(self.bottom_frame)
        self.diffs_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.table = DataTable(self.table_frame, core)
        print("[LeftPanel] Создание панелей завершено")

    def _set_sash_positions(self):
        """Принудительно устанавливает позиции разделителей"""
        # Для вертикального разделителя (между верхом и низом)
        self.update_idletasks()
        total_height = self.winfo_height()
        print(f"[LeftPanel] DEBUG: высота левой панели = {total_height}")

        if total_height > 10:
            sash_pos = int(total_height * TOP_PANEL_PERCENT / 100)
            self.sashpos(0, sash_pos)
            print(f"[LeftPanel] Вертикальный разделитель на {sash_pos}px (высота={total_height}px)")
        else:
            print(f"[LeftPanel] Высота слишком мала ({total_height}), пробуем ещё...")
            self.root_window.after(100, self._set_sash_positions)
            return

        # Для горизонтального разделителя внутри верхней панели (между таблицей и кнопками)
        self.top_paned.update_idletasks()
        top_width = self.top_paned.winfo_width()
        print(f"[LeftPanel] DEBUG: ширина верхней панели = {top_width}")

        if top_width > 10:
            inner_sash_pos = int(top_width * INNER_LEFT_PERCENT / 100)
            self.top_paned.sashpos(0, inner_sash_pos)
            print(f"[LeftPanel] Горизонтальный разделитель на {inner_sash_pos}px (ширина={top_width}px)")
        else:
            print(f"[LeftPanel] Ширина верхней панели слишком мала ({top_width})")