def interpolate(x0, x, y):
    n = len(x)
    res = 0.0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if j != i:
                term *= (x0 - x[j]) / (x[i] - x[j])
        res += term
    return res