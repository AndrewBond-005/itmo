import tkinter as tk
from tkinter import ttk
from utils.const import (
    FLOAT_FORMAT, DEFAULT_ROWS, DELETE_BUTTON_TEXT,
    CELL_WIDTH, CELL_HEIGHT, CELL_FONT_SIZE, NUM_COLUMN_WIDTH
)
from views.table.clear import ClearAllButton
from views.table.add import AddRowButton

DATA_CHANGED_EVENT = "<<DataChanged>>"


class DataTable(ttk.Frame):
    def __init__(self, parent, core_module, rows=DEFAULT_ROWS):
        super().__init__(parent)
        self.core = core_module
        self.rows_count = rows
        self.entries = []
        self._create_table()
        self.core.subscribe(self._refresh_from_core)
        self._refresh_from_core()

        # ВАЖНО: упаковываем себя в родителя
        self.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_table(self):
        # Контейнер для таблицы
        table_container = ttk.Frame(self)
        table_container.pack(fill=tk.BOTH, expand=True)

        # Холст для прокрутки
        self.canvas = tk.Canvas(table_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        # Заголовки
        headers = ["№", "x", "y", ""]
        for col, text in enumerate(headers):
            if col == 3:
                clear_btn = ClearAllButton(self.scrollable_frame, self.core)
                clear_btn.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
            else:
                label = tk.Label(self.scrollable_frame, text=text, relief="solid", borderwidth=1,
                                 bg="lightgray", font=('Arial', CELL_FONT_SIZE, 'bold'))
                label.grid(row=0, column=col, sticky="nsew", padx=0, pady=0)
            self.scrollable_frame.grid_columnconfigure(col, weight=1 if col < 3 else 0)

        # Строки
        for row in range(1, self.rows_count + 1):
            self._add_row_widgets(row)

        for row in range(self.rows_count + 1):
            self.scrollable_frame.grid_rowconfigure(row, minsize=CELL_HEIGHT)

        # Кнопка добавления строки
        self.add_button = AddRowButton(self, self.core, self)
        self.add_button.pack(pady=5)

    def _add_row_widgets(self, row):
        num_label = tk.Label(self.scrollable_frame, text=str(row), relief="solid", borderwidth=1,
                             bg="white", width=NUM_COLUMN_WIDTH, height=1, font=('Arial', CELL_FONT_SIZE))
        num_label.grid(row=row, column=0, sticky="nsew", padx=0, pady=0)

        x_entry = tk.Entry(self.scrollable_frame, relief="solid", borderwidth=1, justify='center',
                           font=('Arial', CELL_FONT_SIZE), width=CELL_WIDTH)
        x_entry.grid(row=row, column=1, sticky="nsew", padx=0, pady=0)
        x_entry.bind("<FocusOut>", lambda e, r=row: self._validate_entry(r, 1))
        x_entry.bind("<Return>", self._on_enter_pressed)

        y_entry = tk.Entry(self.scrollable_frame, relief="solid", borderwidth=1, justify='center',
                           font=('Arial', CELL_FONT_SIZE), width=CELL_WIDTH)
        y_entry.grid(row=row, column=2, sticky="nsew", padx=0, pady=0)
        y_entry.bind("<FocusOut>", lambda e, r=row: self._validate_entry(r, 2))
        y_entry.bind("<Return>", self._on_enter_pressed)

        del_btn = tk.Button(self.scrollable_frame, text=DELETE_BUTTON_TEXT, fg="red", relief="solid",
                            borderwidth=1, bg="white", font=('Arial', CELL_FONT_SIZE - 1),
                            command=lambda r=row: self._delete_row(r))
        del_btn.grid(row=row, column=3, sticky="nsew", padx=0, pady=0)

        self.entries.append({
            'row': row, 'x_entry': x_entry, 'y_entry': y_entry,
            'num_label': num_label, 'del_btn': del_btn
        })

    def _validate_entry(self, row, col):
        entry = self.scrollable_frame.grid_slaves(row=row, column=col)[0]
        if isinstance(entry, tk.Entry):
            val = entry.get().strip().replace(",", ".")
            if val:
                try:
                    num = float(val)
                    entry.delete(0, tk.END)
                    entry.insert(0, f"{num:.3f}")
                    if col == 1:
                        self.core.update_x(row - 1, num)
                    else:
                        self.core.update_y(row - 1, num)
                except:
                    entry.delete(0, tk.END)
                    if col == 1:
                        self.core.update_x(row - 1, None)
                    else:
                        self.core.update_y(row - 1, None)
            else:
                if col == 1:
                    self.core.update_x(row - 1, None)
                else:
                    self.core.update_y(row - 1, None)
        self._on_data_changed()

    def _on_enter_pressed(self, event):
        self.focus_set()
        self._on_data_changed()

    def _delete_row(self, row):
        self.core.delete_point(row - 1)

    def _refresh_from_core(self):
        x_list = self.core.get_x()
        y_list = self.core.get_y()
        for i in range(self.rows_count):
            if i < len(x_list):
                x_val = x_list[i]
                y_val = y_list[i]
                self.entries[i]['x_entry'].delete(0, tk.END)
                self.entries[i]['y_entry'].delete(0, tk.END)
                if x_val is not None:
                    self.entries[i]['x_entry'].insert(0, f"{x_val:.3f}")
                if y_val is not None:
                    self.entries[i]['y_entry'].insert(0, f"{y_val:.3f}")
            else:
                self.entries[i]['x_entry'].delete(0, tk.END)
                self.entries[i]['y_entry'].delete(0, tk.END)
        self._on_data_changed()

    def _on_data_changed(self, event=None):
        self.event_generate(DATA_CHANGED_EVENT)

    def get_valid_data(self):
        result = []
        for i, entry in enumerate(self.entries):
            x_val = entry['x_entry'].get().strip()
            y_val = entry['y_entry'].get().strip()
            if x_val and y_val:
                try:
                    x = float(x_val.replace(",", "."))
                    y = float(y_val.replace(",", "."))
                    result.append((x, y))
                except:
                    pass
        return result

    def scroll_to_bottom(self):
        self.canvas.yview_moveto(1.0)

    def add_new_row(self):
        self.core.add_point(None, None)
        self.after(100, self.scroll_to_bottom)