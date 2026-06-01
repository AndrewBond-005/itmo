"""
Вкладка с таблицей результатов
"""

import tkinter as tk
from config import COLORS, FONT_TABLE, FONT_HEADER


def _interp(xs, ys, xi):
    """Линейная интерполяция / поиск ближайшего значения"""
    if not xs:
        return float("nan")
    idx = min(range(len(xs)), key=lambda i: abs(xs[i] - xi))
    return ys[idx]


class TableTab(tk.Frame):
    """Вкладка с таблицей результатов"""

    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg"])
        self.colors = colors
        self._build()

    def _build(self):
        tk.Label(self, text="Таблица приближённых значений",
                 font=("Segoe UI", 12, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=(12, 4))

        container = tk.Frame(self, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=12, pady=8)

        vsb = tk.Scrollbar(container, orient="vertical")
        hsb = tk.Scrollbar(container, orient="horizontal")
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        self.table_canvas = tk.Canvas(
            container, bg=self.colors["bg"],
            yscrollcommand=vsb.set, xscrollcommand=hsb.set,
            highlightthickness=0
        )
        self.table_canvas.pack(side="left", fill="both", expand=True)
        vsb.config(command=self.table_canvas.yview)
        hsb.config(command=self.table_canvas.xview)

        self.table_inner = tk.Frame(self.table_canvas, bg=self.colors["bg"])
        self.table_window = self.table_canvas.create_window(
            (0, 0), window=self.table_inner, anchor="nw"
        )
        self.table_inner.bind("<Configure>", self._on_configure)
        self.table_canvas.bind("<Configure>", self._on_canvas_configure)

        self.table_canvas.bind_all("<MouseWheel>",
            lambda e: self.table_canvas.yview_scroll(-1*(e.delta//120), "units"))

    def _on_configure(self, event):
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.table_canvas.itemconfig(self.table_window, width=event.width)

    def clear(self):
        for w in self.table_inner.winfo_children():
            w.destroy()

    def draw(self, results, exact_func, x0, y0):
        self.clear()

        parent = self.table_inner
        col_headers = ["i", "xᵢ"] + \
                      [name for name in results] + \
                      ["Точное решение"] + \
                      [f"|Δ| {name}" for name in results]

        first_method = next(iter(results))
        xs_ref = results[first_method][0]

        COL_W = 13
        PAD_X = 6
        PAD_Y = 4
        BD = 1

        def cell(parent, text, row, col,
                 bg=self.colors["card"], fg=self.colors["text"],
                 font=FONT_TABLE, anchor="center", bold=False):
            _font = (font[0], font[1], "bold") if bold else font
            frm = tk.Frame(parent, bg="#000000")
            frm.grid(row=row, column=col, padx=BD, pady=BD, sticky="nsew")
            lbl = tk.Label(
                frm, text=text, font=_font,
                bg=bg, fg=fg,
                padx=PAD_X, pady=PAD_Y,
                anchor=anchor,
                width=COL_W,
            )
            lbl.pack(fill="both", expand=True)
            return frm

        # заголовки
        for col, hdr in enumerate(col_headers):
            cell(parent, hdr, 0, col,
                 bg=self.colors["card"], fg=self.colors["text"],
                 font=FONT_HEADER, bold=True)

        # данные
        for i, xi in enumerate(xs_ref):
            row_bg = self.colors["card"] if i % 2 == 0 else self.colors["bg"]

            cell(parent, str(i), i + 1, 0, bg=row_bg, fg=self.colors["text"])
            cell(parent, f"{xi:>10.5f}", i + 1, 1, bg=row_bg, fg=self.colors["text"])

            col = 2
            yi_exact = exact_func(xi, xs_ref[0], results[first_method][1][0])

            ys_interp = {}
            for name, (xs, ys) in results.items():
                yi = _interp(xs, ys, xi)
                ys_interp[name] = yi

            for name, yi in ys_interp.items():
                cell(parent, f"{yi:>12.6f}", i + 1, col,
                     bg=row_bg, fg=self.colors["text"])
                col += 1

            cell(parent, f"{yi_exact:>12.6f}", i + 1, col,
                 bg=row_bg, fg=self.colors["text"])
            col += 1

            for name, yi in ys_interp.items():
                err = abs(yi_exact - yi)
                cell(parent, f"{err:.2e}", i + 1, col,
                     bg=row_bg, fg=self.colors["text"])
                col += 1

        parent.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))