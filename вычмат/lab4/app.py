# Константы окна
WINDOW_TITLE = "Апроксимация функции"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
RESULTS_TEXT_HEIGHT = 8
RESULTS_TEXT_WIDTH = 40

import tkinter as tk
from tkinter import ttk
from table_widget import DataTable, DATA_CHANGED_EVENT
from graph_widget import GraphWidget
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

        # Главный разделитель окна (левая и правая части)
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Левая часть: контейнер для таблицы, кнопок и результатов
        self.left_frame = tk.Frame(self.paned)
        self.paned.add(self.left_frame)

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
        self.results_text.pack(fill=tk.X, padx=5, pady=5)

        # Правая часть: График
        self.right_frame = tk.Frame(self.paned, bg='white', relief=tk.SUNKEN, bd=1)
        self.paned.add(self.right_frame)

        # График с встроенной панелью навигации
        self.graph = GraphWidget(self.right_frame)
        self.graph.pack(fill=tk.BOTH, expand=True)

        # Кнопки в левой части
        buttons_frame = tk.Frame(self.left_frame)
        buttons_frame.pack(pady=5)

        # Кнопка "Вычислить"
        self.calc_button = setup_calc_button(
            buttons_frame,
            self.table,
            self.graph,
            self.results_text
        )

        # Кнопка автообновления
        self.auto_update_btn = setup_auto_update_button(
            buttons_frame,
            self.table,
            self.graph,
            self.results_text,
            self._calc_callback
        )

        # Кнопка режима добавления точек
        self.point_mode_btn = setup_point_mode_button(
            buttons_frame,
            self.graph,
            self.table
        )

        # ВАЖНО: Привязываем событие изменения данных ПОСЛЕ создания всех кнопок
        self.table.bind(DATA_CHANGED_EVENT, self._on_table_data_changed)

        self.data_table = self.table

        # Сразу отображаем начальные точки
        self.root.after(100, self._force_update_points)

    def _force_update_points(self):
        """Принудительно обновляет точки на графике."""
        data = self.table.get_valid_data()
        x_vals = [d['x'] for d in data]
        y_vals = [d['y'] for d in data]
        self.graph.plot_points_only(x_vals, y_vals)

    def _calc_callback(self):
        """Callback для пересчёта аппроксимации."""
        from buttons.calc_button import on_calc_click
        on_calc_click(self.table, self.graph, self.results_text)

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

        # Обновляем точки на графике (это происходит ВСЕГДА)
        self.graph.plot_points_only(x_vals, y_vals)

        # Если автообновление включено - проверяем и пересчитываем
        if self.auto_update_btn.is_active():
            if len(data) >= 4:
                self._calc_callback()
            else:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Недостаточно точек для автообновления\n(нужно ≥4)", "warning")
                self.results_text.tag_config("warning", foreground="orange")