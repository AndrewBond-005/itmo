import tkinter as tk
from tkinter import ttk
import data.core as core
from views.plot.methods_state import methods_state
import calc.lagrange as lagrange
import calc.newton_divided as newton_div
import calc.newton_finite as newton_fin
from views.plot import lines


class ComputeButton(ttk.Button):
    def __init__(self, parent, x_input, message_area, **kwargs):
        super().__init__(parent, text="Вычислить", command=self._compute, **kwargs)
        self.x_input = x_input
        self.message_area = message_area

    def _compute(self):
        # Получаем x
        x = self.x_input.get_value()
        if x is None:
            self.message_area.add_message("Ошибка: x должен быть числом", "error")
            return

        # Получаем отсортированные узлы
        x_sorted, y_sorted = lines.get_sorted_valid_nodes(core)

        if len(x_sorted) < 2:
            self.message_area.add_message("Ошибка: недостаточно точек для интерполяции (требуется ≥2)", "error")
            return

        # Результаты вычислений
        results = {}
        result_str = f"x = {x:.6f}: "
        first = True

        # Лагранж
        if methods_state.is_lagrange_enabled():
            try:
                y = lagrange.interpolate(x, x_sorted, y_sorted)
                results["lagrange"] = y
                result_str += f"Лагранж={y:.6f}"
                first = False
            except Exception as e:
                results["lagrange"] = None
                result_str += f"Лагранж=ошибка"
                first = False

        # Ньютон (разделённые разности)
        if methods_state.is_newton_div_enabled():
            try:
                coeffs = newton_div.build_coefficients(x_sorted, y_sorted)
                y = newton_div.interpolate(x, x_sorted, coeffs)
                results["newton_div"] = y
                if not first:
                    result_str += ", "
                result_str += f"Ньютон(разд)={y:.6f}"
                first = False
            except Exception as e:
                results["newton_div"] = None
                if not first:
                    result_str += ", "
                result_str += f"Ньютон(разд)=ошибка"
                first = False

        # Ньютон (конечные разности) - только при равномерном шаге
        if methods_state.is_newton_fin_enabled():
            is_uniform, h = newton_fin.check_uniform_step(x_sorted)
            if is_uniform:
                try:
                    coeffs = newton_fin.build_coefficients(y_sorted, h)
                    y = newton_fin.interpolate(x, x_sorted, y_sorted, h, coeffs)
                    if y is not None:
                        results["newton_fin"] = y
                        if not first:
                            result_str += ", "
                        result_str += f"Ньютон(кон)={y:.6f}"
                        first = False
                    else:
                        results["newton_fin"] = None
                except Exception as e:
                    results["newton_fin"] = None
            else:
                results["newton_fin"] = None

        # Сохраняем результаты
        core.set_computed_points(x, results)

        # Выводим результат
        self.message_area.add_message(result_str, "info")