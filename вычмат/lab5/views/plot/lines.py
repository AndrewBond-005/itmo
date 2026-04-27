import numpy as np
import calc.lagrange as lagrange
import calc.newton_divided as newton_div
import calc.newton_finite as newton_fin
from utils.const import GRID_POINTS


def build_grid(x_sorted):
    """
    Создаёт сетку для построения линий от min(x) до max(x)

    Args:
        x_sorted: отсортированный список x-координат узлов

    Returns:
        list: сетка x-координат (200 точек)
    """
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
    """
    Получает отсортированные валидные узлы из core

    Returns:
        tuple: (x_sorted, y_sorted)
    """
    x_list = core.get_x()
    y_list = core.get_y()

    # Собираем только валидные точки (оба значения не None)
    valid = [(x_list[i], y_list[i]) for i in range(len(x_list))
             if x_list[i] is not None and y_list[i] is not None]

    # Сортируем по x
    valid.sort(key=lambda p: p[0])

    if not valid:
        return [], []

    return [p[0] for p in valid], [p[1] for p in valid]


def compute_lagrange_line(x_grid, x_sorted, y_sorted):
    """
    Вычисляет значения интерполяции Лагранжа для сетки

    Returns:
        list: значения y для каждой точки сетки
    """
    if len(x_sorted) < 2:
        return []

    y_grid = []
    for x in x_grid:
        try:
            y = lagrange.interpolate(x, x_sorted, y_sorted)
            y_grid.append(y)
        except:
            y_grid.append(float('nan'))

    return y_grid


def compute_newton_div_line(x_grid, x_sorted, y_sorted):
    """
    Вычисляет значения интерполяции Ньютона (разделённые разности) для сетки

    Returns:
        list: значения y для каждой точки сетки
    """
    if len(x_sorted) < 2:
        return []

    try:
        coeffs = newton_div.build_coefficients(x_sorted, y_sorted)
        y_grid = []
        for x in x_grid:
            y = newton_div.interpolate(x, x_sorted, coeffs)
            y_grid.append(y)
        return y_grid
    except:
        return [float('nan')] * len(x_grid)


def compute_newton_fin_line(x_grid, x_sorted, y_sorted):
    """
    Вычисляет значения интерполяции Ньютона (конечные разности) для сетки

    Returns:
        list: значения y для каждой точки сетки или None если шаг неравномерный
    """
    if len(x_sorted) < 2:
        return []

    # Проверяем равномерность шага
    is_uniform, h = newton_fin.check_uniform_step(x_sorted)

    if not is_uniform:
        print("[Lines] Предупреждение: Шаг неравномерный, интерполяция конечными разностями невозможна")
        return None

    try:
        coeffs = newton_fin.build_coefficients(y_sorted, h)
        y_grid = []
        for x in x_grid:
            y = newton_fin.interpolate(x, x_sorted, y_sorted, h, coeffs)
            if y is None:
                return None
            y_grid.append(y)
        return y_grid
    except:
        return None