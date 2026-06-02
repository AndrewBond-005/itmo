def init_arrays(x0, y0):
    xs = [x0]
    ys = [y0]
    x = x0
    y = y0
    return xs, ys, x, y

def calculate_steps(x0, xn, h):
    n = max(1, round((xn - x0) / h))
    xh = (xn - x0) / n
    return n, xh

def euler(f, x0, y0, xn, h):
    xs, ys, x, y = init_arrays(x0, y0)
    n, h = calculate_steps(x0, xn, h)
    for i in range(n):
        y = y + h * f(x, y)
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys


def runge_kutta4(f, x0, y0, xn, h):
    xs, ys, x, y = init_arrays(x0, y0)
    n, h = calculate_steps(x0, xn, h)
    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + h
        xs.append(x)
        ys.append(y)
    return xs, ys


def adams(f, x0, y0, xn, h):
    n, h = calculate_steps(x0, xn, h)
    if n < 4:
        return runge_kutta4(f, x0, y0, xn, h)
    xs, ys = runge_kutta4(f, x0, y0, x0 + 3*h, h)
    fs = []
    for i in range(4):
        fs.append(f(xs[i], ys[i]))
    for i in range(3, n):
        x_i = xs[-1]
        y_i = ys[-1]
        y_pred = y_i + h/24 * (55*fs[-1] - 59*fs[-2] + 37*fs[-3] - 9*fs[-4])
        x_next = x_i + h
        f_pred = f(x_next, y_pred)
        y_corr = y_i + h/24 * (9*f_pred + 19*fs[-1] - 5*fs[-2] + fs[-3])
        xs.append(x_next)
        ys.append(y_corr)
        fs.append(f(x_next, y_corr))
    return xs, ys