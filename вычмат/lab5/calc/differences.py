def finite_differences_table(y_sorted):
    """
    Построение таблицы конечных разностей

    Args:
        y_sorted: отсортированный список y-координат узлов

    Returns:
        list: треугольная матрица конечных разностей
    """
    n = len(y_sorted)
    if n < 2:
        return []

    table = [[None] * (n - i) for i in range(n)]

    # Заполняем первый столбец значениями y
    for i in range(n):
        table[i][0] = y_sorted[i]

    # Вычисляем разности
    for order in range(1, n):
        for i in range(n - order):
            table[i][order] = table[i + 1][order - 1] - table[i][order - 1]

    return table


def divided_differences_table(x_sorted, y_sorted):
    """
    Построение таблицы разделённых разностей

    Args:
        x_sorted: отсортированный список x-координат узлов
        y_sorted: отсортированный список y-координат узлов

    Returns:
        list: треугольная матрица разделённых разностей
    """
    n = len(x_sorted)
    if n < 2:
        return []

    table = [[None] * (n - i) for i in range(n)]

    # Заполняем первый столбец значениями y
    for i in range(n):
        table[i][0] = y_sorted[i]

    # Вычисляем разделённые разности
    for order in range(1, n):
        for i in range(n - order):
            j = i + order
            denominator = x_sorted[j] - x_sorted[i]
            if denominator == 0:
                table[i][order] = float('nan')
            else:
                table[i][order] = (table[i + 1][order - 1] - table[i][order - 1]) / denominator

    return table