import math


def is_uniform_step(x_sorted, h=None):
    """Проверяет равномерность шага"""
    if len(x_sorted) < 2:
        return False, 0.0

    if h is None:
        h = x_sorted[1] - x_sorted[0]

    epsilon = 1e-10
    for i in range(1, len(x_sorted) - 1):
        if abs((x_sorted[i + 1] - x_sorted[i]) - h) > epsilon:
            return False, h
    return True, h


def finite_differences_table(y_sorted):
    """Построение таблицы конечных разностей"""
    n = len(y_sorted)
    if n < 2:
        return []

    table = [[None] * (n - i) for i in range(n)]

    for i in range(n):
        table[i][0] = y_sorted[i]

    for order in range(1, n):
        for i in range(n - order):
            table[i][order] = table[i + 1][order - 1] - table[i][order - 1]

    return table


def stirling_poly_even(t, m):
    """Вычисляет t²·(t²-1²)·(t²-2²)·...·(t²-(m-1)²)"""
    result = t ** 2
    for k in range(1, m):
        result *= (t ** 2 - k ** 2)
    return result


def stirling_poly_odd(t, m):
    """Вычисляет t·(t²-1²)·(t²-2²)·...·(t²-m²)"""
    result = t
    for k in range(1, m + 1):
        result *= (t ** 2 - k ** 2)
    return result


def stirling(x, x_sorted, y_sorted, h):
    """
    Интерполяция по формуле Стирлинга.
    Возвращает float или None (если невозможно вычислить).
    """
    n = len(x_sorted)

    # Проверка условий
    if n < 3:
        return None

    is_uniform, _ = is_uniform_step(x_sorted, h)
    if not is_uniform:
        return None

    # Центральный узел (для нечётного n берём середину, для чётного - левый из центральных)
    mid = n // 2
    x0 = x_sorted[mid]
    t = (x - x0) / h

    # Получаем таблицу разностей
    diffs = finite_differences_table(y_sorted)

    # Проверяем, достаточно ли данных
    if mid >= len(diffs):
        return None

    # Начальное значение - y0
    result = diffs[mid][0]

    # Члены высших порядков
    m = 0
    max_order = len(diffs[0]) - 1

    while True:
        order_odd = 2 * m + 1
        order_even = 2 * m + 2

        # Нечётный член (усреднение разностей)
        if order_odd <= max_order:
            idx1 = mid - m - 1
            idx2 = mid - m
            if idx1 >= 0 and idx2 < len(diffs):
                if order_odd < len(diffs[idx1]) and order_odd < len(diffs[idx2]):
                    delta_odd = (diffs[idx1][order_odd] + diffs[idx2][order_odd]) / 2
                    term_odd = stirling_poly_odd(t, m) / math.factorial(order_odd) * delta_odd
                    result += term_odd
                else:
                    break
            else:
                break
        else:
            break

        # Чётный член
        if order_even <= max_order:
            idx = mid - m - 1
            if idx >= 0:
                if order_even < len(diffs[idx]):
                    delta_even = diffs[idx][order_even]
                    term_even = stirling_poly_even(t, m + 1) / math.factorial(order_even) * delta_even
                    result += term_even
                else:
                    break
            else:
                break
        else:
            break

        m += 1

    return result