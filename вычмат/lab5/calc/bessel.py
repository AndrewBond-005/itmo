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


def bessel(x, x_sorted, y_sorted, h):
    """
    Интерполяция по формуле Бесселя.
    Лучше всего работает для чётного числа узлов (4, 6, 8...)
    """
    n = len(x_sorted)

    # Проверка условий
    if n < 4:
        return None

    is_uniform, _ = is_uniform_step(x_sorted, h)
    if not is_uniform:
        return None

    # Для Бесселя берём левый из центральных узлов
    mid = n // 2 - 1
    x0 = x_sorted[mid]
    t = (x - x0) / h

    # Получаем таблицу разностей
    diffs = finite_differences_table(y_sorted)

    if mid + 1 >= len(diffs):
        return None

    # (y0 + y1)/2
    y0 = diffs[mid][0] if mid < len(diffs) else 0
    y1 = diffs[mid + 1][0] if mid + 1 < len(diffs) else 0
    result = (y0 + y1) / 2

    # Член первого порядка
    if mid < len(diffs) and 1 < len(diffs[mid]):
        result += (t - 0.5) * diffs[mid][1]

    # Максимальный доступный порядок
    max_order = len(diffs[0]) - 1

    # Члены высших порядков
    for k in range(2, max_order + 1):
        if k % 2 == 0:  # чётный порядок - с усреднением
            idx = mid - k // 2
            if idx >= 0 and idx + 1 < len(diffs):
                if k < len(diffs[idx]) and k < len(diffs[idx + 1]):
                    delta = (diffs[idx][k] + diffs[idx + 1][k]) / 2

                    # Полином Бесселя
                    poly = 1.0
                    if k == 2:
                        poly = t * (t - 1)
                    else:
                        poly = t * (t - 1)
                        m = 1
                        for j in range(3, k + 1):
                            if j % 2 == 1:
                                poly *= (t - 0.5)
                            else:
                                poly *= (t ** 2 - m ** 2)
                                m += 1

                    term = poly / math.factorial(k) * delta
                    result += term
                else:
                    break
            else:
                break
        else:  # нечётный порядок
            idx = mid - (k - 1) // 2
            if idx >= 0 and idx < len(diffs):
                if k < len(diffs[idx]):
                    delta = diffs[idx][k]

                    # Полином Бесселя
                    poly = 1.0
                    if k == 1:
                        poly = t - 0.5
                    elif k == 3:
                        poly = t * (t - 1) * (t - 0.5)
                    else:
                        poly = t * (t - 1)
                        m = 1
                        for j in range(3, k + 1):
                            if j % 2 == 1:
                                poly *= (t - 0.5)
                            else:
                                poly *= (t ** 2 - m ** 2)
                                m += 1

                    term = poly / math.factorial(k) * delta
                    result += term
                else:
                    break
            else:
                break

    return result