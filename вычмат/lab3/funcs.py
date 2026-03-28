import math
import numpy as np
def f1(x):
    return 3 * math.atan(abs(x + 1)) - 2 + 0.2 * math.sin(4 * (x + 1)) - 0.4 * math.cos(2 * (x + 1))

def f2(x):
    return math.sin(2 * x) ** 2 - math.cos(x) ** 2

def f3(x):
    return math.log(math.sin(x) + 1.06, 3) + 1

def f4(x):
    if(x==0):
        return 0
    return (math.log(abs(x)) * x) * 0.8 - math.sin(4 * x)

fs = [f1,f2,f3,f4]


def F1(x, constant=0):
    sgn = np.sign(x + 1)
    return sgn * ((3*x + 3)*np.arctan(x + 1) - 1.5*np.log(x**2 + 2*x + 2)) - 2*x - 0.2*np.sin(2*x + 2) - 0.05*np.cos(4*x + 4) + constant

def F2(x, constant=0):
    return -np.sin(x) * np.cos(x)**3 + constant

def F3(x, constant=0):
    return x + constant

def F4(x, constant=0):
    x_abs = np.abs(x)
    if x_abs == 0:
        return 0.25 * np.cos(0) + constant
    return x**2 * (0.2 * np.log(x_abs) - 0.2) + 0.25 * np.cos(4 * x) + constant

Fs = [F1,F2,F3,F4]


ms=["Метод прямоуголников", "Метод трапеций","Метод Симпсона"]