from funcs import *
def gap(f, a, b, n=100000):
    step = (b - a) / n
    prev_x = a
    mx=0
    try:
        prev_y = f(a)
    except:
        return a
    for i in range(1, n):
        x = a + i * step
        try:
            y = f(x)
            if abs(y - prev_y) > 1e5:
                return (prev_x + x) / 2
            if abs(y) > 1e5:
                return x
            prev_y = y
            prev_x = x
        except:
            return x
    return None


