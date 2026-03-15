from cmath import exp, log
from math import *


def f1(x):
    return 2.74 * x ** 3 - 1.93 * x ** 2 - 15.28 * x - 3.72


def f2(x):
    return x ** 3 - 4*x - 2


def f3(x):
    x=x+1
    return exp(2*x)/(x**2)-15

def df3(x):
    return (2*((x+1)**2)*(e**(2*(x+1)))-(2*(x+1))*(e**(2*(x+1)))) / ((x+1)**4)


def f4(x):
    return 2*log(abs(x-0.5)+1,3) -3 *sin(abs(x-0.5))


fs1 = ' 2.74*x**3 - 1.93*x**2 - 15.28*x - 3.72'
fs2 = 'x**3 - 4x - 2'
fs3 = 'exp(2*x)/(x**2)-10'
fs4 = 'log(abs(x)+1,3)/2 -3 *sin(abs(x)+1) +2.5'
fsl = [fs1, fs2, fs3, fs4]

fl = {
    1: f1,
    2: f2,
    3: f3,
    4: f4
}

def df(f,x):
    h = max(1e-8, abs(x) * 1e-8)
    return (f(x + h) - f(x - h)) / (h)