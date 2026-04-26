import tkinter as tk
from tkinter import ttk
from utils.const import TABLE_FONT, FLOAT_FORMAT, DEFAULT_ROWS, DELETE_BUTTON_TEXT
from views.table.clear import ClearAllButton

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

    def _create_table(self):
        # Заголовки
        headers = ["№", "x", "y", ""]
        for col, text in enumerate(headers):
            if col == 3:
                # Кнопка очистки всего в заголовке
                clear_btn = ClearAllButton(self, self.core)
                clear_btn.grid(row=0, column=col, sticky="nsew")
            else:
                label = tk.Label(self, text=text, relief="solid", borderwidth=1,
                                 bg="lightgray", font=('Arial', 9, 'bold'))
                label.grid(row=0, column=col, sticky="nsew")
            self.grid_columnconfigure(col, weight=1 if col < 3 else 0)

        # Строки
        for row in range(1, self.rows_count + 1):
            # Номер
            num_label = tk.Label(self, text=str(row), relief="solid", borderwidth=1,
                                 bg="white", width=4, height=1, font=('Arial', 9))
            num_label.grid(row=row, column=0, sticky="nsew")

            # Entry X
            x_entry = tk.Entry(self, relief="solid", borderwidth=1, justify='center',
                               font=('Arial', 9), width=10)
            x_entry.grid(row=row, column=1, sticky="nsew", padx=0, pady=0)
            x_entry.bind("<FocusOut>", lambda e, r=row: self._validate_entry(r, 1))
            x_entry.bind("<Return>", self._on_enter_pressed)

            # Entry Y
            y_entry = tk.Entry(self, relief="solid", borderwidth=1, justify='center',
                               font=('Arial', 9), width=10)
            y_entry.grid(row=row, column=2, sticky="nsew", padx=0, pady=0)
            y_entry.bind("<FocusOut>", lambda e, r=row: self._validate_entry(r, 2))
            y_entry.bind("<Return>", self._on_enter_pressed)

            # Кнопка удаления строки
            del_btn = tk.Button(self, text=DELETE_BUTTON_TEXT, fg="red", relief="solid",
                                borderwidth=1, bg="white", font=('Arial', 8),
                                command=lambda r=row: self._delete_row(r))
            del_btn.grid(row=row, column=3, sticky="nsew")

            self.entries.append({
                'row': row, 'x_entry': x_entry, 'y_entry': y_entry,
                'num_label': num_label, 'del_btn': del_btn
            })

        for row in range(self.rows_count + 1):
            self.grid_rowconfigure(row, weight=0)
            self.grid_rowconfigure(row, minsize=22)

    def _validate_entry(self, row, col):
        entry = self.grid_slaves(row=row, column=col)[0]
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