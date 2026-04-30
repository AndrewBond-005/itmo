def is_uniform_step(x):
    if len(x) < 2:
        return False, 0.0
    h = x[1] - x[0]
    for i in range(1, len(x) - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-10:
            return False, h
    return True, h


def finite_differences_table(y_sorted):
    """Построение таблицы конечных разностей"""
    n = len(y_sorted)
    # Создаём пустую таблицу
    table = []
    for i in range(n):
        row = [None] * (n - i)
        table.append(row)
    # Заполняем нулевой столбец (y_i)
    for i in range(n):
        table[i][0] = y_sorted[i]
    # Заполняем остальные столбцы
    for order in range(1, n):
        for i in range(n - order):
            table[i][order] = table[i + 1][order - 1] - table[i][order - 1]

    return table


def stirling(x, x_sorted, y_sorted, h):
    n = len(x_sorted)
    if n < 3:
        return None
    uniform, _ = is_uniform_step(x_sorted)
    if not uniform:
        return None

    table = finite_differences_table(y_sorted)
    mid = n // 2
    x0 = x_sorted[mid]
    t = (x - x0) / h

    result = table[mid][0]
    max_order = len(table[0]) - 1

    for k in range(1, max_order + 1):
        if k % 2 == 1:
            idx1 = mid - (k + 1) // 2
            idx2 = mid - (k - 1) // 2
            if idx1 >= 0 and idx2 >= 0 and k < len(table[idx1]) and k < len(table[idx2]):
                delta = (table[idx1][k] + table[idx2][k]) / 2.0
                term = t
                for j in range(1, (k + 1) // 2):
                    term *= (t * t - j * j)
                for j in range(2, k + 1):
                    term /= j
                result += term * delta
            else:
                break
        else:
            idx = mid - k // 2
            if idx >= 0 and k < len(table[idx]):
                delta = table[idx][k]
                term = 1.0
                for j in range(1, k // 2):
                    term *= (t * t - j * j)
                for j in range(1, k // 2 + 1):
                    term *= (t * t - (j - 1) * (j - 1))
                for j in range(2, k + 1):
                    term /= j
                result += term * delta
            else:
                break

    return result