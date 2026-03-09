def chord(a, b, eps, f):
    xp = a
    k=0
    while True:
        k+=1
        x = a - (b - a) * f(a) / (f(b) - f(a))
        if abs(x - xp) <= eps:
            return x,k
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        xp = x
