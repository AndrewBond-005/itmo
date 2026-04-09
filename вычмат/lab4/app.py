# Константы окна
WINDOW_TITLE = "Апроксимация функции"
RESULTS_TEXT_HEIGHT = 8
RESULTS_TEXT_WIDTH = 40
LEFT_PANEL_WIDTH_RATIO = 0.33
RIGHT_PANEL_WIDTH_RATIO = 0.67
MIN_POINTS = 8
MAX_POINTS = 12

import tkinter as tk
from tkinter import ttk
from table_widget import DataTable, DATA_CHANGED_EVENT
from graph_widget import GraphWidget
from results_table import ResultsTable
from buttons import (
    setup_calc_button,
    setup_auto_update_button,
    setup_point_mode_button,
    setup_import_export_buttons,
    setup_help_exit  # Импортируем твою функцию
)


class App:
    """Главный класс приложения. Управляет окном и основными виджетами."""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)

        screen_width = self.root.winfo_screenwidth()
        left_width = int(screen_width * LEFT_PANEL_WIDTH_RATIO)
        right_width = int(screen_width * RIGHT_PANEL_WIDTH_RATIO)

        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Левая часть
        self.left_frame = tk.Frame(self.paned, width=left_width)
        self.paned.add(self.left_frame, width=left_width)

        # Правая часть
        self.right_frame = tk.Frame(self.paned, bg='white', relief=tk.SUNKEN, bd=1, width=right_width)
        self.paned.add(self.right_frame, width=right_width)

        # График
        self.graph = GraphWidget(self.right_frame)
        self.graph.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = tk.Label(
            self.left_frame,
            text="Аппроксимация функции",
            font=('Arial', 16, 'bold'),
        )
        title_label.pack()

        # Предупреждение
        self.warning_label = tk.Label(self.left_frame, text="", fg="red", font=('Arial', 9))
        self.warning_label.pack(pady=2)

        def show_warning(msg):
            self.warning_label.configure(text=msg)
            self.root.after(3000, lambda: self.warning_label.configure(text=""))

        # Таблица ввода данных
        self.table = DataTable(self.left_frame, rows=12)
        self.table.pack(fill=tk.BOTH, expand=True)

        # Кнопки первого ряда
        buttons_frame1 = tk.Frame(self.left_frame)
        buttons_frame1.pack(pady=5)

        # Текстовая область
        text_frame = tk.Frame(self.left_frame)
        text_frame.pack(fill=tk.X, padx=5, pady=(5, 0))

        self.results_text = tk.Text(
            text_frame,
            height=RESULTS_TEXT_HEIGHT,
            width=RESULTS_TEXT_WIDTH,
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)

        self.results_table = ResultsTable(self.left_frame)
        self.results_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Callback для вычисления
        def do_calc():
            data = self.table.get_valid_data()
            if len(data) < MIN_POINTS:
                show_warning(f"⚠ Недостаточно точек (нужно ≥{MIN_POINTS})")
                return
            from buttons.calc_button import on_calc_click
            on_calc_click(self.calc_button, self.table, self.graph, self.results_text, self.results_table)

        # Кнопки первого ряда
        self.calc_button = setup_calc_button(
            buttons_frame1,
            self.table,
            self.graph,
            self.results_text,
            self.results_table
        )
        self.calc_button.pack(side=tk.LEFT, padx=5)

        self.point_mode_btn = setup_point_mode_button(
            buttons_frame1,
            self.graph,
            self.table
        )
        self.point_mode_btn.btn.pack(side=tk.LEFT, padx=5)

        self.auto_update_btn = setup_auto_update_button(
            buttons_frame1,
            self.table,
            self.graph,
            self.results_text,
            self.results_table,
            do_calc
        )
        self.auto_update_btn.btn.pack(side=tk.LEFT, padx=5)

        # Кнопки второго ряда (Импорт/Экспорт + Помощь/Выход)
        buttons_frame2 = tk.Frame(self.left_frame)
        buttons_frame2.pack(pady=5)

        # Импорт/Экспорт
        import_export_frame = setup_import_export_buttons(
            buttons_frame2,
            self.table,
            self.results_text,
            self.results_table,
            lambda: MAX_POINTS,
            show_warning
        )
        import_export_frame.pack(side=tk.LEFT, padx=5)

        # Помощь/Выход (твоя функция)
        help_exit_frame = setup_help_exit(buttons_frame2, self.root)
        help_exit_frame.pack(side=tk.LEFT, padx=5)

        self.table.bind(DATA_CHANGED_EVENT, self._on_table_data_changed)
        self.data_table = self.table

        self.root.after(100, self._force_update_points)
        self.root.update_idletasks()
        self.paned.sash_place(0, left_width, 0)

        def clear_all_results():
            self.results_text.delete(1.0, tk.END)
            self.results_table.clear()
            self.graph.clear()

        self.table.set_clear_all_callback(clear_all_results)

    def _force_update_points(self):
        data = self.table.get_valid_data()
        x_vals = [d['x'] for d in data]
        y_vals = [d['y'] for d in data]
        self.graph.plot_points_only(x_vals, y_vals)

    def _on_table_data_changed(self, event=None):
        data = self.table.get_valid_data()
        x_vals = [d['x'] for d in data]
        y_vals = [d['y'] for d in data]

        self.graph.plot_points_only(x_vals, y_vals)

        if len(data) < MIN_POINTS:
            self.warning_label.configure(text=f"⚠ Недостаточно точек (нужно ≥{MIN_POINTS})")
            return
        elif len(data) > MAX_POINTS:
            self.warning_label.configure(text=f"⚠ Слишком много точек (максимум {MAX_POINTS})")
        else:
            self.warning_label.configure(text="")

        if self.auto_update_btn.is_active():
            if len(data) >= MIN_POINTS:
                from buttons.calc_button import on_calc_click
                on_calc_click(self.calc_button, self.table, self.graph, self.results_text, self.results_table)
