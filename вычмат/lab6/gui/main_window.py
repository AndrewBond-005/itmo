"""
Главное окно приложения
"""

import tkinter as tk
from tkinter import ttk, messagebox
import traceback

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from config import COLORS, FONT_HEADER
from funcs import ODE_LIST
from methods import NumericalMethods
from accuracy_estimators import AccuracyEstimator
from gui.left_panel import LeftPanel
from gui.table_tab import TableTab
from gui.plot_tab import PlotTab
from gui.accuracy_tab import AccuracyTab


class ODESolverApp(tk.Tk):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()
        self.title("ODE Solver — Численные методы решения ОДУ")
        self.configure(bg=COLORS["bg"])
        self.state("zoomed")
        self.minsize(1100, 700)

        self._build_vars()
        self._build_layout()

    def _build_vars(self):
        self.var_ode = tk.IntVar(value=0)
        self.var_x0 = tk.StringVar(value="0")
        self.var_y0 = tk.StringVar(value="1")
        self.var_xn = tk.StringVar(value="2")
        self.var_h = tk.StringVar(value="0.1")
        self.var_eps = tk.StringVar(value="0.001")

        self.var_euler = tk.BooleanVar(value=True)
        self.var_rk4 = tk.BooleanVar(value=True)
        self.var_adams = tk.BooleanVar(value=True)
        self.var_show_exact = tk.BooleanVar(value=True)

    def _build_layout(self):
        self.paned = tk.PanedWindow(
            self, orient=tk.HORIZONTAL,
            bg=COLORS["bg"], sashwidth=5, sashrelief="flat"
        )
        self.paned.pack(fill="both", expand=True)

        # Левая панель
        self.left_panel = LeftPanel(self.paned, self)
        self.paned.add(self.left_panel, minsize=260)

        # Правая область
        self.right_frame = tk.Frame(self.paned, bg=COLORS["bg"])
        self.paned.add(self.right_frame, minsize=600)

        self._build_notebook()

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

        # Создаём вкладки
        self.table_tab = TableTab(self.notebook, COLORS)
        self.plot_tab = PlotTab(self.notebook, COLORS, self.var_show_exact)
        self.accuracy_tab = AccuracyTab(self.notebook, COLORS)

        self.notebook.add(self.table_tab, text="  Таблица результатов  ")
        self.notebook.add(self.plot_tab, text="  Графики  ")
        self.notebook.add(self.accuracy_tab, text="  Точность  ")

    def get_params(self):
        """Получить параметры из полей ввода"""
        x0 = float(self.var_x0.get().replace(",", "."))
        y0 = float(self.var_y0.get().replace(",", "."))
        xn = float(self.var_xn.get().replace(",", "."))
        h = float(self.var_h.get().replace(",", "."))
        eps = float(self.var_eps.get().replace(",", "."))
        return x0, y0, xn, h, eps

    def get_selected_methods(self):
        """Получить выбранные методы"""
        methods = []
        if self.var_euler.get():
            methods.append("euler")
        if self.var_rk4.get():
            methods.append("rk4")
        if self.var_adams.get():
            methods.append("adams")
        return methods

    def get_selected_ode(self):
        """Получить выбранное ОДУ"""
        return ODE_LIST[self.var_ode.get()]

    def solve(self):
        """Основная логика решения"""
        try:
            x0, y0, xn, h, eps = self.get_params()
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
        if not self.get_selected_methods():
            errors.append("Выберите хотя бы один метод решения")
        if errors:
            messagebox.showerror("Некорректные данные", "\n".join(f"• {e}" for e in errors))
            return

        try:
            ode = self.get_selected_ode()
            f = ode.f
            ex = ode.exact

            results = {}
            acc_info = {}

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
            messagebox.showerror("Ошибка вычислений", traceback.format_exc())
            return

        # Очистка и отрисовка
        self.table_tab.clear()
        self.plot_tab.clear()
        self.accuracy_tab.clear()

        self.table_tab.draw(results, ex, x0, y0)
        self.plot_tab.draw(results, xs_exact, ys_exact, ode.label)
        self.accuracy_tab.draw(acc_info, eps)

        self.left_panel.set_status("Вычисление завершено ✓", COLORS["accent2"])

    def clear(self):
        """Очистить все результаты"""
        self.table_tab.clear()
        self.plot_tab.clear()
        self.accuracy_tab.clear()
        self.left_panel.set_status("Очищено")