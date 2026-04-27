def check_uniform_step(x_sorted):
    """
    Проверка равномерности шага

    Args:
        x_sorted: отсортированный список x-координат узлов

    Returns:
        tuple: (is_uniform, step) - равномерен ли шаг и значение шага
    """
    if len(x_sorted) < 2:
        return False, 0.0

    h = x_sorted[1] - x_sorted[0]
    epsilon = 1e-10

    for i in range(1, len(x_sorted) - 1):
        if abs((x_sorted[i + 1] - x_sorted[i]) - h) > epsilon:
            return False, h

    return True, h


def build_coefficients(y_sorted, h):
    """
    Вычисление конечных разностей для интерполяции Ньютона

    Args:
        y_sorted: отсортированный список y-координат узлов
        h: шаг сетки

    Returns:
        list: коэффициенты (конечные разности ∆y0, ∆²y0, ...)
    """
    n = len(y_sorted)
    # Создаём таблицу конечных разностей
    diff_table = []
    current = y_sorted.copy()
    diff_table.append(current)

    for order in range(1, n):
        next_row = []
        for i in range(len(current) - 1):
            next_row.append(current[i + 1] - current[i])
        diff_table.append(next_row)
        current = next_row

    # Возвращаем первые элементы каждого порядка
    return [diff_table[i][0] for i in range(n)]


def interpolate(x, x_sorted, y_sorted, h, coeffs):
    """
    Интерполяция многочленом Ньютона (конечные разности)

    Args:
        x: точка, в которой вычисляется значение
        x_sorted: отсортированный список x-координат узлов
        y_sorted: отсортированный список y-координат узлов
        h: шаг сетки
        coeffs: коэффициенты (конечные разности)

    Returns:
        float: интерполированное значение или None (если шаг неравномерный)
    """
    # Проверяем равномерность шага
    is_uniform, _ = check_uniform_step(x_sorted)
    if not is_uniform:
        return None

    n = len(x_sorted)

    # Выбираем начальную точку (ближайшую к x)
    if x <= x_sorted[n // 2]:
        # Интерполяция вперёд
        t = (x - x_sorted[0]) / h
        result = coeffs[0]
        term = 1.0
        for i in range(1, n):
            term *= (t - (i - 1)) / i
            result += coeffs[i] * term
    else:
        # Интерполяция назад
        t = (x - x_sorted[-1]) / h
        result = y_sorted[-1]
        term = 1.0

        # Для интерполяции назад нужны конечные разности от конца
        # Пересчитываем таблицу разностей для конца
        y_rev = y_sorted[::-1]
        diff_rev = []
        current = y_rev.copy()
        diff_rev.append(current)

        for order in range(1, n):
            next_row = []
            for i in range(len(current) - 1):
                next_row.append(current[i + 1] - current[i])
            diff_rev.append(next_row)
            current = next_row

        coeffs_rev = [diff_rev[i][0] for i in range(n)]

        for i in range(1, n):
            term *= (t + (i - 1)) / i
            result += coeffs_rev[i] * term

    return result