from funcs import *


def newton(f, g, x, y, eps):
    k=0
    while (True):
        k+=1
        a, b = [dx(f, x, y), dy(f, x, y)]
        c, d = [dx(g, x, y), dy(g, x, y)]
        e, h = [-f(x, y), -g(x, y)]
        ddy = (h - e * c / a) / (d - b * c / a)
        ddx = (e - b *ddy) / a
        x = x + ddx
        y = y + ddy
        if abs(ddx) < eps and abs(ddy) < eps:
            return k,x, y,ddx,ddy
        if(k>500):
            return "метод не сошёлся"

