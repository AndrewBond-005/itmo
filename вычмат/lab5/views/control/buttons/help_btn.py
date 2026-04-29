import tkinter as tk
from tkinter import ttk
from views.help_window import show_help


class HelpButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Помощь", command=self._show_help, **kwargs)

    def _show_help(self):
        show_help()