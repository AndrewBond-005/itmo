import random

from funcs import *

def solve(a,b,eps,f,lam):
    x = (a + b) / 2
    i = 0
    while i <= 2000:
        i += 1
        xn = phi(x,f,lam)
        if abs(f(x)) < eps:
            return xn,i
        if xn < a or xn > b:
            xn = a + (b - a) * random.random()
        x = xn
    return "Метод не сошёлся"


def phi(x, f,lam):
    if df(f,x)<0:
        lam*=-1
    return x + lam * f(x)


def lamd(a, b,f):
    h = (b - a) / 1000
    mxdf = 0
    x = a
    while x <= b:
        try:
            df = abs((f(x + h) - f(x)) / h)
            mxdf = max(mxdf, df)
        except:
            pass
        x += h
    return -1.0 / mxdf


def simple_iteration(f, a, b, eps):
    lam = lamd(a, b,f)
    return solve(a,b,eps,f,lam)
