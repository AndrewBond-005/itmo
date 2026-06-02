import tkinter as tk
from config import COLORS, FONT_TITLE, FONT_TABLE, FONT_HEADER


class AccuracyTab(tk.Frame):

    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg"])
        self.colors = colors
        self._build()

    def _build(self):
        tk.Label(self, text="Оценка точности методов",
                 font=("Segoe UI", 12, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=(12, 4))

        self.acc_frame = tk.Frame(self, bg=self.colors["bg"])
        self.acc_frame.pack(fill="both", expand=True, padx=20, pady=8)

    def clear(self):
        for w in self.acc_frame.winfo_children():
            w.destroy()

    def draw(self, acc_info, eps):
        self.clear()
        parent = self.acc_frame
        tk.Label(parent, text="Результаты оценки точности",
                 font=FONT_TITLE, bg=self.colors["bg"],
                 fg=self.colors["text"]).pack(anchor="w", pady=(0, 12))
        BD = 1
        table_frame = tk.Frame(parent, bg=self.colors["border"])
        table_frame.pack(anchor="w")
        headers = ["Метод", "Max погрешность"]
        col_widths = [18, 20]

        def acc_cell(text, row, col, bg=self.colors["card"], fg=self.colors["text"],
                     font=FONT_TABLE, bold=False, anchor="center"):
            _font = (font[0], font[1], "bold") if bold else font
            frm = tk.Frame(table_frame, bg=self.colors["border"])
            frm.grid(row=row, column=col, padx=BD, pady=BD, sticky="nsew")
            tk.Label(frm, text=text, font=_font, bg=bg, fg=fg,
                     padx=8, pady=5, anchor=anchor,
                     width=col_widths[col]).pack(fill="both", expand=True)
        for c, hdr in enumerate(headers):
            acc_cell(hdr, 0, c, bg=self.colors["card"], fg=self.colors["text"],
                     font=FONT_HEADER, bold=True)
        for r, (name, (max_err, desc)) in enumerate(acc_info.items(), start=1):
            row_bg = self.colors["card"] if r % 2 == 0 else self.colors["bg"]
            acc_cell(name, r, 0, bg=row_bg, fg=self.colors["text"])
            acc_cell(f"{max_err:.2e}", r, 1, bg=row_bg, fg=self.colors["text"])