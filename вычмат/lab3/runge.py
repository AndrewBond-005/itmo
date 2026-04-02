from rectangle import *
from simpsons import *
from trapezoid import *
from funcs import *
from gap import *


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
        if(n>11*10**5):
            return [None, n,f"Что-то пошло не так, либо метод слишком медленно сходится, "
                            f"либо функция имеет непредвиденный разрыв второго рода на отрезке. "
                    f"лучший результат которого удалось добиться это {I1}"]
def govnokod(mn, f, a, b, n, k, eps):
    ms = [rect, trap, simps]
    if (mn == 0):
        ans=[[],[]]
        for i in range(0, 3):
            res= rounge(ms[mn], f, a, b, n, i / 2, 1+i%2, eps)
            if isinstance(res, list) and len(res) == 2:
                ans[0].append(res[0])
                ans[1].append(res[1])
            else:
                return res
        return ans
    else:
        return rounge(ms[mn], f, a, b, n, 0, k, eps)

def middle(x):
    log10 = np.log10(x)
    return 10 ** (-0.0243637166 * log10 ** 3 +
                  0.2768605689 * log10 ** 2 +
                  1.2160078745 * log10 +
                  -3.6133434187)
def solve(fn, mn, a, b, n, eps):
    methk = [2, 2, 4]
    k = methk[mn]
    f = fs[fn]
    if fn >= 4:
        g = gap(f, a, b)
        if g is not None:
            print("Обнаржуена точка разрыва в ", g)
            ep=10**-4
            if (abs(g - a) <= ep):
                return [None, None, "Функция терпит бесконечный разрыв в точке а, интеграл невычислим"]
            if (abs(g - b) <= ep):
                return [None, None, "Функция терпит бесконечный разрыв в точке b, интеграл невычислим"]
            if (abs(g - b) > ep and abs(g - a) > ep):
                a1 = max(a, g - (b - g))
                b1 = min(b, g + (g - a))
                fa=abs(f(a1))
                fb=abs(f(b1))
                diff = (fa-fb) / max(fa, fb)
                lg=abs(np.log10(fa))
                if diff < max(0.1,0.1 *lg):
                    if(a==a1):
                        return govnokod(mn, f, b1, b, n, k, eps)
                    else:
                        return govnokod(mn, f, a, a1, n, k, eps)
                else:
                    return [None, None, f"Условие симметрии около точки разрыва не выполнено (разница {diff} > {max(0.1,0.1 *lg)}"]
        else:
            return govnokod(mn, f, a, b, n, k, eps)
    else:
        return govnokod(mn, f, a, b, n, k, eps)
