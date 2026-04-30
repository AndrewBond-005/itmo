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


def build_forward_coefficients(y_sorted, h):
    """
    Вычисление конечных разностей для интерполяции Ньютона ВПЕРЁД

    Args:
        y_sorted: отсортированный список y-координат узлов
        h: шаг сетки

    Returns:
        list: коэффициенты Δy0, Δ²y0, Δ³y0...
    """
    n = len(y_sorted)
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


def build_backward_coefficients(y_sorted, h):
    """
    Вычисление конечных разностей для интерполяции Ньютона НАЗАД

    Args:
        y_sorted: отсортированный список y-координат узлов
        h: шаг сетки

    Returns:
        list: коэффициенты Δy_{n-1}, Δ²y_{n-2}, Δ³y_{n-3}...
    """
    n = len(y_sorted)

    # Создаём таблицу конечных разностей (обычную)
    diff_table = []
    current = y_sorted.copy()
    diff_table.append(current)

    for order in range(1, n):
        next_row = []
        for i in range(len(current) - 1):
            next_row.append(current[i + 1] - current[i])
        diff_table.append(next_row)
        current = next_row

    # Для формулы назад берём последние элементы каждого порядка
    # Δy_{n-1}, Δ²y_{n-2}, Δ³y_{n-3}...
    coeffs = []
    for order in range(n):
        idx = n - 1 - order
        if idx >= 0 and order < len(diff_table[order]):
            coeffs.append(diff_table[order][idx])
        else:
            coeffs.append(0)

    return coeffs


def interpolate(x, x_sorted, y_sorted, h, coeffs_forward):
    """
    Интерполяция многочленом Ньютона (конечные разности)
    Автоматический выбор формулы вперёд/назад

    Args:
        x: точка, в которой вычисляется значение
        x_sorted: отсортированный список x-координат узлов
        y_sorted: отсортированный список y-координат узлов
        h: шаг сетки
        coeffs_forward: коэффициенты для формулы вперёд

    Returns:
        float: интерполированное значение
    """
    # Проверяем равномерность шага
    is_uniform, _ = check_uniform_step(x_sorted)
    if not is_uniform:
        return None

    n = len(x_sorted)

    # Определяем, где находится x относительно узлов
    # Если x ближе к началу (первая половина) - используем формулу вперёд
    # Если x ближе к концу - используем формулу назад

    x_mid = (x_sorted[0] + x_sorted[-1]) / 2

    if x <= x_mid:
        # Формула Ньютона ВПЕРЁД
        t = (x - x_sorted[0]) / h
        result = coeffs_forward[0]
        term = 1.0

        for i in range(1, n):
            term *= (t - (i - 1)) / i
            result += coeffs_forward[i] * term

        return result
    else:
        # Формула Ньютона НАЗАД
        coeffs_backward = build_backward_coefficients(y_sorted, h)

        t = (x - x_sorted[-1]) / h
        result = coeffs_backward[0]  # это y_{n-1}
        term = 1.0

        for i in range(1, n):
            term *= (t + (i - 1)) / i
            result += coeffs_backward[i] * term

        return result