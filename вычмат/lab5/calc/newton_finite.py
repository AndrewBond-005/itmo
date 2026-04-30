def check_step(x):
    if len(x) < 2:
        return False, 0.0
    h = x[1] - x[0]
    for i in range(1, len(x) - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-10:
            return False, h
    return True, h


def diff(y):
    n = len(y)
    table = [y.copy()]
    for order in range(1, n):
        row = []
        for i in range(len(table[order - 1]) - 1):
            row.append(table[order - 1][i + 1] - table[order - 1][i])
        table.append(row)
    return table


def newton(x0, x, y, h, forward=True):
    n = len(x)
    table = diff(y)
    if forward:
        idx = 0
    else:
        idx = -1
    t = (x0 - x[idx]) / h
    result = table[0][idx]
    term = 1.0
    for i in range(1, n):
        if forward:
            term *= (t - i + 1) / i
        else:
            term *= (t + i - 1) / i

        if i < len(table):
            result += term * table[i][idx]

    return result


def interpolate(x0, x, y):
    is_uniform, h = check_step(x)
    if not is_uniform or len(x) < 2:
        return None
    mid = (x[0] + x[-1]) / 2
    if x0 <= mid:
        return newton(x0, x, y, h,True)
    else:
        return newton(x0, x, y, h,False)


def interpolate_line(x_grid, x, y):
    result = []
    for x0 in x_grid:
        result.append(interpolate(x0, x, y))
    return result