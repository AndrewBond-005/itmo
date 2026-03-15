def newton(x0, eps, f):
    x = x0
    k=0
    while True:
        k+=1
        fx = f(x)
        if (abs(fx)<eps):
            return x,k-1
        h = max(1e-8, abs(x) * 1e-8)
        fpx = (f(x + h) - f(x - h)) / (h)
        xn = x - fx / fpx
        if abs(xn - x) < eps:
            return xn,k
        x = xn

