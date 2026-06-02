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
from methods import euler, runge_kutta4, adams
from accuracy_estimators import AccuracyEstimator
from gui.left_panel import LeftPanel
from gui.table_tab import TableTab
from gui.plot_tab import PlotTab
from gui.accuracy_tab import AccuracyTab


class ODESolverApp(tk.Tk):

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
        self.left_panel = LeftPanel(self.paned, self)
        self.paned.add(self.left_panel, minsize=260)
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
        self.table_tab = TableTab(self.notebook, COLORS)
        self.plot_tab = PlotTab(self.notebook, COLORS, self.var_show_exact)
        self.accuracy_tab = AccuracyTab(self.notebook, COLORS)
        self.notebook.add(self.table_tab, text="  Таблица результатов  ")
        self.notebook.add(self.plot_tab, text="  Графики  ")
        self.notebook.add(self.accuracy_tab, text="  Точность  ")

    def get_params(self):
        x0 = float(self.var_x0.get().replace(",", "."))
        y0 = float(self.var_y0.get().replace(",", "."))
        xn = float(self.var_xn.get().replace(",", "."))
        h = float(self.var_h.get().replace(",", "."))
        eps = float(self.var_eps.get().replace(",", "."))
        return x0, y0, xn, h, eps

    def get_selected_methods(self):
        methods = []
        if self.var_euler.get():
            methods.append("euler")
        if self.var_rk4.get():
            methods.append("rk4")
        if self.var_adams.get():
            methods.append("adams")
        return methods

    def get_selected_ode(self):
        return ODE_LIST[self.var_ode.get()]

    def solve(self):
        print("\n" + "=" * 60)
        print("[MAIN] Нажата кнопка Решить")
        print("=" * 60)

        try:
            x0, y0, xn, h, eps = self.get_params()
            print(f"[MAIN] Параметры: x0={x0}, y0={y0}, xn={xn}, h={h}, eps={eps:.2e}")
        except ValueError:
            print("[MAIN] Ошибка ввода чисел")
            messagebox.showerror("Ошибка ввода",
                                 "Все числовые поля должны содержать корректные числа.\n"
                                 "Используйте точку или запятую в качестве десятичного разделителя.")
            return

        errors = []
        if xn <= x0:
            errors.append("xₙ должен быть больше x₀")
        if eps <= 0:
            errors.append("Точность ε должна быть положительной")
        if not self.get_selected_methods():
            errors.append("Выберите хотя бы один метод решения")
        if errors:
            print(f"[MAIN] Ошибки валидации: {errors}")
            messagebox.showerror("Некорректные данные", "\n".join(f"• {e}" for e in errors))
            return

        try:
            ode = self.get_selected_ode()
            f = ode.f
            ex = ode.exact
            print(f"[MAIN] Выбрано ОДУ: {ode.label}")

            results = {}
            acc_info = {}
            h_used = {}

            # Метод Эйлера (p=1) с автоматическим подбором шага
            if self.var_euler.get():
                print("\n[MAIN] --- Запуск метода Эйлера ---")
                xs, ys, final_h, error = AccuracyEstimator.runge_error_with_adaptation(
                    euler, f, x0, y0, xn, eps, p=1, h_start=h
                )
                print(f"[MAIN] Эйлер завершён: h={final_h:.8f}, error={error:.6e}, точек={len(xs)}")
                results["Эйлер"] = (xs, ys)
                acc_info["Эйлер"] = (error, f"правило Рунге (p=1), h={final_h:.6f}")
                h_used["Эйлер"] = final_h

            # Метод Рунге-Кутта 4 (p=4) с автоматическим подбором шага
            if self.var_rk4.get():
                print("\n[MAIN] --- Запуск метода Рунге-Кутта 4 ---")
                xs, ys, final_h, error = AccuracyEstimator.runge_error_with_adaptation(
                    runge_kutta4, f, x0, y0, xn, eps, p=4, h_start=h
                )
                print(f"[MAIN] РК4 завершён: h={final_h:.8f}, error={error:.6e}, точек={len(xs)}")
                results["Рунге-Кутта 4"] = (xs, ys)
                acc_info["Рунге-Кутта 4"] = (error, f"правило Рунге (p=4), h={final_h:.6f}")
                h_used["Рунге-Кутта 4"] = final_h

            # Метод Адамса (многошаговый) — используем сравнение с точным решением
            if self.var_adams.get():
                print("\n[MAIN] --- Запуск метода Адамса ---")
                h_current = h
                error = float('inf')
                xs, ys = [], []
                for iteration in range(10):
                    print(f"[MAIN] Адамс итерация {iteration + 1}/10, h={h_current:.8f}")
                    xs, ys = adams(f, x0, y0, xn, h_current)
                    error = AccuracyEstimator.exact_error(xs, ys, ex, x0, y0)
                    print(f"[MAIN] Адамс error={error:.6e}")
                    if error <= eps or iteration == 9:
                        break
                    h_current = h_current / 2
                    print(f"[MAIN] Уменьшаем h до {h_current:.8f}")
                results["Адамс"] = (xs, ys)
                acc_info["Адамс"] = (error, f"сравнение с точным решением, h={h_current:.6f}")
                h_used["Адамс"] = h_current
                print(f"[MAIN] Адамс завершён: h={h_current:.8f}, error={error:.6e}, точек={len(xs)}")

            # Точное решение на плотной сетке (для красивого графика)
            min_h = min(h_used.values()) if h_used else h
            n_exact = max(200, int((xn - x0) / min_h) * 5)
            print(f"[MAIN] Построение точного решения: {n_exact} точек")
            xs_exact = [x0 + i * (xn - x0) / n_exact for i in range(n_exact + 1)]
            ys_exact = [ex(x, x0, y0) for x in xs_exact]

        except Exception as e:
            print(f"[MAIN] ОШИБКА: {e}")
            traceback.print_exc()
            messagebox.showerror("Ошибка вычислений", traceback.format_exc())
            return

        # Отрисовка результатов
        print("\n[MAIN] Отрисовка результатов...")
        self.table_tab.clear()
        self.plot_tab.clear()
        self.accuracy_tab.clear()

        self.table_tab.draw(results, ex, x0, y0)
        print("[MAIN] Таблица нарисована")

        self.plot_tab.draw(results, xs_exact, ys_exact, ode.label)
        print("[MAIN] График нарисован")
        print(f"[MAIN] acc_info перед отрисовкой: {list(acc_info.keys())}")
        print(f"[MAIN] eps={eps}")
        self.accuracy_tab.draw(acc_info, eps)
        print("[MAIN] Точность нарисована")

        # Статус с информацией о подобранных шагах
        status_msg = "Вычисление завершено ✓ | Шаги: "
        for name, h_val in h_used.items():
            if name == "Эйлер":
                short_name = "Эйлер"
            elif name == "Рунге-Кутта 4":
                short_name = "РК4"
            else:
                short_name = name
            status_msg += f"{short_name}={h_val:.6f} "
        self.left_panel.set_status(status_msg, COLORS["accent2"])
        print(f"[MAIN] {status_msg}")
        print("[MAIN] Готово!\n")

    def clear(self):
        print("[MAIN] Очистка результатов")
        self.table_tab.clear()
        self.plot_tab.clear()
        self.accuracy_tab.clear()
        self.left_panel.set_status("Очищено")

    def show_help(self):
        help_text = """О программе "ODE Solver"

    • Программа решает задачу Коши для обыкновенных дифференциальных уравнений 1-го порядка.
    • Поддерживаемые методы:
       - Метод Эйлера (1-й порядок)
       - Метод Рунге-Кутта 4-го порядка
       - Метод Адамса (предиктор-корректор)

    • Автоматический подбор шага по правилу Рунге для Эйлера и РК4.
    • Оценка погрешности и сравнение с точным решением.
"""

        messagebox.showinfo("Помощь", help_text)

    def quit_app(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти из программы?"):
            self.destroy()