def is_uniform_step(x_sorted):
    """Проверяет равномерность шага"""
    if len(x_sorted) < 2:
        return False, 0.0
    h = x_sorted[1] - x_sorted[0]
    for i in range(1, len(x_sorted) - 1):
        diff = x_sorted[i + 1] - x_sorted[i]
        if abs(diff - h) > 1e-10:
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
    """Интерполяция по формуле Стирлинга"""
    n = len(x_sorted)
    # Проверяем условия
    if n < 3:
        return None
    uniform, _ = is_uniform_step(x_sorted)
    if not uniform:
        return None
    # Строим таблицу разностей
    table = finite_differences_table(y_sorted)
    # Находим центральный узел
    mid = n // 2
    x0 = x_sorted[mid]
    t = (x - x0) / h
    # Начинаем с y0
    result = table[mid][0]
    # Добавляем члены для чётных и нечётных порядков
    max_order = len(table[0]) - 1

    for k in range(1, max_order + 1):
        if k % 2 == 1:  # нечётный порядок
            # Берём среднее от двух разностей
            idx1 = mid - (k + 1) // 2
            idx2 = mid - (k - 1) // 2

            if idx1 >= 0 and idx2 >= 0 and k < len(table[idx1]) and k < len(table[idx2]):
                delta = (table[idx1][k] + table[idx2][k]) / 2.0
                # Считаем полином для нечётного порядка
                poly = t
                j = 1
                while j < (k + 1) // 2:
                    poly = poly * (t * t - j * j)
                    j = j + 1
                # Считаем факториал
                fact = 1
                for i in range(2, k + 1):
                    fact = fact * i
                result = result + poly / fact * delta
            else:
                break
        else:  # чётный порядок
            idx = mid - k // 2
            if idx >= 0 and k < len(table[idx]):
                delta = table[idx][k]
                # Считаем полином для чётного порядка
                poly = t * t
                j = 1
                while j < k // 2:
                    poly = poly * (t * t - j * j)
                    j = j + 1
                if k == 2:
                    poly = t * t
                # Считаем факториал
                fact = 1
                for i in range(2, k + 1):
                    fact = fact * i
                result = result + poly / fact * delta
            else:
                break
    return result
