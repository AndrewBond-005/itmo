"""
=============================================================================
  ODE Solver — Решатель обыкновенных дифференциальных уравнений
=============================================================================
  Структура (всё в одном файле, но логически разделено на секции):

  [1] IMPORTS
  [2] ODE DEFINITIONS     — уравнения y' = f(x, y) и их точные решения
  [3] NUMERICAL METHODS   — Эйлер, Рунге-Кутта 4, Адамс (предиктор-корректор)
  [4] ACCURACY ESTIMATORS — правило Рунге, оценка по точному решению
  [5] GUI — главное окно, виджеты, обработчики событий
  [6] ENTRY POINT
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# [1] IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox
import math
import traceback

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


# ─────────────────────────────────────────────────────────────────────────────
# [2] ODE DEFINITIONS
#     Каждое ОДУ: f(x, y) → float
#     Каждое точное решение: exact(x, x0, y0) → float
# ─────────────────────────────────────────────────────────────────────────────

class ODE1:
    """y' = 2"""
    label = "y' = 2"

    @staticmethod
    def f(x: float, y: float) -> float:
        return 2.0

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        return y0 + 2.0 * (x - x0)


class ODE2:
    """y' = 2   (вариант 2 — идентичен по структуре, y0 другая)"""
    label = "y' = 2  (вариант 2)"

    @staticmethod
    def f(x: float, y: float) -> float:
        return 2.0

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        return y0 + 2.0 * (x - x0)


class ODE3:
    """y' = 2   (вариант 3)"""
    label = "y' = 2  (вариант 3)"

    @staticmethod
    def f(x: float, y: float) -> float:
        return 2.0

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        return y0 + 2.0 * (x - x0)


class ODE4:
    """y' = 2   (вариант 4)"""
    label = "y' = 2  (вариант 4)"

    @staticmethod
    def f(x: float, y: float) -> float:
        return 2.0

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        return y0 + 2.0 * (x - x0)


ODE_LIST = [ODE1, ODE2, ODE3, ODE4]


# ─────────────────────────────────────────────────────────────────────────────
# [3] NUMERICAL METHODS
# ─────────────────────────────────────────────────────────────────────────────

class NumericalMethods:
    """
    Три численных метода решения ОДУ y' = f(x, y).
    Все методы принимают:
        f      — правая часть ОДУ
        x0, y0 — начальные условия
        xn     — правая граница
        h      — шаг
    Возвращают: (xs, ys) — списки узлов и значений.
    """

    # ── 3.1 Метод Эйлера ──────────────────────────────────────────────────
    @staticmethod
    def euler(f, x0: float, y0: float, xn: float, h: float):
        """
        Явный метод Эйлера:
            y_{i+1} = y_i + h * f(x_i, y_i)
        """
        xs, ys = [x0], [y0]
        x, y = x0, y0
        n = max(1, round((xn - x0) / h))
        h = (xn - x0) / n          # пересчитываем шаг точно
        for _ in range(n):
            y = y + h * f(x, y)
            x = x + h
            xs.append(x)
            ys.append(y)
        return xs, ys

    # ── 3.2 Метод Рунге-Кутта 4-го порядка ───────────────────────────────
    @staticmethod
    def runge_kutta4(f, x0: float, y0: float, xn: float, h: float):
        """
        Классический РК4:
            k1 = h*f(x,       y)
            k2 = h*f(x+h/2,   y+k1/2)
            k3 = h*f(x+h/2,   y+k2/2)
            k4 = h*f(x+h,     y+k3)
            y_{i+1} = y_i + (k1+2k2+2k3+k4)/6
        """
        xs, ys = [x0], [y0]
        x, y = x0, y0
        n = max(1, round((xn - x0) / h))
        h = (xn - x0) / n
        for _ in range(n):
            k1 = h * f(x,       y)
            k2 = h * f(x + h/2, y + k1/2)
            k3 = h * f(x + h/2, y + k2/2)
            k4 = h * f(x + h,   y + k3)
            y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
            x = x + h
            xs.append(x)
            ys.append(y)
        return xs, ys

    # ── 3.3 Метод Адамса (предиктор-корректор 4-го порядка) ─────────────
    @staticmethod
    def adams(f, x0: float, y0: float, xn: float, h: float):
        """
        Явный метод Адамса–Башфорта–Мултона (4-шаговый предиктор-корректор).

        Предиктор (Адамс-Башфорт 4):
            y*_{n+1} = y_n + h/24*(55f_n - 59f_{n-1} + 37f_{n-2} - 9f_{n-3})

        Корректор (Адамс-Мултон 4):
            y_{n+1}  = y_n + h/24*(9f*_{n+1} + 19f_n - 5f_{n-1} + f_{n-2})

        Первые 3 шага запускаются методом РК4.
        """
        n_steps = max(1, round((xn - x0) / h))
        h = (xn - x0) / n_steps

        # стартуем РК4 для получения первых 4 точек
        xs_rk, ys_rk = NumericalMethods.runge_kutta4(f, x0, y0, x0 + 3*h, h)
        xs = list(xs_rk)
        ys = list(ys_rk)

        if n_steps < 4:
            # слишком мало шагов — возвращаем РК4
            xs_full, ys_full = NumericalMethods.runge_kutta4(f, x0, y0, xn, h)
            return xs_full, ys_full

        fs = [f(xs[i], ys[i]) for i in range(4)]

        for i in range(3, n_steps):
            x_i = xs[-1]
            y_i = ys[-1]

            # предиктор
            y_pred = y_i + h/24 * (
                55*fs[-1] - 59*fs[-2] + 37*fs[-3] - 9*fs[-4]
            )
            x_next = x_i + h
            f_pred = f(x_next, y_pred)

            # корректор
            y_corr = y_i + h/24 * (
                9*f_pred + 19*fs[-1] - 5*fs[-2] + fs[-3]
            )

            xs.append(x_next)
            ys.append(y_corr)
            fs.append(f(x_next, y_corr))

        return xs, ys


# ─────────────────────────────────────────────────────────────────────────────
# [4] ACCURACY ESTIMATORS
# ─────────────────────────────────────────────────────────────────────────────

class AccuracyEstimator:
    """
    Оценка точности:
      - правило Рунге для одношаговых методов (Эйлер, РК4)
      - сравнение с точным решением для многошагового метода (Адамс)
    """

    @staticmethod
    def runge_error(method_func, f, x0, y0, xn, h, p):
        """
        Правило Рунге:
            err_i ≈ |y_h(x_i) - y_{h/2}(x_i)| / (2^p - 1)
        где p — порядок метода.
        Возвращает максимальную погрешность.
        """
        _, ys_h  = method_func(f, x0, y0, xn, h)
        _, ys_h2 = method_func(f, x0, y0, xn, h/2)

        # берём каждую вторую точку мелкой сетки
        ys_h2_coarse = ys_h2[::2]
        n = min(len(ys_h), len(ys_h2_coarse))

        errors = [
            abs(ys_h2_coarse[i] - ys_h[i]) / (2**p - 1)
            for i in range(n)
        ]
        return max(errors) if errors else 0.0

    @staticmethod
    def exact_error(xs, ys, exact_func, x0, y0):
        """
        ε = max|y_i^точн − y_i|  для 0 ≤ i ≤ n
        """
        errors = [abs(exact_func(xs[i], x0, y0) - ys[i]) for i in range(len(xs))]
        return max(errors) if errors else 0.0


# ─────────────────────────────────────────────────────────────────────────────
# [5] GUI
# ─────────────────────────────────────────────────────────────────────────────

# ── Цветовая палитра ─────────────────────────────────────────────────────────
COLORS = {
    "bg":          "#f8f9fa",   # основной фон окна (светлый)
    "panel":       "#ffffff",   # боковая панель (белый)
    "card":        "#f1f3f5",   # карточки (светло-серый)
    "accent":      "#4f8bc9",   # акцент (спокойный синий)
    "accent2":     "#69a84f",   # второй акцент (мягкий зелёный)
    "text":        "#2c3e50",   # основной текст (тёмно-синий)
    "text_dim":    "#6c757d",   # приглушённый текст (серый)
    "entry_bg":    "#ffffff",   # поле ввода (белый)
    "border":      "#000000",   # граница (светло-серый)
    "euler":       "#e67e22",   # цвет Эйлера (мягкий оранжевый)
    "rk4":         "#27ae60",   # цвет РК4 (приглушённый зелёный)
    "adams":       "#8e44ad",   # цвет Адамса (спокойный фиолетовый)
    "exact":       "#2980b9",   # цвет точного решения (глубокий синий)
    "plot_bg":     "#ffffff",   # фон графика (белый)
    "plot_axes":   "#adb5bd",   # оси графика (светло-серый)
    "plot_grid":   "#e9ecef",   # сетка графика (очень светлый)
}

PLOT_COLORS = {
    "Эйлер":           COLORS["euler"],
    "Рунге-Кутта 4":   COLORS["rk4"],
    "Адамс":           COLORS["adams"],
    "Точное решение":  COLORS["exact"],
}

FONT_TITLE   = ("Segoe UI", 13, "bold")
FONT_LABEL   = ("Segoe UI", 12)
FONT_ENTRY   = ("Consolas", 12)
FONT_TABLE   = ("Consolas", 11)
FONT_HEADER  = ("Segoe UI", 12, "bold")
FONT_RESULT  = ("Consolas", 9)


# ── Вспомогательные виджеты ──────────────────────────────────────────────────

def styled_label(parent, text, font=None, fg=None, bg=None, **kw):
    return tk.Label(
        parent, text=text,
        font=font or FONT_LABEL,
        fg=fg   or COLORS["text"],
        bg=bg   or COLORS["panel"],
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
    # Извлекаем конфликтующие параметры из kw
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

# ── Главное окно ─────────────────────────────────────────────────────────────

class ODESolverApp(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()
        self.title("ODE Solver — Численные методы решения ОДУ")
        self.configure(bg=COLORS["bg"])
        self.state("zoomed")          # развернуть на весь экран (Windows)
        self.minsize(1100, 700)

        self._build_vars()
        self._build_layout()
        self._on_ode_change()         # инициализировать лейбл уравнения

    # ── инициализация переменных ─────────────────────────────────────────
    def _build_vars(self):
        self.var_ode  = tk.IntVar(value=0)
        self.var_x0   = tk.StringVar(value="0")
        self.var_y0   = tk.StringVar(value="1")
        self.var_xn   = tk.StringVar(value="2")
        self.var_h    = tk.StringVar(value="0.1")
        self.var_eps  = tk.StringVar(value="0.001")

        self.var_euler = tk.BooleanVar(value=True)
        self.var_rk4   = tk.BooleanVar(value=True)
        self.var_adams = tk.BooleanVar(value=True)
        self.var_show_exact = tk.BooleanVar(value=True)

    # ── компоновка интерфейса ────────────────────────────────────────────
    def _build_layout(self):
        # контейнер: панель слева + рабочая область справа
        self.paned = tk.PanedWindow(
            self, orient=tk.HORIZONTAL,
            bg=COLORS["bg"], sashwidth=5, sashrelief="flat"
        )
        self.paned.pack(fill="both", expand=True)

        # ── Левая панель ─────────────────────────────────────────────────
        self.left_frame = tk.Frame(self.paned, bg=COLORS["panel"], width=310)
        self.left_frame.pack_propagate(False)
        self.paned.add(self.left_frame, minsize=260)

        self._build_left_panel()

        # ── Правая область (notebook с вкладками) ────────────────────────
        self.right_frame = tk.Frame(self.paned, bg=COLORS["bg"])
        self.paned.add(self.right_frame, minsize=600)

        self._build_notebook()

    # ── Левая панель: управление ─────────────────────────────────────────
    def _build_left_panel(self):
        p = self.left_frame

        # заголовок
        tk.Label(p, text="Численные методы \nрешения ОДУ", font=("Segoe UI", 16, "bold"),
                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(pady=(20, 2))

        tk.Frame(p, height=1, bg=COLORS["border"]).pack(fill="x", padx=16)

        # ── Выбор ОДУ ────────────────────────────────────────────────────
        self._section(p, "Выберите уравнение")

        for i, ode in enumerate(ODE_LIST):
            rb = tk.Radiobutton(
                p, text=ode.label,
                variable=self.var_ode, value=i,
                font=FONT_LABEL,
                bg=COLORS["panel"], fg=COLORS["text"],
                activebackground=COLORS["panel"],
                activeforeground=COLORS["accent"],
                selectcolor=COLORS["card"],
                command=self._on_ode_change,
            )
            rb.pack(anchor="w", padx=24, pady=2)

        # текущее уравнение
        self.lbl_eq = tk.Label(
            p, text="", font=("Consolas", 10, "bold"),
            bg=COLORS["card"], fg=COLORS["accent2"],
            relief="flat", pady=6, padx=10
        )
        self.lbl_eq.pack(fill="x", padx=16, pady=(6, 12))

        tk.Frame(p, height=1, bg=COLORS["border"]).pack(fill="x", padx=16)

        # ── Исходные данные ───────────────────────────────────────────────
        self._section(p, "Исходные данные")

        fields = [
            ("x₀  (начало):",  self.var_x0),
            ("y₀  (y(x₀)):",   self.var_y0),
            ("xₙ  (конец):",   self.var_xn),
            ("h   (шаг):",     self.var_h),
            ("ε   (точность):",self.var_eps),
        ]
        for lbl_text, var in fields:
            row = tk.Frame(p, bg=COLORS["panel"])
            row.pack(fill="x", padx=16, pady=3)
            styled_label(row, lbl_text, width=18, anchor="w").pack(side="left")
            styled_entry(row, var, width=10).pack(side="right")

        tk.Frame(p, height=1, bg=COLORS["border"]).pack(fill="x", padx=16, pady=8)

        # ── Методы ───────────────────────────────────────────────────────
        self._section(p, "Методы решения")

        chk_opts = dict(
            bg=COLORS["panel"], fg=COLORS["text"],
            activebackground=COLORS["panel"],
            activeforeground=COLORS["accent"],
            selectcolor=COLORS["card"],
            font=FONT_LABEL,
        )
        tk.Checkbutton(p, text="Метод Эйлера",
                       variable=self.var_euler, **chk_opts).pack(anchor="w", padx=24, pady=2)
        tk.Checkbutton(p, text="Метод Рунге-Кутта 4",
                       variable=self.var_rk4,   **chk_opts).pack(anchor="w", padx=24, pady=2)
        tk.Checkbutton(p, text="Метод Адамса",
                       variable=self.var_adams,  **chk_opts).pack(anchor="w", padx=24, pady=2)
        tk.Checkbutton(p, text="Точное решение",
                       variable=self.var_show_exact, **chk_opts).pack(anchor="w", padx=24, pady=(8, 2))

        tk.Frame(p, height=1, bg=COLORS["border"]).pack(fill="x", padx=16, pady=8)
        # ── Кнопка ───────────────────────────────────────────────────────
        styled_button(p, "▶  Решить", self._solve).pack(
            fill="x", padx=16, pady=(16, 8)
        )
        styled_button(p, "🗑  Очистить", self._clear,
                      bg=COLORS["card"], activebackground=COLORS["border"]).pack(
            fill="x", padx=16, pady=(0, 8)
        )

        # статус
        self.lbl_status = tk.Label(
            p, text="Готов к работе", font=("Segoe UI", 8),
            bg=COLORS["panel"], fg=COLORS["text_dim"], wraplength=270
        )
        self.lbl_status.pack(pady=4, padx=10)

    def _section(self, parent, title):
        tk.Label(
            parent, text=title,
            font=FONT_TITLE,
            bg=COLORS["panel"], fg=COLORS["text"],
            anchor="w"
        ).pack(fill="x", padx=16, pady=(10, 4))

    # ── Правая область: notebook ──────────────────────────────────────────
    def _build_notebook(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TNotebook",
                        background=COLORS["bg"],
                        borderwidth=0)
        style.configure("Custom.TNotebook.Tab",
                        background=COLORS["card"],
                        foreground=COLORS["text"],
                        font=FONT_HEADER,
                        padding=[14, 6])
        style.map("Custom.TNotebook.Tab",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(self.right_frame, style="Custom.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # вкладка таблицы
        self.tab_table = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.tab_table, text="  Таблица результатов  ")

        # вкладка графика
        self.tab_plot = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.tab_plot, text=" Графики  ")

        # вкладка точности
        self.tab_accuracy = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.tab_accuracy, text=" Точность  ")

        self._build_table_tab()
        self._build_plot_tab()
        self._build_accuracy_tab()

    # ── Вкладка «Таблица» ─────────────────────────────────────────────────
    def _build_table_tab(self):
        frame = self.tab_table

        # заголовок вкладки
        tk.Label(frame, text="Таблица приближённых значений",
                 font=("Segoe UI", 12, "bold"),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(12, 4))

        # контейнер с прокруткой
        container = tk.Frame(frame, bg=COLORS["bg"])
        container.pack(fill="both", expand=True, padx=12, pady=8)

        # скроллбары
        vsb = ttk.Scrollbar(container, orient="vertical")
        hsb = ttk.Scrollbar(container, orient="horizontal")
        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")

        # Canvas для таблицы (используем tk.Canvas + Frame внутри)
        self.table_canvas = tk.Canvas(
            container, bg=COLORS["bg"],
            yscrollcommand=vsb.set, xscrollcommand=hsb.set,
            highlightthickness=0
        )
        self.table_canvas.pack(side="left", fill="both", expand=True)
        vsb.config(command=self.table_canvas.yview)
        hsb.config(command=self.table_canvas.xview)

        self.table_inner = tk.Frame(self.table_canvas, bg=COLORS["bg"])
        self.table_window = self.table_canvas.create_window(
            (0, 0), window=self.table_inner, anchor="nw"
        )
        self.table_inner.bind("<Configure>", self._on_table_configure)
        self.table_canvas.bind("<Configure>", self._on_canvas_configure)

        # прокрутка мышью
        self.table_canvas.bind_all("<MouseWheel>",
            lambda e: self.table_canvas.yview_scroll(-1*(e.delta//120), "units"))

    def _on_table_configure(self, event):
        self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")
        )

    def _on_canvas_configure(self, event):
        self.table_canvas.itemconfig(self.table_window, width=event.width)

    # ── Вкладка «Графики» ────────────────────────────────────────────────
    def _build_plot_tab(self):
        frame = self.tab_plot
        self.fig = Figure(figsize=(9, 6), facecolor=COLORS["plot_bg"])
        self.ax  = self.fig.add_subplot(111)
        self._style_ax(self.ax)

        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas_plot.get_tk_widget().pack(fill="both", expand=True)

        toolbar_frame = tk.Frame(frame, bg=COLORS["bg"])
        toolbar_frame.pack(fill="x")
        toolbar = NavigationToolbar2Tk(self.canvas_plot, toolbar_frame)
        toolbar.config(bg=COLORS["bg"])
        toolbar.update()

    def _style_ax(self, ax):
        ax.set_facecolor(COLORS["plot_bg"])
        ax.tick_params(colors=COLORS["text_dim"], labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(COLORS["plot_axes"])
        ax.xaxis.label.set_color(COLORS["text"])
        ax.yaxis.label.set_color(COLORS["text"])
        ax.title.set_color(COLORS["text"])
        ax.grid(True, color=COLORS["plot_grid"], linestyle="--", linewidth=0.7, alpha=0.7)

    # ── Вкладка «Точность» ───────────────────────────────────────────────
    def _build_accuracy_tab(self):
        frame = self.tab_accuracy
        tk.Label(frame, text="Оценка точности методов",
                 font=("Segoe UI", 12, "bold"),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(12, 4))

        self.acc_frame = tk.Frame(frame, bg=COLORS["bg"])
        self.acc_frame.pack(fill="both", expand=True, padx=20, pady=8)

    # ── Обработчики событий ──────────────────────────────────────────────

    def _on_ode_change(self):
        ode = ODE_LIST[self.var_ode.get()]
        self.lbl_eq.config(text=f"  {ode.label}")

    def _set_status(self, msg, color=None):
        self.lbl_status.config(text=msg, fg=color or COLORS["text_dim"])
        self.update_idletasks()

    def _clear(self):
        for w in self.table_inner.winfo_children():
            w.destroy()
        for w in self.acc_frame.winfo_children():
            w.destroy()
        self.ax.clear()
        self._style_ax(self.ax)
        self.canvas_plot.draw()
        self._set_status("Очищено")

    # ── Основная логика: решение ─────────────────────────────────────────

    def _solve(self):
        # ── 1. Парсинг и валидация ввода ──────────────────────────────────
        try:
            x0  = float(self.var_x0.get().replace(",", "."))
            y0  = float(self.var_y0.get().replace(",", "."))
            xn  = float(self.var_xn.get().replace(",", "."))
            h   = float(self.var_h.get().replace(",", "."))
            eps = float(self.var_eps.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка ввода",
                "Все числовые поля должны содержать корректные числа.\n"
                "Используйте точку или запятую в качестве десятичного разделителя.")
            return

        errors = []
        if xn <= x0:
            errors.append("xₙ должен быть больше x₀")
        if h <= 0:
            errors.append("Шаг h должен быть положительным")
        if eps <= 0:
            errors.append("Точность ε должна быть положительной")
        if h >= (xn - x0):
            errors.append("Шаг h должен быть меньше длины интервала (xₙ − x₀)")
        if not (self.var_euler.get() or self.var_rk4.get() or self.var_adams.get()):
            errors.append("Выберите хотя бы один метод решения")
        if errors:
            messagebox.showerror("Некорректные данные", "\n".join(f"• {e}" for e in errors))
            return

        # ── 2. Вычисление ─────────────────────────────────────────────────
        try:
            ode = ODE_LIST[self.var_ode.get()]
            f   = ode.f
            ex  = ode.exact

            results = {}   # method_name → (xs, ys)
            acc_info = {}  # method_name → (max_err, description)

            nm = NumericalMethods

            if self.var_euler.get():
                xs_e, ys_e = nm.euler(f, x0, y0, xn, h)
                results["Эйлер"] = (xs_e, ys_e)
                err_e = AccuracyEstimator.runge_error(nm.euler, f, x0, y0, xn, h, p=1)
                acc_info["Эйлер"] = (err_e, "правило Рунге (p=1)")

            if self.var_rk4.get():
                xs_r, ys_r = nm.runge_kutta4(f, x0, y0, xn, h)
                results["Рунге-Кутта 4"] = (xs_r, ys_r)
                err_r = AccuracyEstimator.runge_error(nm.runge_kutta4, f, x0, y0, xn, h, p=4)
                acc_info["Рунге-Кутта 4"] = (err_r, "правило Рунге (p=4)")

            if self.var_adams.get():
                xs_a, ys_a = nm.adams(f, x0, y0, xn, h)
                results["Адамс"] = (xs_a, ys_a)
                err_a = AccuracyEstimator.exact_error(xs_a, ys_a, ex, x0, y0)
                acc_info["Адамс"] = (err_a, "сравнение с точным решением")

            # точное решение на плотной сетке
            n_exact = max(200, int((xn - x0) / h) * 5)
            xs_exact = [x0 + i*(xn-x0)/n_exact for i in range(n_exact+1)]
            ys_exact = [ex(x, x0, y0) for x in xs_exact]

        except Exception:
            messagebox.showerror("Ошибка вычислений",
                traceback.format_exc())
            return

        self._set_status("Вычисление завершено ✓", COLORS["accent2"])

        # ── 3. Обновление интерфейса ──────────────────────────────────────
        self._clear()
        self._draw_table(results, ex, x0, y0)
        self._draw_plot(results, xs_exact, ys_exact, ode.label)
        self._draw_accuracy(acc_info, eps)

    # ── Отрисовка таблицы ────────────────────────────────────────────────

    def _draw_table(self, results, exact_func, x0, y0):
        parent = self.table_inner

        # заголовки
        col_headers = ["i", "xᵢ"] + \
                      [name for name in results] + \
                      ["Точное решение"] + \
                      [f"|Δ| {name}" for name in results]

        # определяем общую сетку узлов (по первому методу)
        first_method = next(iter(results))
        xs_ref = results[first_method][0]

        # ── рисуем таблицу через grid с border-trick ──────────────────────
        COL_W = 13  # ширина ячейки (символов)
        PAD_X = 6
        PAD_Y = 4
        BD = 1  # толщина бордера

        def cell(parent, text, row, col,
                 bg=COLORS["card"], fg=COLORS["text"],
                 font=FONT_TABLE, anchor="center", bold=False):
            _font = (font[0], font[1], "bold") if bold else font
            frm = tk.Frame(parent, bg=COLORS["border"])
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

        # заголовки (все одного цвета)
        for col, hdr in enumerate(col_headers):
            cell(parent, hdr, 0, col,
                 bg=COLORS["card"], fg=COLORS["text"],
                 font=FONT_HEADER, bold=True)

        # данные
        for i, xi in enumerate(xs_ref):
            row_bg = COLORS["card"] if i % 2 == 0 else COLORS["bg"]

            cell(parent, str(i), i + 1, 0, bg=row_bg, fg=COLORS["text"])
            cell(parent, f"{xi:>10.5f}", i + 1, 1, bg=row_bg, fg=COLORS["text"])

            col = 2
            yi_exact = exact_func(xi, xs_ref[0], results[first_method][1][0])

            ys_interp = {}
            for name, (xs, ys) in results.items():
                yi = _interp(xs, ys, xi)
                ys_interp[name] = yi

            # численные методы (один цвет для всех)
            for name, yi in ys_interp.items():
                cell(parent, f"{yi:>12.6f}", i + 1, col,
                     bg=row_bg, fg=COLORS["text"])
                col += 1

            # точное решение
            cell(parent, f"{yi_exact:>12.6f}", i + 1, col,
                 bg=row_bg, fg=COLORS["text"])
            col += 1

            # погрешности (один цвет для всех)
            for name, yi in ys_interp.items():
                err = abs(yi_exact - yi)
                cell(parent, f"{err:.2e}", i + 1, col,
                     bg=row_bg, fg=COLORS["text"])
                col += 1

        parent.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
    # ── Отрисовка графиков ───────────────────────────────────────────────

    def _draw_plot(self, results, xs_exact, ys_exact, ode_label):
        self.ax.clear()
        self._style_ax(self.ax)

        # Точное решение — только если включено
        if self.var_show_exact.get():
            self.ax.plot(xs_exact, ys_exact,
                         color=COLORS["exact"], linewidth=2.5,
                         label="Точное решение", zorder=5)

        # численные методы
        styles = {"Эйлер": ("-", 1.6), "Рунге-Кутта 4": ("-", 1.6), "Адамс": ("-", 2.0)}
        markers = {"Эйлер": "o", "Рунге-Кутта 4": "o", "Адамс": "o"}

        for name, (xs, ys) in results.items():
            lstyle, lw = styles.get(name, ("-", 1.5))
            mkr = markers.get(name, ".")
            n = len(xs)
            ms = 5 if n <= 30 else (3 if n <= 80 else 0)
            self.ax.plot(
                xs, ys,
                color=PLOT_COLORS.get(name, "#ffffff"),
                linestyle=lstyle, linewidth=lw,
                marker='' if ms > 0 else None, markersize=ms,
                label=name, alpha=0.9, zorder=4
            )
        # marker=mkr
        self.ax.set_title(f"Решение ОДУ: {ode_label}",
                          color=COLORS["text"], fontsize=11, pad=12)
        self.ax.set_xlabel("x", fontsize=10)
        self.ax.set_ylabel("y", fontsize=10)

        # Легенда будет автоматически включать только то, что нарисовано
        if self.ax.get_legend_handles_labels()[0]:  # если есть хоть одна линия
            legend = self.ax.legend(
                facecolor=COLORS["card"],
                edgecolor=COLORS["border"],
                labelcolor=COLORS["text"],
                fontsize=9, loc="best"
            )

        self.fig.tight_layout()
        self.canvas_plot.draw()
    # ── Вкладка точности ─────────────────────────────────────────────────

    def _draw_accuracy(self, acc_info, eps):
        parent = self.acc_frame

        # заголовок
        tk.Label(parent, text="Результаты оценки точности",
                 font=FONT_TITLE, bg=COLORS["bg"],
                 fg=COLORS["text"]).pack(anchor="w", pady=(0, 12))

        BD = 1
        table_frame = tk.Frame(parent, bg=COLORS["border"])
        table_frame.pack(anchor="w")

        headers = ["Метод", "Max погрешность", "Способ оценки", "ε (задано)", "Статус"]
        col_widths = [18, 18, 34, 12, 12]

        def acc_cell(text, row, col, bg=COLORS["card"], fg=COLORS["text"],
                     font=FONT_TABLE, bold=False, anchor="center"):
            _font = (font[0], font[1], "bold") if bold else font
            frm = tk.Frame(table_frame, bg=COLORS["border"])
            frm.grid(row=row, column=col, padx=BD, pady=BD, sticky="nsew")
            tk.Label(frm, text=text, font=_font, bg=bg, fg=fg,
                     padx=8, pady=5, anchor=anchor,
                     width=col_widths[col]).pack(fill="both", expand=True)

        # заголовки
        for c, hdr in enumerate(headers):
            acc_cell(hdr, 0, c, bg=COLORS["card"], fg=COLORS["text"],
                     font=FONT_HEADER, bold=True)

        for r, (name, (max_err, desc)) in enumerate(acc_info.items(), start=1):
            ok = max_err <= eps
            status_text = "✓ OK" if ok else "✗ Превышена"
            row_bg = COLORS["card"] if r % 2 == 0 else COLORS["bg"]

            acc_cell(name, r, 0, bg=row_bg, fg=COLORS["text"])
            acc_cell(f"{max_err:.2e}", r, 1, bg=row_bg, fg=COLORS["text"])
            acc_cell(desc, r, 2, bg=row_bg, fg=COLORS["text_dim"], anchor="w")
            acc_cell(f"{eps:.2e}", r, 3, bg=row_bg, fg=COLORS["text_dim"])
            acc_cell(status_text, r, 4, bg=row_bg, fg=COLORS["text"])  # статус тоже обычный


# ─────────────────────────────────────────────────────────────────────────────
# Вспомогательные функции (модуль-уровень)
# ─────────────────────────────────────────────────────────────────────────────

def _interp(xs, ys, xi):
    """Линейная интерполяция / поиск ближайшего значения."""
    if not xs:
        return float("nan")
    # найдём ближайший индекс
    idx = min(range(len(xs)), key=lambda i: abs(xs[i] - xi))
    return ys[idx]


# ─────────────────────────────────────────────────────────────────────────────
# [6] ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ODESolverApp()
    app.mainloop()
