import tkinter as tk
from tkinter import ttk
from views.control.method_row import MethodRow
from utils.const import COLOR_LAGRANGE, COLOR_NEWTON_DIV, COLOR_NEWTON_FIN, COLOR_STIRLING, COLOR_BESSEL
import calc.lagrange as lagrange
import calc.newton_divided as newton_div
import calc.newton_finite as newton_fin
import calc.stirling as stirling
import calc.bessel as bessel


class MethodsPanel(ttk.LabelFrame):
    """Панель с вертикальным списком методов и полями вывода"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Методы интерполяции", **kwargs)

        # Словарь для хранения строк методов
        self.method_rows = {}

        # Создаём строки для всех методов
        self.method_rows["lagrange"] = MethodRow(
            self, "Лагранж", COLOR_LAGRANGE, lagrange.interpolate
        )

        self.method_rows["newton_div"] = MethodRow(
            self, "Ньютон (разд)", COLOR_NEWTON_DIV, newton_div.interpolate
        )

        self.method_rows["newton_fin"] = MethodRow(
            self, "Ньютон (кон)", COLOR_NEWTON_FIN, newton_fin.interpolate
        )

        self.method_rows["stirling"] = MethodRow(
            self, "Стирлинг", COLOR_STIRLING, stirling.stirling
        )

        self.method_rows["bessel"] = MethodRow(
            self, "Бессель", COLOR_BESSEL, bessel.bessel
        )

    def is_enabled(self, method_name):
        """Проверяет, включён ли метод"""
        if method_name in self.method_rows:
            return self.method_rows[method_name].is_enabled()
        return False

    def update_value(self, method_name, value):
        """Обновляет значение для метода"""
        if method_name in self.method_rows:
            self.method_rows[method_name].update_value(value)

    def get_all_enabled(self):
        """Возвращает список включённых методов"""
        return [name for name, row in self.method_rows.items() if row.is_enabled()]

    def get_row(self, method_name):
        """Возвращает строку метода"""
        return self.method_rows.get(method_name)