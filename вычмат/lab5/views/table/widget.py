import tkinter as tk
from tkinter import ttk
from utils.const import (
    FLOAT_FORMAT, DEFAULT_ROWS,
    CELL_WIDTH, CELL_HEIGHT, CELL_FONT_SIZE, NUM_COLUMN_WIDTH
)
from views.table.clear import ClearAllButton
from views.table.delete import DeleteButton
from views.table.add import AddRowButton

DATA_CHANGED_EVENT = "<<DataChanged>>"


class DataTable(ttk.Frame):
    def __init__(self, parent, core_module):
        super().__init__(parent)
        self.core = core_module
        self.entries = []
        self._create_table()
        self.core.subscribe(self._refresh_from_core)
        # Инициализируем 10 пустыми строками
        if len(self.core.get_x()) == 0:
            for _ in range(DEFAULT_ROWS):
                self.core.add_point(None, None)
        self._refresh_from_core()
        self.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_table(self):
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(table_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        self._bind_scroll_events(self.canvas)
        self._bind_scroll_events(scrollbar)

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

        self.scrollable_frame.grid_rowconfigure(0, minsize=CELL_HEIGHT)

        self.add_button = AddRowButton(self, self.core, self)
        self.add_button.pack(pady=5)

    def _bind_scroll_events(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel)
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _add_row_widgets(self, row_index, x_val=None, y_val=None):
        row = row_index + 1

        num_label = tk.Label(self.scrollable_frame, text=str(row), relief="solid", borderwidth=1,
                             bg="white", width=NUM_COLUMN_WIDTH, height=1, font=('Arial', CELL_FONT_SIZE))
        num_label.grid(row=row, column=0, sticky="nsew", padx=0, pady=0)

        x_entry = tk.Entry(self.scrollable_frame, relief="solid", borderwidth=1, justify='center',
                           font=('Arial', CELL_FONT_SIZE), width=CELL_WIDTH)
        x_entry.grid(row=row, column=1, sticky="nsew", padx=0, pady=0)
        x_entry.bind("<FocusOut>", lambda e, idx=row_index: self._validate_entry(idx, 0))
        x_entry.bind("<Return>", self._on_enter_pressed)

        y_entry = tk.Entry(self.scrollable_frame, relief="solid", borderwidth=1, justify='center',
                           font=('Arial', CELL_FONT_SIZE), width=CELL_WIDTH)
        y_entry.grid(row=row, column=2, sticky="nsew", padx=0, pady=0)
        y_entry.bind("<FocusOut>", lambda e, idx=row_index: self._validate_entry(idx, 1))
        y_entry.bind("<Return>", self._on_enter_pressed)

        del_btn = DeleteButton(self.scrollable_frame, self.core, row_index)
        del_btn.grid(row=row, column=3, sticky="nsew", padx=0, pady=0)

        if x_val is not None:
            x_entry.insert(0, f"{x_val:.3f}")
        if y_val is not None:
            y_entry.insert(0, f"{y_val:.3f}")

        self.entries.append({
            'row_index': row_index,
            'x_entry': x_entry,
            'y_entry': y_entry,
            'num_label': num_label,
            'del_btn': del_btn
        })

        self.scrollable_frame.grid_rowconfigure(row, minsize=CELL_HEIGHT)

    def _validate_entry(self, row_index, col):
        entry = self.entries[row_index]['x_entry'] if col == 0 else self.entries[row_index]['y_entry']
        val = entry.get().strip().replace(",", ".")
        if val:
            try:
                num = float(val)
                entry.delete(0, tk.END)
                entry.insert(0, f"{num:.3f}")
                if col == 0:
                    self.core.update_x(row_index, num)
                else:
                    self.core.update_y(row_index, num)
            except:
                entry.delete(0, tk.END)
                if col == 0:
                    self.core.update_x(row_index, None)
                else:
                    self.core.update_y(row_index, None)
        else:
            if col == 0:
                self.core.update_x(row_index, None)
            else:
                self.core.update_y(row_index, None)
        self._on_data_changed()

    def _on_enter_pressed(self, event):
        self.focus_set()
        self._on_data_changed()

    def _refresh_from_core(self):
        x_list = self.core.get_x()
        y_list = self.core.get_y()

        for entry in self.entries:
            entry['x_entry'].destroy()
            entry['y_entry'].destroy()
            entry['num_label'].destroy()
            entry['del_btn'].destroy()
        self.entries.clear()

        for i in range(len(x_list)):
            self._add_row_widgets(i, x_list[i], y_list[i])

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