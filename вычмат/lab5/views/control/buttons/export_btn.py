import tkinter as tk
from tkinter import ttk
from func_parser.export_file import export_to_file


class ExportButton(ttk.Button):
    def __init__(self, parent, message_area, **kwargs):
        super().__init__(parent, text="Экспорт", command=self._export, **kwargs)
        self.message_area = message_area

    def _export(self):
        export_to_file(self.message_area)