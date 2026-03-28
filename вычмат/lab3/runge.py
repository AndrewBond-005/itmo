from rectangle import *
from simpsons import *
from trapezoid import *
from funcs import *


def R(I0, I1, k):
    return abs(I1 - I0) / (2 ** k - 1)


def rounge(m, f, a, b, n, h, k, eps):
    I0 = m(f, a, b, n, h)
    while (True):
        n *= 2
        I1 = m(f, a, b, n, h)
        if R(I0, I1, k) < eps:
            return [I1, n]
        else:
            I0 = I1


def solve(f, mn, a, b, n, eps):
    methk = [2, 2, 4]
    ms = [rect, trap, simps]
    ans = []
    k = methk[mn]
    m = []
    if (mn == 0):
        for i in range(0, 3):
            res = rounge(ms[mn], f, a, b, n, i/2, k, eps)
            ans.append(res[0])
            m.append(res[1])
    else:
        res = rounge(ms[mn], f, a, b, n, 0, k, eps)
        ans.append(res[0])
        m.append(res[1])
    return [ans, m]
