import math
import numpy as np
def f1(x):
    return 3 * math.atan(abs(x + 1)) - 2 + 0.2 * math.sin(4 * (x + 1)) - 0.4 * math.cos(2 * (x + 1))

def f2(x):
    return math.sin(2 * x) ** 2 - math.cos(x) ** 2

def f3(x):
    return np.sin(x) * np.cos(3 * x) + np.sqrt(np.abs(x)) - 1

def f4(x):
    if(x==0):
        return 1
    return (math.log(abs(x)) * x) * 0.8 - math.sin(4 * x)+1

def f5(x):
    return (x + 1) / (x - 1) + math.sin(x - 1) - 1

def f6(x):
    return math.log(abs(x - 1)) - x + 1

def f7(x):
    return 0.5 * (9 * math.exp(math.sin(5*x + 4) / 2) / ((x + 2) ** (1/3)))

fs = [f1,f2,f3,f4,f5,f6,f7]


def F1(x, constant=0):
    sgn = np.sign(x + 1)
    return sgn * ((3*x + 3)*np.arctan(x + 1) - 1.5*np.log(x**2 + 2*x + 2)) - 2*x - 0.2*np.sin(2*x + 2) - 0.05*np.cos(4*x + 4) + constant

def F2(x, constant=0):
    return -np.sin(x) * np.cos(x)**3 + constant

def F3(x, constant=0):
    return (-math.cos(4 * x) / 8 + math.cos(2 * x) / 4 + 2 * x * math.sqrt(abs(x)) / 3 -x +constant)

def F4(x, constant=0):
    if x == 0:
        log_term = 0.0
    else:
        log_term = x ** 2 * math.log(abs(x))

    return (2 * log_term / 5 + math.cos(4 * x) / 4 - x ** 2 / 5 + constant)+x

def F5(x, constant=0):
    return 2* math.log(abs(x - 1)) - math.cos(x - 1)

def F6(x, constant=0):
    return  math.log(abs(x - 1)) * (x - 1) - (x ** 2) / 2


Fs = [F1,F2,F3,F4,F5,F6]

if(len(fs)>len(Fs)):
    k=len(fs)-len(Fs)
    for i in range(1,k+1):
        Fs.append(None)


ms=["Метод прямоуголников", "Метод трапеций","Метод Симпсона"]