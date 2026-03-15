from math import *
def f1(x, y):
    return x ** 2 + y ** 2 - 4


def g1(x, y):
    return y - 3 * x ** 2


def f2(x, y):
    return sin(2*x)**2 -cos(x)**2-y


def g2(x, y):
    return -sin(2*x-1)/2-y


def f3(x, y):
    return log(sin(x)+1.01,3)+2-y

def g3(x, y):
    return (9*exp((sin(2*x+4)/2)))/(x+2)-1-y

def dx(f, x, y):
    h = 1e-10
    return (f(x + h, y) - f(x, y)) / h


def dy(f, x, y):
    h = 1e-14
    return (f(x, y + h) - f(x, y)) / h

fs=[[f1,g1],[f2,g2],[f3,g3]]
systems = [
    (f1, g1, "x² + y² = 4, y = 3x²"),
    (f2, g2, "x² - y = 1, x + y² = 3"),
    (f3, g3, "x³ = y, x + y³ = 2")
]