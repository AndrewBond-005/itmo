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


def stirling(x, x_sorted, y_sorted, h):
    """
    Интерполяция по формуле Стирлинга.
    Лучше всего работает для нечётного числа узлов (5, 7, 9...)
    """
    n = len(x_sorted)

    # Проверка условий
    if n < 3:
        return None

    is_uniform, _ = is_uniform_step(x_sorted, h)
    if not is_uniform:
        return None

    # Центральный узел
    mid = n // 2
    x0 = x_sorted[mid]
    t = (x - x0) / h

    # Получаем таблицу разностей
    diffs = finite_differences_table(y_sorted)

    if mid >= len(diffs):
        return None

    # Начальное значение - y0
    result = diffs[mid][0]

    # Максимальный доступный порядок
    max_order = len(diffs[0]) - 1

    # Добавляем члены
    for k in range(1, max_order + 1):
        if k % 2 == 1:  # нечётный порядок
            idx1 = mid - (k + 1) // 2
            idx2 = mid - (k - 1) // 2
            if idx1 >= 0 and idx2 < len(diffs) and idx2 < len(diffs):
                if k < len(diffs[idx1]) and k < len(diffs[idx2]):
                    delta = (diffs[idx1][k] + diffs[idx2][k]) / 2
                    # Полином для нечётного порядка
                    poly = t
                    for j in range(1, (k + 1) // 2):
                        poly *= (t ** 2 - j ** 2)
                    term = poly / math.factorial(k) * delta
                    result += term
                else:
                    break
            else:
                break
        else:  # чётный порядок
            idx = mid - k // 2
            if idx >= 0 and idx < len(diffs):
                if k < len(diffs[idx]):
                    delta = diffs[idx][k]
                    # Полином для чётного порядка
                    poly = t ** 2
                    for j in range(1, k // 2):
                        poly *= (t ** 2 - j ** 2)
                    term = poly / math.factorial(k) * delta
                    result += term
                else:
                    break
            else:
                break

    return result