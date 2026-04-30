import tkinter as tk
from tkinter import ttk
import data.core as core
from views.plot import lines
from utils.const import CLICK_EPSILON, SCROLL_STEP


class ComputeButton(ttk.Button):
    def __init__(self, parent, x_input, message_area, **kwargs):
        super().__init__(parent, text="Вычислить", command=self._compute, **kwargs)
        self.x_input = x_input
        self.message_area = message_area
        self.methods_panel = None

    def set_methods_panel(self, methods_panel):
        self.methods_panel = methods_panel

    def _compute(self):
        # Получаем x
        x = self.x_input.get_value()
        if x is None:
            self.message_area.add_message("Ошибка: x должен быть числом", "error")
            return
        x_sorted, y_sorted = lines.get_sorted_valid_nodes(core)
        if len(x_sorted) < 2:
            self.message_area.add_message("Ошибка: недостаточно точек для интерполяции (требуется ≥2)", "error")
            return
        is_uniform = False
        h = None
        if len(x_sorted) >= 2:
            h = x_sorted[1] - x_sorted[0]
            is_uniform = all(abs(x_sorted[i + 1] - x_sorted[i] - h) < 1e-10 for i in range(len(x_sorted) - 1))

        result_str = f"x = {x:.6f}: "
        first = True
        if self.methods_panel and self.methods_panel.is_enabled("lagrange"):
            try:
                import calc.lagrange as lagrange
                y = lagrange.interpolate(x, x_sorted, y_sorted)
                self.methods_panel.update_value("lagrange", y)
                result_str += f"Лагранж={y:.6f}"
                first = False
            except Exception as e:
                self.methods_panel.update_value("lagrange", None)

        if self.methods_panel and self.methods_panel.is_enabled("newton_div"):
            try:
                import calc.newton_divided as newton_div
                coeffs = newton_div.build_coefficients(x_sorted, y_sorted)
                y = newton_div.interpolate(x, x_sorted, coeffs)
                self.methods_panel.update_value("newton_div", y)
                if not first:
                    result_str += ", "
                result_str += f"Ньютон(разд)={y:.6f}"
                first = False
            except Exception as e:
                self.methods_panel.update_value("newton_div", None)

        if self.methods_panel and self.methods_panel.is_enabled("newton_fin"):
            if is_uniform:
                try:
                    import calc.newton_finite as newton_fin
                    coeffs = newton_fin.build_coefficients(y_sorted, h)
                    y = newton_fin.interpolate(x, x_sorted, y_sorted, h, coeffs)
                    self.methods_panel.update_value("newton_fin", y)
                    if not first:
                        result_str += ", "
                    result_str += f"Ньютон(кон)={y:.6f}"
                    first = False
                except Exception as e:
                    self.methods_panel.update_value("newton_fin", None)
            else:
                self.methods_panel.update_value("newton_fin", None)

        if self.methods_panel and self.methods_panel.is_enabled("stirling"):
            if is_uniform and len(x_sorted) >= 3:
                try:
                    import calc.stirling as stirling
                    y = stirling.stirling(x, x_sorted, y_sorted, h)
                    self.methods_panel.update_value("stirling", y)
                    if not first:
                        result_str += ", "
                    result_str += f"Стирлинг={y:.6f}"
                    first = False
                except Exception as e:
                    self.methods_panel.update_value("stirling", None)
            else:
                self.methods_panel.update_value("stirling", None)

        if self.methods_panel and self.methods_panel.is_enabled("bessel"):
            if is_uniform and len(x_sorted) >= 4:
                try:
                    import calc.bessel as bessel
                    y = bessel.bessel(x, x_sorted, y_sorted, h)
                    self.methods_panel.update_value("bessel", y)
                    if not first:
                        result_str += ", "
                    result_str += f"Бессель={y:.6f}"
                    first = False
                except Exception as e:
                    self.methods_panel.update_value("bessel", None)
            else:
                self.methods_panel.update_value("bessel", None)

        if self.methods_panel:
            results = {
                "lagrange": self.methods_panel.get_row("lagrange").get_value(),
                "newton_div": self.methods_panel.get_row("newton_div").get_value(),
                "newton_fin": self.methods_panel.get_row("newton_fin").get_value(),
                "stirling": self.methods_panel.get_row("stirling").get_value(),
                "bessel": self.methods_panel.get_row("bessel").get_value()
            }
            core.set_computed_points(x, results)
        self.message_area.add_message(result_str, "info")