import tkinter as tk
from tkinter import ttk
import data.core as core
from func_parser.func_parser import parse_function
from views.plot import lines


class GenerateButton(ttk.Button):
    def __init__(self, parent, func_input, a_input, b_input, n_input, message_area, **kwargs):
        super().__init__(parent, text="Сгенерировать", command=self._generate, **kwargs)
        self.func_input = func_input
        self.a_input = a_input
        self.b_input = b_input
        self.n_input = n_input
        self.message_area = message_area

    def _generate(self):
        # Получаем функцию
        expr = self.func_input.get_value()
        if not expr:
            self.message_area.add_message("Ошибка: введите функцию", "error")
            return

        try:
            f = parse_function(expr)
        except ValueError as e:
            self.message_area.add_message(str(e), "error")
            return

        # Получаем границы
        a = self.a_input.get_value()
        if a is None:
            self.message_area.add_message("Ошибка: a должно быть числом", "error")
            return

        b = self.b_input.get_value()
        if b is None:
            self.message_area.add_message("Ошибка: b должно быть числом", "error")
            return

        if a >= b:
            self.message_area.add_message("Ошибка: a должно быть меньше b", "error")
            return

        # Получаем количество точек
        n = self.n_input.get_value()
        if n is None:
            self.message_area.add_message("Ошибка: n должно быть целым числом", "error")
            return

        if n < 2:
            self.message_area.add_message("Ошибка: n должно быть ≥ 2", "error")
            return

        # Генерируем точки
        step = (b - a) / (n - 1)
        points = []

        for i in range(n):
            x = a + i * step
            try:
                y = f(x)
                if y is not None and not (isinstance(y, complex) or (isinstance(y, float) and (y != y))):
                    points.append((x, y))
                else:
                    self.message_area.add_message(
                        f"Предупреждение: точка x={x:.3f} дала нечисловое значение, пропущена", "warning")
            except Exception as e:
                self.message_area.add_message(f"Ошибка вычисления f({x:.3f}): {e}", "error")
                return

        # БЫСТРОЕ ДОБАВЛЕНИЕ - одним вызовом!
        core.set_points(points)

        self.message_area.add_message(f"Сгенерировано {len(points)} точек из {n} на интервале [{a}, {b}]", "info")