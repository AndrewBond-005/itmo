import tkinter as tk
from tkinter import ttk
from func_parser.export_file import export_to_file


class ExportButton(ttk.Button):
    def __init__(self, parent, message_area, methods_panel=None, **kwargs):
        super().__init__(parent, text="Экспорт", command=self._export, **kwargs)
        self.message_area = message_area
        self.methods_panel = methods_panel

    def _export(self):
        export_to_file(self.message_area, self.methods_panel)