"""
Численные методы решения ОДУ
"""

def euler(f, x0, y0, xn, h):
    """
    Явный метод Эйлера: y_{i+1} = y_i + h * f(x_i, y_i)
    Порядок точности: O(h)
    """
    xs, ys = [x0], [y0]
    x, y = x0, y0
    n = max(1, round((xn - x0) / h))
    h = (xn - x0) / n
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys


def runge_kutta4(f, x0, y0, xn, h):
    """
    Классический метод Рунге-Кутты 4-го порядка
    Порядок точности: O(h⁴)
    """
    xs, ys = [x0], [y0]
    x, y = x0, y0
    n = max(1, round((xn - x0) / h))
    h = (xn - x0) / n
    for _ in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f(x + h,   y + k3)
        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys


def adams(f, x0, y0, xn, h):
    """
    Метод Адамса (предиктор-корректор 4-го порядка)
    Первые 3 шага запускаются методом РК4
    """
    n_steps = max(1, round((xn - x0) / h))
    h = (xn - x0) / n_steps

    # стартуем РК4 для получения первых 4 точек
    xs_rk, ys_rk = runge_kutta4(f, x0, y0, x0 + 3*h, h)
    xs = list(xs_rk)
    ys = list(ys_rk)

    if n_steps < 4:
        xs_full, ys_full = runge_kutta4(f, x0, y0, xn, h)
        return xs_full, ys_full

    fs = [f(xs[i], ys[i]) for i in range(4)]

    for i in range(3, n_steps):
        x_i = xs[-1]
        y_i = ys[-1]

        # предиктор
        y_pred = y_i + h/24 * (55*fs[-1] - 59*fs[-2] + 37*fs[-3] - 9*fs[-4])
        x_next = x_i + h
        f_pred = f(x_next, y_pred)

        # корректор
        y_corr = y_i + h/24 * (9*f_pred + 19*fs[-1] - 5*fs[-2] + fs[-3])

        xs.append(x_next)
        ys.append(y_corr)
        fs.append(f(x_next, y_corr))

    return xs, ys