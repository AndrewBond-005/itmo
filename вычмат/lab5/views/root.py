import tkinter as tk
from tkinter import ttk
from utils.const import LEFT_PANEL_PERCENT, RIGHT_PANEL_PERCENT
from views.left import LeftPanel
from views.right import RightPanel


class RootWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Интерполяция функций")
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")

        print("[RootWindow] Инициализация...")

        self._create_main_paned()
        self._setup_close_handler()
        print("[RootWindow] Инициализация завершена")

    def _create_main_paned(self):
        print("[RootWindow] Создание главной панели...")
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Левая панель
        self.left_panel = LeftPanel(self.main_paned, self.root)
        self.main_paned.add(self.left_panel, weight=LEFT_PANEL_PERCENT)

        # Правая панель с графиком
        self.right_panel = RightPanel(self.main_paned, self.left_panel.control_frame)
        self.main_paned.add(self.right_panel, weight=RIGHT_PANEL_PERCENT)

        # Принудительная установка после отрисовки
        self.root.after(100, self._set_all_sash_positions)

    def _set_all_sash_positions(self):
        """Устанавливает все разделители"""
        # Главный разделитель (левая/правая панель)
        tw = self.main_paned.winfo_width()
        if tw > 10:
            sash_pos = int(tw * LEFT_PANEL_PERCENT / 100)
            self.main_paned.sashpos(0, sash_pos)
            print(f"[RootWindow] Главный разделитель на {sash_pos}px (ширина={tw}px)")
        else:
            self.root.after(50, self._set_all_sash_positions)
            return

        # Разделители внутри левой панели (уже вызываются в LeftPanel)
        # Просто обновляем геометрию
        self.root.update_idletasks()

    def _setup_close_handler(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        print("[RootWindow] Закрытие приложения")
        self.root.destroy()

    def run(self):
        print("[RootWindow] Запуск mainloop")
        self.root.mainloop()