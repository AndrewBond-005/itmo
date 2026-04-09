# Константы таблицы данных
DATA_CHANGED_EVENT = "<<DataChanged>>"
DEFAULT_ROWS = 12

# Настройки внешнего вида
FONT_FAMILY = "Arial"
FONT_SIZE = 10
FONT_BOLD = (FONT_FAMILY, FONT_SIZE, "bold")
FONT_NORMAL = (FONT_FAMILY, FONT_SIZE)

# Размеры
ENTRY_WIDTH = 12
LABEL_WIDTH = 8
BUTTON_WIDTH = 3
ROW_HEIGHT = 25
CELL_PAD_X = 0
CELL_PAD_Y = 0

# Цвета
HEADER_BG = "lightgray"
CELL_BG = "white"
DEL_BUTTON_COLOR = "red"
BORDER_RELIEF = "solid"
BORDER_WIDTH = 1

import tkinter as tk
from tkinter import ttk
from utils import parse_number, format_number


class DataTable(ttk.Frame):
    """Виджет таблицы для ввода координат X и Y."""

    def __init__(self, parent, rows=DEFAULT_ROWS):
        super().__init__(parent)
        self.rows_count = rows
        self.entries = []
        self._create_table()

    def _create_table(self):
        """Создание таблицы через Frame + Entry."""
        # Заголовки
        headers = ["№", "x", "y", "🗑"]
        for col, text in enumerate(headers):
            label = tk.Label(
                self,
                text=text,
                relief=BORDER_RELIEF,
                borderwidth=BORDER_WIDTH,
                bg=HEADER_BG,
                font=FONT_BOLD
            )
            label.grid(row=0, column=col, sticky="nsew")

        # Строки с данными
        for row in range(1, self.rows_count + 1):
            # Номер строки
            num_label = tk.Label(
                self,
                text=str(row),
                relief=BORDER_RELIEF,
                borderwidth=BORDER_WIDTH,
                bg=CELL_BG,
                width=LABEL_WIDTH,
                font=FONT_NORMAL
            )
            num_label.grid(row=row, column=0, sticky="nsew")

            # Entry для X
            x_entry = tk.Entry(
                self,
                relief=BORDER_RELIEF,
                borderwidth=BORDER_WIDTH,
                justify='center',
                bg=CELL_BG,
                font=FONT_NORMAL,
                width=ENTRY_WIDTH
            )
            x_entry.grid(row=row, column=1, sticky="nsew", padx=CELL_PAD_X, pady=CELL_PAD_Y)
            x_entry.bind("<FocusOut>", lambda e, r=row, c=1: self._validate_entry(r, c))
            x_entry.bind("<Return>", self._on_enter_pressed)

            # Entry для Y
            y_entry = tk.Entry(
                self,
                relief=BORDER_RELIEF,
                borderwidth=BORDER_WIDTH,
                justify='center',
                bg=CELL_BG,
                font=FONT_NORMAL,
                width=ENTRY_WIDTH
            )
            y_entry.grid(row=row, column=2, sticky="nsew", padx=CELL_PAD_X, pady=CELL_PAD_Y)
            y_entry.bind("<FocusOut>", lambda e, r=row, c=2: self._validate_entry(r, c))
            y_entry.bind("<Return>", self._on_enter_pressed)

            # Кнопка удаления
            del_btn = tk.Button(
                self,
                text="🗑",
                fg=DEL_BUTTON_COLOR,
                relief=BORDER_RELIEF,
                borderwidth=BORDER_WIDTH,
                bg=CELL_BG,
                font=FONT_NORMAL,
                width=BUTTON_WIDTH,
                command=lambda r=row: self._delete_row(r)
            )
            del_btn.grid(row=row, column=3, sticky="nsew")

            # Сохраняем Entry в список
            self.entries.append({
                'row': row,
                'x_entry': x_entry,
                'y_entry': y_entry,
                'num_label': num_label,
                'del_btn': del_btn
            })

        # Настройка весов колонок для растягивания
        self.grid_columnconfigure(0, weight=0)  # №
        self.grid_columnconfigure(1, weight=1)  # x
        self.grid_columnconfigure(2, weight=1)  # y
        self.grid_columnconfigure(3, weight=0)  # кнопка

        for row in range(self.rows_count + 1):
            self.grid_rowconfigure(row, weight=1)

    def _on_enter_pressed(self, event):
        """Обработка нажатия Enter - убираем фокус с Entry."""
        self.focus_set()
        self._on_data_changed()

    def _validate_entry(self, row, col):
        """Проверяет и форматирует введённое значение."""
        entry_widget = self.grid_slaves(row=row, column=col)[0]
        if isinstance(entry_widget, tk.Entry):
            value = entry_widget.get()
            if value.strip():
                parsed = parse_number(value)
                if parsed is not None:
                    # Форматируем число
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, format_number(parsed))
                else:
                    # Если не число - очищаем
                    entry_widget.delete(0, tk.END)

        self._on_data_changed()

    def _delete_row(self, row):
        """Удаляет данные из строки и сдвигает остальные."""
        # Сдвигаем данные вверх
        for i in range(row, self.rows_count):
            # Получаем значения из следующей строки
            next_x = self.grid_slaves(row=i + 1, column=1)[0].get()
            next_y = self.grid_slaves(row=i + 1, column=2)[0].get()

            # Вставляем в текущую
            self.grid_slaves(row=i, column=1)[0].delete(0, tk.END)
            self.grid_slaves(row=i, column=1)[0].insert(0, next_x)
            self.grid_slaves(row=i, column=2)[0].delete(0, tk.END)
            self.grid_slaves(row=i, column=2)[0].insert(0, next_y)

        # Очищаем последнюю строку
        self.grid_slaves(row=self.rows_count, column=1)[0].delete(0, tk.END)
        self.grid_slaves(row=self.rows_count, column=2)[0].delete(0, tk.END)

        self._on_data_changed()

    def get_valid_data(self):
        """Возвращает список словарей с валидными парами (x, y)."""
        result = []
        for row in range(1, self.rows_count + 1):
            x_widget = self.grid_slaves(row=row, column=1)[0]
            y_widget = self.grid_slaves(row=row, column=2)[0]

            if isinstance(x_widget, tk.Entry) and isinstance(y_widget, tk.Entry):
                x_val = parse_number(x_widget.get())
                y_val = parse_number(y_widget.get())

                if x_val is not None and y_val is not None:
                    result.append({
                        "row": row,
                        "x": x_val,
                        "y": y_val
                    })
        return result

    def get_valid_count(self):
        """Возвращает количество валидных точек."""
        return len(self.get_valid_data())

    def add_point(self, x, y):
        """Добавляет точку в первую свободную строку."""
        for row in range(1, self.rows_count + 1):
            x_widget = self.grid_slaves(row=row, column=1)[0]
            y_widget = self.grid_slaves(row=row, column=2)[0]

            # Проверяем что строка пустая
            if not x_widget.get().strip() and not y_widget.get().strip():
                x_widget.delete(0, tk.END)
                x_widget.insert(0, format_number(x))
                y_widget.delete(0, tk.END)
                y_widget.insert(0, format_number(y))

                # Принудительно обновляем интерфейс
                self.update_idletasks()

                # Генерируем событие
                self._on_data_changed()
                return True
        return False

    def remove_last_point(self):
        """Удаляет последнюю непустую точку."""
        for row in range(self.rows_count, 0, -1):
            x_widget = self.grid_slaves(row=row, column=1)[0]
            y_widget = self.grid_slaves(row=row, column=2)[0]

            x_val = parse_number(x_widget.get())
            y_val = parse_number(y_widget.get())

            if x_val is not None and y_val is not None:
                x_widget.delete(0, tk.END)
                y_widget.delete(0, tk.END)

                # Принудительно обновляем интерфейс
                self.update_idletasks()

                # Генерируем событие
                self._on_data_changed()
                return True
        return False

    def _on_data_changed(self):
        """Генерирует событие об изменении данных."""
        self.update_idletasks()
        self.event_generate(DATA_CHANGED_EVENT)
        self.update_idletasks()