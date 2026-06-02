import tkinter as tk
from tkinter import messagebox
from config import COLORS, FONT_TITLE, FONT_LABEL, FONT_ENTRY
from funcs import ODE_LIST


def styled_label(parent, text, font=None, fg=None, bg=None, **kw):
    return tk.Label(
        parent, text=text,
        font=font or FONT_LABEL,
        fg=fg or COLORS["text"],
        bg=bg or COLORS["panel"],
        **kw
    )


def styled_entry(parent, textvariable, width=14):
    return tk.Entry(
        parent,
        textvariable=textvariable,
        font=FONT_ENTRY,
        bg=COLORS["entry_bg"],
        fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["accent"],
        width=width,
    )


def styled_button(parent, text, command, **kw):
    kw.pop('bg', None)
    kw.pop('activebackground', None)
    kw.pop('activeforeground', None)

    btn = tk.Button(
        parent, text=text, command=command,
        font=FONT_TITLE,
        bg=COLORS["accent"],
        fg="#ffffff",
        activebackground="#9b8df9",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=18, pady=8,
        **kw
    )
    return btn


class LeftPanel(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["panel"], width=310)
        self.app = app
        self.pack_propagate(False)
        self._build()

    def _build(self):
        # заголовок
        tk.Label(self, text="Численные методы \nрешения ОДУ",
                 font=("Segoe UI", 16, "bold"),
                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(pady=(20, 2))

        tk.Frame(self, height=1, bg=COLORS["border"]).pack(fill="x", padx=16)

        self._build_ode_selection()
        self._build_input_fields()
        self._build_methods()
        self._build_buttons()

        self.lbl_status = tk.Label(
            self, text="Готов к работе", font=("Segoe UI", 8),
            bg=COLORS["panel"], fg=COLORS["text_dim"], wraplength=270
        )
        self.lbl_status.pack(pady=4, padx=10)

    def _section(self, title):
        tk.Label(
            self, text=title,
            font=FONT_TITLE,
            bg=COLORS["panel"], fg=COLORS["text"],
            anchor="w"
        ).pack(fill="x", padx=16, pady=(10, 4))

    def _build_ode_selection(self):
        self._section("Выберите уравнение")
        for i, ode in enumerate(ODE_LIST):
            rb = tk.Radiobutton(
                self, text=ode.label,
                variable=self.app.var_ode, value=i,
                font=FONT_LABEL,
                bg=COLORS["panel"], fg=COLORS["text"],
                activebackground=COLORS["panel"],
                activeforeground=COLORS["accent"],
                selectcolor=COLORS["card"],
                command=self._on_ode_change,
            )
            rb.pack(anchor="w", padx=24, pady=2)
        self.lbl_eq = tk.Label(
            self, text="", font=("Consolas", 10, "bold"),
            bg=COLORS["card"], fg=COLORS["accent2"],
            relief="flat", pady=6, padx=10
        )
        self.lbl_eq.pack(fill="x", padx=16, pady=(6, 12))
        tk.Frame(self, height=1, bg=COLORS["border"]).pack(fill="x", padx=16)

    def _on_ode_change(self):
        ode = ODE_LIST[self.app.var_ode.get()]
        self.lbl_eq.config(text=f"  {ode.label}")

    def _build_input_fields(self):
        self._section("Исходные данные")
        fields = [
            ("x₀  (начало):", self.app.var_x0),
            ("y₀  (y(x₀)):", self.app.var_y0),
            ("xₙ  (конец):", self.app.var_xn),
            ("h   (шаг):", self.app.var_h),
            ("ε   (точность):", self.app.var_eps),
        ]
        for lbl_text, var in fields:
            row = tk.Frame(self, bg=COLORS["panel"])
            row.pack(fill="x", padx=16, pady=3)
            styled_label(row, lbl_text, width=18, anchor="w").pack(side="left")
            styled_entry(row, var, width=10).pack(side="right")

        tk.Frame(self, height=1, bg=COLORS["border"]).pack(fill="x", padx=16, pady=8)

    def _build_methods(self):
        self._section("Методы решения")
        chk_opts = dict(
            bg=COLORS["panel"], fg=COLORS["text"],
            activebackground=COLORS["panel"],
            activeforeground=COLORS["accent"],
            selectcolor=COLORS["card"],
            font=FONT_LABEL,
        )
        tk.Checkbutton(self, text="Метод Эйлера",
                       variable=self.app.var_euler, **chk_opts).pack(anchor="w", padx=24, pady=2)
        tk.Checkbutton(self, text="Метод Рунге-Кутта 4",
                       variable=self.app.var_rk4, **chk_opts).pack(anchor="w", padx=24, pady=2)
        tk.Checkbutton(self, text="Метод Адамса",
                       variable=self.app.var_adams, **chk_opts).pack(anchor="w", padx=24, pady=2)
        tk.Checkbutton(self, text="Точное решение",
                       variable=self.app.var_show_exact, **chk_opts).pack(anchor="w", padx=24, pady=(8, 2))
        tk.Frame(self, height=1, bg=COLORS["border"]).pack(fill="x", padx=16, pady=8)

    def _build_buttons(self):
        styled_button(self, "▶  Решить", self.app.solve).pack(fill="x", padx=16, pady=(16, 8))
        styled_button(self, "🗑  Очистить", self.app.clear,
                      bg=COLORS["card"], activebackground=COLORS["border"]).pack(
            fill="x", padx=16, pady=(0, 8))

    def set_status(self, msg, color=None):
        self.lbl_status.config(text=msg, fg=color or COLORS["text_dim"])
        self.update_idletasks()