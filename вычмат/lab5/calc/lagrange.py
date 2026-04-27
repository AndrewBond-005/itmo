def interpolate(x, x_sorted, y_sorted):
    """
    Интерполяция многочленом Лагранжа

    Args:
        x: точка, в которой вычисляется значение
        x_sorted: отсортированный список x-координат узлов
        y_sorted: отсортированный список y-координат узлов

    Returns:
        float: интерполированное значение
    """
    n = len(x_sorted)
    result = 0.0

    for i in range(n):
        # Вычисляем базисный полином Лагранжа L_i(x)
        term = y_sorted[i]
        for j in range(n):
            if j != i:
                term *= (x - x_sorted[j]) / (x_sorted[i] - x_sorted[j])
        result += term

    return result