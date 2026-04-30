def check_uniform_step(x_sorted):
    if len(x_sorted) < 2:
        return False, 0.0
    h = x_sorted[1] - x_sorted[0]
    for i in range(1, len(x_sorted) - 1):
        if abs((x_sorted[i + 1] - x_sorted[i]) - h) > 1e-10:
            return False, h
    return True, h

def finite_differences(y):
    n = len(y)
    table = [y.copy()]
    for order in range(1, n):
        row = []
        for i in range(len(table[order - 1]) - 1):
            row.append(table[order - 1][i + 1] - table[order - 1][i])
        table.append(row)
    return table

def interpolate_forward(x, x_sorted, y_sorted, h):
    n = len(x_sorted)
    table = finite_differences(y_sorted)
    t = (x - x_sorted[0]) / h
    result = table[0][0]
    term = 1.0
    for i in range(1, n):
        term *= (t - i + 1) / i
        if i < len(table[i]):
            result += term * table[i][0]
    return result

def interpolate_backward(x, x_sorted, y_sorted, h):
    n = len(x_sorted)
    table = finite_differences(y_sorted)
    t = (x - x_sorted[-1]) / h
    result = y_sorted[-1]
    term = 1.0
    for i in range(1, n):
        term *= (t + i - 1) / i
        if i < len(table[i]):
            result += term * table[i][-1]
    return result

def interpolate(x, x_sorted, y_sorted):
    is_uniform, h = check_uniform_step(x_sorted)
    if not is_uniform or len(x_sorted) < 2:
        return None
    mid = (x_sorted[0] + x_sorted[-1]) / 2
    if x <= mid:
        return interpolate_forward(x, x_sorted, y_sorted, h)
    else:
        return interpolate_backward(x, x_sorted, y_sorted, h)

def interpolate_line(x_grid, x_sorted, y_sorted):
    result = []
    for x in x_grid:
        y = interpolate(x, x_sorted, y_sorted)
        result.append(y)
    return result