import numpy as np
import calc.lagrange as lagrange
import calc.newton_divided as newton_div
import calc.newton_finite as newton_fin
from utils.const import GRID_POINTS, MIN_GRID_POINTS, MAX_GRID_POINTS, POINTS_PER_UNIT
import math


def build_grid(x_sorted):
    """
    Создаёт сетку для построения линий с динамическим количеством точек
    """
    if len(x_sorted) < 2:
        return []

    x_min = min(x_sorted)
    x_max = max(x_sorted)
    interval_length = x_max - x_min

    points_count = int(interval_length * POINTS_PER_UNIT)
    points_count = max(MIN_GRID_POINTS, min(MAX_GRID_POINTS, points_count))

    padding = interval_length * 0.05
    x_start = x_min - padding
    x_end = x_max + padding

    # Создаём сетку
    grid = np.linspace(x_start, x_end, points_count).tolist()

    # Добавляем все узлы в сетку (чтобы линия точно проходила через них)
    for x in x_sorted:
        # Проверяем с небольшой погрешностью, чтобы не дублировать
        found = False
        for g in grid:
            if abs(g - x) < 1e-10:
                found = True
                break
        if not found:
            grid.append(x)

    # Сортируем сетку
    grid.sort()

    return grid


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


def enforce_nodes(x_grid, y_grid, x_sorted, y_sorted):
    """
    Гарантирует, что линия проходит через узлы интерполяции.
    Если x из сетки совпадает с узлом - заменяем вычисленное значение на точное.
    """
    result = y_grid.copy()

    for i, x in enumerate(x_grid):
        # Ищем, есть ли такой x среди узлов
        for j, x_node in enumerate(x_sorted):
            if abs(x - x_node) < 1e-10:  # с небольшой погрешностью
                result[i] = y_sorted[j]
                break

    return result


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

    # Гарантируем прохождение через узлы
    y_grid = enforce_nodes(x_grid, y_grid, x_sorted, y_sorted)

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

        # Гарантируем прохождение через узлы
        y_grid = enforce_nodes(x_grid, y_grid, x_sorted, y_sorted)

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

    y_grid = newton_fin.interpolate_line(x_grid, x_sorted, y_sorted)

    if y_grid is None:
        return None

    # Гарантируем прохождение через узлы
    y_grid = enforce_nodes(x_grid, y_grid, x_sorted, y_sorted)

    return y_grid