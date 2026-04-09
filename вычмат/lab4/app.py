# Константы окна
WINDOW_TITLE = "Апроксимация функции"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
RESULTS_TEXT_HEIGHT = 6
RESULTS_TEXT_WIDTH = 40
LEFT_PANEL_WIDTH_RATIO = 0.33
RIGHT_PANEL_WIDTH_RATIO = 0.67

import tkinter as tk
from tkinter import ttk
from table_widget import DataTable, DATA_CHANGED_EVENT
from graph_widget import GraphWidget
from results_table import ResultsTable
from buttons import (
    setup_calc_button,
    setup_auto_update_button,
    setup_point_mode_button
)


class App:
    """Главный класс приложения. Управляет окном и основными виджетами."""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)

        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Вычисляем ширину панелей
        left_width = int(screen_width * LEFT_PANEL_WIDTH_RATIO)
        right_width = int(screen_width * RIGHT_PANEL_WIDTH_RATIO)

        # Главный разделитель окна
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Левая часть
        self.left_frame = tk.Frame(self.paned, width=left_width)
        self.paned.add(self.left_frame, width=left_width)

        # Правая часть
        self.right_frame = tk.Frame(self.paned, bg='white', relief=tk.SUNKEN, bd=1, width=right_width)
        self.paned.add(self.right_frame, width=right_width)

        # Таблица ввода данных
        self.table = DataTable(self.left_frame, rows=12)
        self.table.pack(fill=tk.BOTH, expand=True)

        # Текстовая область для результатов
        self.results_text = tk.Text(
            self.left_frame,
            height=RESULTS_TEXT_HEIGHT,
            width=RESULTS_TEXT_WIDTH,
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.results_text.pack(fill=tk.X, padx=5, pady=(5, 0))

        # Таблица со всеми аппроксимациями
        self.results_table = ResultsTable(self.left_frame)
        self.results_table.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # График
        self.graph = GraphWidget(self.right_frame)
        self.graph.pack(fill=tk.BOTH, expand=True)

        # Кнопки
        buttons_frame = tk.Frame(self.left_frame)
        buttons_frame.pack(pady=5)

        # Кнопка "Вычислить"
        self.calc_button = setup_calc_button(
            buttons_frame,
            self.table,
            self.graph,
            self.results_text,
            self.results_table
        )

        # Callback для вычисления
        def do_calc():
            from buttons.calc_button import on_calc_click
            on_calc_click(self.calc_button, self.table, self.graph, self.results_text, self.results_table)

        # Кнопка автообновления
        self.auto_update_btn = setup_auto_update_button(
            buttons_frame,
            self.table,
            self.graph,
            self.results_text,
            self.results_table,
            do_calc
        )

        # Кнопка режима добавления точек
        self.point_mode_btn = setup_point_mode_button(
            buttons_frame,
            self.graph,
            self.table
        )

        # Привязываем событие изменения данных
        self.table.bind(DATA_CHANGED_EVENT, self._on_table_data_changed)

        self.data_table = self.table

        # Отображаем начальные точки
        self.root.after(100, self._force_update_points)

        # Устанавливаем позицию разделителя
        self.root.update_idletasks()
        self.paned.sash_place(0, left_width, 0)

    def _force_update_points(self):
        """Принудительно обновляет точки на графике."""
        data = self.table.get_valid_data()
        x_vals = [d['x'] for d in data]
        y_vals = [d['y'] for d in data]
        self.graph.plot_points_only(x_vals, y_vals)

    def _on_table_data_changed(self, event=None):
        """
        Обработчик изменения данных в таблице.
        ВСЕГДА обновляет точки на графике.
        Если включено автообновление - пересчитывает аппроксимацию.
        """
        # Получаем актуальные данные
        data = self.table.get_valid_data()
        x_vals = [d['x'] for d in data]
        y_vals = [d['y'] for d in data]

        # Обновляем точки на графике
        self.graph.plot_points_only(x_vals, y_vals)

        # Если автообновление включено - проверяем и пересчитываем
        if self.auto_update_btn.is_active():
            if len(data) >= 4:
                from buttons.calc_button import on_calc_click
                # Передаём self.calc_button как первый аргумент
                on_calc_click(self.calc_button, self.table, self.graph, self.results_text, self.results_table)
            else:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Недостаточно точек для автообновления\n(нужно ≥4)", "warning")
                self.results_text.tag_config("warning", foreground="orange")
                self.results_table.clear()