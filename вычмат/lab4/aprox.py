from funcs import *
import math


def linear_approx(x, y, n):
    d = sxx(x) * n - sx(x) * sx(x)
    d1 = sxy(x, y) * n - sx(x) * sx(y)
    d2 = sxx(x) * sx(y) - sx(x) * sxy(x, y)
    a1 = d1 / d
    a2 = d2 / d
    return (a2, a1)


def polinom_approx(x, y, n, nn):
    m = [[0 for i in range(nn)] for j in range(nn)]
    for i in range(0, nn):
        for j in range(0, nn):
            if (i == 0 and j == 0):
                m[i][j] = n;
            else:
                m[i][j] = sxn(x, i + j)
    k = []
    for i in range(0, nn):
        h = []
        for j in range(0, n):
            h.append(y[j] * x[j] ** i)
        k.append(sx(h))
    d = det(m)
    mi = []
    for j in range(nn):
        m0 = [row[:] for row in m]
        for i in range(nn):
            m0[i][j] = k[i]
        mi.append(m0)
    d0 = []
    for i in range(nn):
        d0.append(det(mi[i]) / d)
    return tuple(d0)


def exponential_approx(x, y, n):
    yn = [math.log(y[i]) for i in range(n)]
    a, b = linear_approx(x, yn, n)
    print(a, b)
    print(math.exp(a), b)
    return (math.exp(a), b)


def logarithmic_approx(x, y, n):
    xn = [math.log(x[i]) for i in range(n)]
    a, b = linear_approx(xn, y, n)
    print(a, b)
    return (b, a)


def power_approx(x, y, n):
    yn = [math.log(y[i]) for i in range(n)]
    xn = [math.log(x[i]) for i in range(n)]
    a, b = linear_approx(xn, yn, n)
    print(a, b)
    print(math.exp(a), b)
    return (math.exp(a), b)
