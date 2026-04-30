import numpy as np
import calc.lagrange as lagrange
import calc.newton_divided as newton_div
import calc.newton_finite as newton_fin
import calc.bessel as bessel
import calc.stirling as stirling
from utils.const import GRID_POINTS
import math


def build_grid(x_sorted):
    if len(x_sorted) < 2:
        return []

    x_min = min(x_sorted)
    x_max = max(x_sorted)

    # Добавляем небольшой отступ для красоты
    padding = (x_max - x_min) * 0.05
    x_start = x_min - padding
    x_end = x_max + padding

    return np.linspace(x_start, x_end, GRID_POINTS).tolist()


def get_sorted_valid_nodes(core):
    x_list = core.get_x()
    y_list = core.get_y()

    # Собираем только валидные точки (оба значения не None)
    valid = [(x_list[i], y_list[i]) for i in range(len(x_list))
             if x_list[i] is not None and y_list[i] is not None]

    # Сортируем по x
    valid.sort(key=lambda p: p[0])

    # Проверяем на дублирующиеся x
    for i in range(len(valid) - 1):
        if valid[i][0] == valid[i + 1][0]:
            print(f"[Lines] Предупреждение: дублирующиеся x = {valid[i][0]}, интерполяция может быть некорректной")

    if not valid:
        return [], []

    return [p[0] for p in valid], [p[1] for p in valid]


def compute_lagrange_line(x_grid, x_sorted, y_sorted):
    if len(x_sorted) < 2:
        return []
    y_grid = []
    for x in x_grid:
        try:
            y = lagrange.interpolate(x, x_sorted, y_sorted)
            if math.isnan(y):
                y_grid.append(float('nan'))
            else:
                y_grid.append(y)
        except Exception as e:
            print(f"[Lines] Ошибка Лагранжа: {e}")
            y_grid.append(float('nan'))

    return y_grid


def compute_newton_div_line(x_grid, x_sorted, y_sorted):
    if len(x_sorted) < 2:
        return []
    try:
        coeffs = newton_div.build_coefficients(x_sorted, y_sorted)
        if any(math.isnan(c) for c in coeffs):
            return [float('nan')] * len(x_grid)
        y_grid = []
        for x in x_grid:
            y = newton_div.interpolate(x, x_sorted, coeffs)
            if math.isnan(y):
                y_grid.append(float('nan'))
            else:
                y_grid.append(y)
        return y_grid
    except Exception as e:
        print(f"[Lines] Ошибка Ньютона (разд): {e}")
        return [float('nan')] * len(x_grid)


def compute_newton_fin_line(x_grid, x_sorted, y_sorted):
    if len(x_sorted) < 2:
        return []

    is_uniform, _ = newton_fin.check_step(x_sorted)
    if not is_uniform:
        return None

    return newton_fin.interpolate_line(x_grid, x_sorted, y_sorted)


def compute_stirling_line(x_grid, x_sorted, y_sorted):
    if len(x_sorted) < 3:
        return []

    # Проверяем равномерность шага
    is_uniform, h = stirling.is_uniform_step(x_sorted)
    if not is_uniform:
        return None

    y_grid = []
    for x in x_grid:
        try:
            y = stirling.stirling(x, x_sorted, y_sorted, h)
            if y is None or math.isnan(y):
                y_grid.append(float('nan'))
            else:
                y_grid.append(y)
        except:
            y_grid.append(float('nan'))

    return y_grid


def compute_bessel_line(x_grid, x_sorted, y_sorted):
    if len(x_sorted) < 4:
        return []

    # Проверяем равномерность шага
    is_uniform, h = bessel.is_uniform_step(x_sorted)
    if not is_uniform:
        return None

    y_grid = []
    for x in x_grid:
        try:
            y = bessel.bessel(x, x_sorted, y_sorted, h)
            if y is None or math.isnan(y):
                y_grid.append(float('nan'))
            else:
                y_grid.append(y)
        except:
            y_grid.append(float('nan'))

    return y_grid