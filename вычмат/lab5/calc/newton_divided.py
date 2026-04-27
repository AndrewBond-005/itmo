def build_coefficients(x_sorted, y_sorted):
    """
    Вычисление разделённых разностей для интерполяции Ньютона

    Args:
        x_sorted: отсортированный список x-координат узлов
        y_sorted: отсортированный список y-координат узлов

    Returns:
        list: коэффициенты (разделённые разности)
    """
    n = len(x_sorted)
    # Создаём таблицу разделённых разностей
    coef = [[0] * n for _ in range(n)]

    # Заполняем нулевой уровень
    for i in range(n):
        coef[i][0] = y_sorted[i]

    # Вычисляем разделённые разности
    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (x_sorted[i + j] - x_sorted[i])

    # Возвращаем первую строку таблицы (коэффициенты многочлена)
    return [coef[0][i] for i in range(n)]


def interpolate(x, x_sorted, coeffs):
    """
    Интерполяция многочленом Ньютона (разделённые разности)

    Args:
        x: точка, в которой вычисляется значение
        x_sorted: отсортированный список x-координат узлов
        coeffs: коэффициенты (разделённые разности)

    Returns:
        float: интерполированное значение
    """
    n = len(x_sorted)
    result = coeffs[0]
    term = 1.0

    for i in range(1, n):
        term *= (x - x_sorted[i - 1])
        result += coeffs[i] * term

    return result