# Константы таблицы результатов
FONT_SIZE = 12
FONT_FAMILY = "Arial"
FONT_BOLD = (FONT_FAMILY, FONT_SIZE, "bold")
FONT_NORMAL = (FONT_FAMILY, FONT_SIZE)

COLUMN_WIDTHS = {
    "Тип": 150,
    "a": 65,
    "b": 65,
    "c": 65,
    "d": 65,
    "S": 65,
    "δ": 65,
    "R²": 65,
    "r": 70
}

ROW_HEIGHT = 25
HEADER_BG = "lightgray"
CELL_BG = "white"
SELECTED_BG = "#0078d4"  # Синий цвет для выделенной строки
SELECTED_FG = "white"
GRID_COLOR = "gray"
BORDER_RELIEF = "solid"
BORDER_WIDTH = 1
CELL_PAD = 0

import tkinter as tk
from tkinter import ttk
from utils import format_number


class ResultsTable(ttk.Frame):
    """Виджет таблицы для отображения всех аппроксимаций."""

    def __init__(self, parent):
        super().__init__(parent)
        self.headers = ["Тип", "a", "b", "c", "d", "S", "δ", "R²", "r"]
        self.labels = []
        self.approximations_data = []
        self.selected_rows = set()  # Множество выделенных строк
        self.graph_callback = None
        self._create_table()

    def set_graph_callback(self, callback):
        """Устанавливает callback для отображения функции на графике."""
        self.graph_callback = callback

    def _on_row_click(self, row_idx):
        """Обработчик клика по строке - переключает выделение."""
        if row_idx >= len(self.approximations_data):
            return

        # Переключаем выделение
        if row_idx in self.selected_rows:
            self.selected_rows.remove(row_idx)
            for label in self.labels[row_idx]:
                label.configure(bg=CELL_BG, fg="black")
        else:
            self.selected_rows.add(row_idx)
            for label in self.labels[row_idx]:
                label.configure(bg=SELECTED_BG, fg=SELECTED_FG)


        # Вызываем callback для обновления графика
        if self.graph_callback:
            self.graph_callback()

    def get_selected_approximations(self):
        """Возвращает список выделенных аппроксимаций."""
        result = [self.approximations_data[i] for i in self.selected_rows
                  if i < len(self.approximations_data)]
        return result

    def update_results(self, approximations, saved_selected_names=None):
        """Заполняет таблицу данными аппроксимаций."""

        # Сохраняем старые названия выбранных аппроксимаций
        old_selected_names = set()
        for idx in self.selected_rows:
            if idx < len(self.approximations_data):
                old_selected_names.add(self.approximations_data[idx]['name'])

        self.approximations_data = approximations

        # Очищаем таблицу
        for row in range(self.rows_count):
            for col in range(len(self.headers)):
                self.labels[row][col].config(text="", bg=CELL_BG, fg="black")

        if not approximations:
            self.selected_rows.clear()
            return

        # ВАЖНО: Не сбрасываем selected_rows, а обновляем индексы
        new_selected_rows = set()

        for row, approx in enumerate(approximations):
            if row >= self.rows_count:
                break

            name = approx['name']

            # Восстанавливаем выделение если было
            if name in old_selected_names:
                self.selected_rows.add(row)

            coeffs = approx['coeffs']

            if name == 'Линейная':
                a = format_number(coeffs[0])
                b = format_number(coeffs[1])
                c = "—"
                d = "—"
                r_val = format_number(approx['r'])
            elif name == 'Квадратичная':
                a = format_number(coeffs[0])
                b = format_number(coeffs[1])
                c = format_number(coeffs[2])
                d = "—"
                r_val = "—"
            elif name == 'Кубическая':
                a = format_number(coeffs[0])
                b = format_number(coeffs[1])
                c = format_number(coeffs[2])
                d = format_number(coeffs[3])
                r_val = "—"
            elif name == 'Экспоненциальная':
                a = format_number(coeffs[0])
                b = format_number(coeffs[1])
                c = "—"
                d = "—"
                r_val = "—"
            elif name == 'Логарифмическая':
                a = format_number(coeffs[0])
                b = format_number(coeffs[1])
                c = "—"
                d = "—"
                r_val = "—"
            elif name == 'Степенная':
                a = format_number(coeffs[0])
                b = format_number(coeffs[1])
                c = "—"
                d = "—"
                r_val = "—"
            else:
                continue

            values = (
                name,
                a,
                b,
                c,
                d,
                format_number(approx['S'], 4),
                format_number(approx['sigma'], 4),
                format_number(approx['R2'], 4),
                r_val
            )

            for col, value in enumerate(values):
                self.labels[row][col].config(text=value)

            # Применяем цвет выделения
            if row in self.selected_rows:
                for label in self.labels[row]:
                    label.configure(bg=SELECTED_BG, fg=SELECTED_FG)



    def _create_table(self):
        """Создание таблицы через Frame + Label."""
        # Заголовки
        for col, text in enumerate(self.headers):
            label = tk.Label(
                self,
                text=text,
                relief=BORDER_RELIEF,
                borderwidth=BORDER_WIDTH,
                bg=HEADER_BG,
                font=FONT_BOLD
            )
            label.grid(row=0, column=col, sticky="nsew", padx=CELL_PAD, pady=CELL_PAD)

        self.rows_count = 6
        self.labels = []

        # Строки с данными
        for row in range(1, self.rows_count + 1):
            row_labels = []
            for col, header in enumerate(self.headers):
                cell_label = tk.Label(
                    self,
                    text="",
                    relief=BORDER_RELIEF,
                    borderwidth=BORDER_WIDTH,
                    bg=CELL_BG,
                    font=FONT_NORMAL,
                    anchor='center'
                )
                cell_label.grid(row=row, column=col, sticky="nsew", padx=CELL_PAD, pady=CELL_PAD)

                # Привязываем клик к ячейке
                cell_label.bind("<Button-1>", lambda e, r=row - 1: self._on_row_click(r))

                row_labels.append(cell_label)

            self.labels.append(row_labels)

        for col, header in enumerate(self.headers):
            self.grid_columnconfigure(col, weight=1 if col > 0 else 0)

        for row in range(self.rows_count + 1):
            self.grid_rowconfigure(row, weight=1)

    def clear(self):
        """Очищает таблицу."""
        self.approximations_data = []
        self.selected_rows.clear()
        for row in range(self.rows_count):
            for col in range(len(self.headers)):
                self.labels[row][col].config(text="", bg=CELL_BG, fg="black")