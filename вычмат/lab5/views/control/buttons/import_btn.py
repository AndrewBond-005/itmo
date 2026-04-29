import tkinter as tk
from tkinter import ttk
import data.core as core
from func_parser.import_file import import_from_file


class ImportButton(ttk.Button):
    def __init__(self, parent, message_area, **kwargs):
        super().__init__(parent, text="Импорт", command=self._import, **kwargs)
        self.message_area = message_area

    def _import(self):
        x_list, y_list = import_from_file(self.message_area)

        if x_list is None or not x_list:
            return

        # Очищаем и загружаем новые точки
        core.clear_all()
        for x, y in zip(x_list, y_list):
            core.add_point(x, y)

        # Очищаем вычисленные точки
        core.clear_computed_points()

        self.message_area.add_message(f"Импортировано {len(x_list)} точек", "info")