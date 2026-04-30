def build_coefficients(x, y):
    n = len(x)
    coef = y.copy()

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])

    return coef


def interpolate(x0, x, coef):
    n = len(x)
    res = coef[0]
    term = 1.0

    for i in range(1, n):
        term *= (x0 - x[i - 1])
        res += coef[i] * term

    return res