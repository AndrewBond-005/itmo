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
        prev = table[order - 1]
        curr = []
        for i in range(len(prev) - 1):
            curr.append(prev[i + 1] - prev[i])
        table.append(curr)
    return table


def forward(x0, x, y, h):
    n = len(x)
    table = diff(y)
    t = (x0 - x[0]) / h
    result = table[0][0]
    term = 1.0
    for i in range(1, n):
        term *= (t - i + 1) / i
        if i < len(table):
            result += term * table[i][0]
    return result


def backward(x0, x, y, h):
    n = len(x)
    table = diff(y)
    t = (x0 - x[-1]) / h
    result = table[0][-1]
    term = 1.0
    for i in range(1, n):
        term *= (t + i - 1) / i
        if i < len(table) and len(table[i]) > 0:
            result += term * table[i][-1]
    return result


def interpolate(x0, x, y):
    is_uniform, h = check_step(x)
    if not is_uniform or len(x) < 2:
        return None
    mid = (x[0] + x[-1]) / 2
    if x0 <= mid:
        return forward(x0, x, y, h)
    else:
        return backward(x0, x, y, h)


def interpolate_line(x_grid, x, y):
    result = []
    for x0 in x_grid:
        result.append(interpolate(x0, x, y))
    return result