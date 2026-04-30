def finite_differences_table(y_sorted):
    """
    Построение таблицы конечных разностей

    table[k][i] - разность (k+1)-го порядка для узла i
    """
    n = len(y_sorted)
    table = []
    current = y_sorted.copy()
    table.append(current)

    for order in range(1, n):
        prev = table[order - 1]
        curr = []
        for i in range(len(prev) - 1):
            curr.append(prev[i + 1] - prev[i])
        table.append(curr)

    return table


def divided_differences_table(x_sorted, y_sorted):
    """
    Построение таблицы разделённых разностей

    table[k][i] - разделённая разность (k+1)-го порядка для узла i
    """
    n = len(x_sorted)
    table = []
    current = y_sorted.copy()
    table.append(current)

    for order in range(1, n):
        prev = table[order - 1]
        curr = []
        for i in range(len(prev) - 1):
            denominator = x_sorted[i + order] - x_sorted[i]
            if denominator == 0:
                curr.append(float('nan'))
            else:
                curr.append((prev[i + 1] - prev[i]) / denominator)
        table.append(curr)

    return table