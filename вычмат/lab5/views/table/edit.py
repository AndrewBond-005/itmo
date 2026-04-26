import tkinter as tk

class CellEditor:
    def __init__(self, treeview, core_module):
        self.treeview = treeview
        self.core = core_module
        self.entry = None

    def start_edit(self, event):
        pass  # не используется, редактирование через Entry в таблице