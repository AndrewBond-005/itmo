# Константы таблицы
DATA_CHANGED_EVENT = "<<DataChanged>>"
DEFAULT_ROWS = 12
COLUMNS = ["№", "x", "y", "φ(x)", "ε", ""]
COLUMN_WIDTHS = [50, 100, 100, 100, 100, 60]
LABEL_WIDTH = 8
ENTRY_WIDTH = 12

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
        headers = COLUMNS
        for col, text in enumerate(headers):
            label = tk.Label(
                self,
                text=text,
                relief="solid",
                borderwidth=1,
                bg="lightgray",
                font=('Arial', 10, 'bold')
            )
            label.grid(row=0, column=col, sticky="nsew")
            self.grid_columnconfigure(col, weight=0 if col in [0, 5] else 1)

        # Строки с данными
        for row in range(1, self.rows_count + 1):
            # Номер строки
            num_label = tk.Label(
                self,
                text=str(row),
                relief="solid",
                borderwidth=1,
                bg="white",
                width=LABEL_WIDTH,
                height = 1
            )
            num_label.grid(row=row, column=0, sticky="nsew")

            # Entry для X
            x_entry = tk.Entry(
                self,
                relief="solid",
                borderwidth=1,
                justify='center',
                bg="white",
                width = 12
            )
            x_entry.grid(row=row, column=1, sticky="nsew", padx=0, pady=0)
            x_entry.bind("<FocusOut>", lambda e, r=row, c=1: self._validate_entry(r, c))
            x_entry.bind("<Return>", self._on_enter_pressed)

            # Entry для Y
            y_entry = tk.Entry(
                self,
                relief="solid",
                borderwidth=1,
                justify='center',
                bg="white"
            )
            y_entry.grid(row=row, column=2, sticky="nsew", padx=0, pady=0)
            y_entry.bind("<FocusOut>", lambda e, r=row, c=2: self._validate_entry(r, c))
            y_entry.bind("<Return>", self._on_enter_pressed)

            # Label для φ(x) (только для чтения)
            phi_label = tk.Label(
                self,
                text="",
                relief="solid",
                borderwidth=1,
                bg="#f0f0f0"
            )
            phi_label.grid(row=row, column=3, sticky="nsew")

            # Label для ε (только для чтения)
            eps_label = tk.Label(
                self,
                text="",
                relief="solid",
                borderwidth=1,
                bg="#f0f0f0"
            )
            eps_label.grid(row=row, column=4, sticky="nsew")

            # Кнопка удаления
            del_btn = tk.Button(
                self,
                text="🗑",
                fg="red",
                relief="solid",
                borderwidth=1,
                bg="white",
                command=lambda r=row: self._delete_row(r)
            )
            del_btn.grid(row=row, column=5, sticky="nsew")

            # Сохраняем виджеты в список
            self.entries.append({
                'row': row,
                'x_entry': x_entry,
                'y_entry': y_entry,
                'phi_label': phi_label,
                'eps_label': eps_label,
                'num_label': num_label,
                'del_btn': del_btn
            })

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
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, format_number(parsed))
                else:
                    entry_widget.delete(0, tk.END)

        self._on_data_changed()

    def _delete_row(self, row):
        """Удаляет данные из строки и сдвигает остальные."""
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

        # Очищаем φ(x) и ε
        self.clear_phi_epsilon()

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

    # В класс DataTable добавить:
    def set_row_count(self, new_count):
        """Изменяет количество строк в таблице."""
        current = self.rows_count

        if new_count == current:
            return

        if new_count > current:
            # Добавляем строки
            for row in range(current + 1, new_count + 1):
                self._add_row(row)
        elif new_count < current:
            # Удаляем лишние строки (с конца)
            for row in range(current, new_count, -1):
                self._remove_row(row)

        self.rows_count = new_count
        self._on_data_changed()

    def _add_row(self, row):
        """Добавляет одну строку в таблицу."""
        num_label = tk.Label(
            self,
            text=str(row),
            relief="solid",
            borderwidth=1,
            bg="white",
            width=LABEL_WIDTH
        )
        num_label.grid(row=row, column=0, sticky="nsew")

        x_entry = tk.Entry(
            self,
            relief="solid",
            borderwidth=1,
            justify='center',
            bg="white"
        )
        x_entry.grid(row=row, column=1, sticky="nsew", padx=0, pady=0)
        x_entry.bind("<FocusOut>", lambda e, r=row, c=1: self._validate_entry(r, c))
        x_entry.bind("<Return>", self._on_enter_pressed)

        y_entry = tk.Entry(
            self,
            relief="solid",
            borderwidth=1,
            justify='center',
            bg="white"
        )
        y_entry.grid(row=row, column=2, sticky="nsew", padx=0, pady=0)
        y_entry.bind("<FocusOut>", lambda e, r=row, c=2: self._validate_entry(r, c))
        y_entry.bind("<Return>", self._on_enter_pressed)

        phi_label = tk.Label(
            self,
            text="",
            relief="solid",
            borderwidth=1,
            bg="#f0f0f0"
        )
        phi_label.grid(row=row, column=3, sticky="nsew")

        eps_label = tk.Label(
            self,
            text="",
            relief="solid",
            borderwidth=1,
            bg="#f0f0f0"
        )
        eps_label.grid(row=row, column=4, sticky="nsew")

        del_btn = tk.Button(
            self,
            text="🗑",
            fg="red",
            relief="solid",
            borderwidth=1,
            bg="white",
            command=lambda r=row: self._delete_row(r)
        )
        del_btn.grid(row=row, column=5, sticky="nsew")

        self.entries.append({
            'row': row,
            'x_entry': x_entry,
            'y_entry': y_entry,
            'phi_label': phi_label,
            'eps_label': eps_label,
            'num_label': num_label,
            'del_btn': del_btn
        })

        self.grid_rowconfigure(row, weight=1)

    def _remove_row(self, row):
        """Удаляет одну строку из таблицы."""
        for widget in self.grid_slaves(row=row):
            widget.destroy()

        self.entries = [e for e in self.entries if e['row'] != row]
    def get_valid_rows(self):
        """Возвращает список индексов строк с валидными данными."""
        return [item['row'] for item in self.get_valid_data()]

    def get_valid_count(self):
        """Возвращает количество валидных точек."""
        return len(self.get_valid_data())

    def set_cell_value(self, row, col, value):
        """Устанавливает значение в ячейку."""
        if 1 <= row <= self.rows_count:
            widget = self.grid_slaves(row=row, column=col)[0]
            if isinstance(widget, tk.Label):
                widget.configure(text=str(value))
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, str(value))

    def update_phi_epsilon(self, phi_values, epsilon_values):
        """Обновляет колонки φ(x) и ε для всех валидных строк."""
        valid_rows = self.get_valid_rows()
        for i, row_idx in enumerate(valid_rows):
            if i < len(phi_values):
                self.set_cell_value(row_idx, 3, format_number(phi_values[i]))
            if i < len(epsilon_values):
                self.set_cell_value(row_idx, 4, format_number(epsilon_values[i]))

    def clear_phi_epsilon(self):
        """Очищает φ(x) и ε."""
        for row in range(1, self.rows_count + 1):
            self.set_cell_value(row, 3, "")
            self.set_cell_value(row, 4, "")

    def add_point(self, x, y):
        """Добавляет точку в первую свободную строку."""
        for row in range(1, self.rows_count + 1):
            x_widget = self.grid_slaves(row=row, column=1)[0]
            y_widget = self.grid_slaves(row=row, column=2)[0]

            if not x_widget.get().strip() and not y_widget.get().strip():
                x_widget.delete(0, tk.END)
                x_widget.insert(0, format_number(x))
                y_widget.delete(0, tk.END)
                y_widget.insert(0, format_number(y))
                self.update_idletasks()
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
                self.update_idletasks()
                self._on_data_changed()
                return True
        return False

    def _on_data_changed(self):
        """Генерирует событие об изменении данных."""
        self.update_idletasks()
        self.event_generate(DATA_CHANGED_EVENT)
        self.update_idletasks()

