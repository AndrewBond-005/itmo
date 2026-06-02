import tkinter as tk
from config import COLORS, FONT_TITLE, FONT_TABLE, FONT_HEADER


class AccuracyTab(tk.Frame):

    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg"])
        self.colors = colors
        self._build()

    def _build(self):
        # Верхний заголовок
        tk.Label(self, text="Оценка точности методов",
                 font=("Segoe UI", 12, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=(12, 4))

        # Контейнер с прокруткой для таблицы
        self.canvas_container = tk.Frame(self, bg=self.colors["bg"])
        self.canvas_container.pack(fill="both", expand=True, padx=20, pady=8)

        # Создаём Canvas с прокруткой
        self.canvas = tk.Canvas(self.canvas_container, bg=self.colors["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"])

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Привязываем прокрутку мышью
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    def clear(self):
        """Полная очистка содержимого"""
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw(self, acc_info, eps):
        self.clear()
        if not acc_info:
            tk.Label(self.scrollable_frame, text="Нет данных для отображения",
                     font=FONT_TABLE, bg=self.colors["bg"],
                     fg=self.colors["text_dim"]).pack(pady=20)
            return

        # Заголовок
        title_label = tk.Label(self.scrollable_frame, text="Результаты оценки точности",
                               font=FONT_TITLE, bg=self.colors["bg"],
                               fg=self.colors["text"])
        title_label.pack(anchor="w", pady=(0, 12))

        BD = 1
        table_frame = tk.Frame(self.scrollable_frame, bg=self.colors["border"])
        table_frame.pack(anchor="w", fill="x", pady=5)

        headers = ["Метод", "Max погрешность"]
        col_widths = [18, 20]

        def acc_cell(text, row, col, bg=self.colors["card"], fg=self.colors["text"],
                     font=FONT_TABLE, bold=False, anchor="center"):
            _font = (font[0], font[1], "bold") if bold else font
            frm = tk.Frame(table_frame, bg=self.colors["border"])
            frm.grid(row=row, column=col, padx=BD, pady=BD, sticky="nsew")
            lbl = tk.Label(frm, text=text, font=_font, bg=bg, fg=fg,
                           padx=8, pady=5, anchor=anchor,
                           width=col_widths[col])
            lbl.pack(fill="both", expand=True)
            return frm

        # Заголовки таблицы
        for c, hdr in enumerate(headers):
            acc_cell(hdr, 0, c, bg=self.colors["card"], fg=self.colors["text"],
                     font=FONT_HEADER, bold=True)

        # Данные
        for r, (name, (max_err, desc)) in enumerate(acc_info.items(), start=1):
            row_bg = self.colors["card"] if r % 2 == 0 else self.colors["bg"]
            acc_cell(name, r, 0, bg=row_bg, fg=self.colors["text"])
            acc_cell(f"{max_err:.2e}", r, 1, bg=row_bg, fg=self.colors["text"])

        # Принудительное обновление
        table_frame.update_idletasks()
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

