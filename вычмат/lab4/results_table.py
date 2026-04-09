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

# Настройки внешнего вида
ROW_HEIGHT = 25
HEADER_BG = "lightgray"
CELL_BG = "white"
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
        self.labels = []  # Для хранения виджетов ячеек
        self._create_table()

    def _create_table(self):
        """Создание таблицы через Frame + Label (как в DataTable)."""
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

        # Изначально 6 строк (можно настроить)
        self.rows_count = 6

        # Строки с данными
        for row in range(1, self.rows_count + 1):
            row_labels = []
            for col, header in enumerate(self.headers):
                # Создаем Label для каждой ячейки
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
                row_labels.append(cell_label)

            self.labels.append(row_labels)

        # Настройка весов колонок для растягивания
        for col, header in enumerate(self.headers):
            self.grid_columnconfigure(col, weight=1 if col > 0 else 0)

        # Настройка веса для строк
        for row in range(self.rows_count + 1):
            self.grid_rowconfigure(row, weight=1)

    def update_results(self, approximations):
        """
        Заполняет таблицу данными аппроксимаций.
        approximations - список словарей из compute_all_approximations()
        """
        # Очищаем таблицу
        for row in range(self.rows_count):
            for col in range(len(self.headers)):
                self.labels[row][col].config(text="")

        if not approximations:
            return

        # Заполняем данными
        for row, approx in enumerate(approximations):
            if row >= self.rows_count:
                break

            # Извлекаем коэффициенты в зависимости от типа
            name = approx['name']
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

            # Заполняем ячейки строки
            for col, value in enumerate(values):
                self.labels[row][col].config(text=value)

    def clear(self):
        """Очищает таблицу."""
        for row in range(self.rows_count):
            for col in range(len(self.headers)):
                self.labels[row][col].config(text="")