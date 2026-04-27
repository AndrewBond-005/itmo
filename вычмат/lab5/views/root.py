import tkinter as tk
from tkinter import ttk
from utils.const import LEFT_PANEL_PERCENT
from views.left import LeftPanel
from views.right import RightPanel


class RootWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Интерполяция функций")
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        self._create_main_paned()
        self._setup_close_handler()

    def _create_main_paned(self):
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        self.left_panel = LeftPanel(self.main_paned, self.root)
        self.main_paned.add(self.left_panel, weight=LEFT_PANEL_PERCENT)

        # Передаём control_frame (который внутри left_panel) в правую панель
        self.right_panel = RightPanel(self.main_paned, self.left_panel.control_frame)
        self.main_paned.add(self.right_panel, weight=100 - LEFT_PANEL_PERCENT)

        self.root.after(100, self._set_initial_sash)

    def _set_initial_sash(self):
        tw = self.main_paned.winfo_width()
        if tw > 10:
            self.main_paned.sashpos(0, int(tw * LEFT_PANEL_PERCENT / 100))

    def _setup_close_handler(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()