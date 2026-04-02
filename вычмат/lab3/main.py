import sys

from rectangle import *
from enter import *
from funcs import *
from runge import *



def help():
    print("Инструкция по использованию программы численного интегрирования:")
    print("Данные вводятся в следующем порядке:")
    print("   - Номер функции (от 1 до 7)")
    print("   - Номер метода (1 - прямоугольники, 2 - трапеции, 3 - Симпсона)")
    print("   - Границы интегрирования (два числа через пробел)")
    print("   - Точность вычислений (положительное число)")
    print("В любой момент вместо числа можно ввести \"exit\" для выхода")
    print("Метод прямоугольников выдаёт три результата: левые, средние и правые")
    print("Методы трапеций и Симпсона выдают один результат")
    print("Для оценки погрешности используется правило Рунге")
    print("Список функций и их точки разрыва:")
    print("   f1(x) = 3*atan|x+1| - 2 + 0.2*sin(4(x+1)) - 0.4*cos(2(x+1))")
    print("   f2(x) = sin²(2x) - cos²(x)")
    print("   f3(x) = sin(x)*cos(3x) + √|x| - 1")
    print("   f4(x) = 0.8*|x|*ln|x| - sin(4x) + 1")
    print("   f5(x) = (x+1)/(x-1) + sin(x-1) - 1            — разрыв в x = 1, симметричная")
    print("   f6(x) = ln|x-1| - x + 1                       — разрыв в x = 1, не симметричная ")
    print("   f7(x) = 0.5*(9*e^(sin(5x+4)/2) / (x+2)^(1/3)) — разрыв в x = -2, не симметричная")
    print()


help()
while True:
    res = enter()
    if(res==None):
        sys.exit(1)
    fn, mn, a,b, eps = res
    n=4
    fn-=1
    mn-=1
    result = solve(fn, mn, a, b, n, eps)
    if len(result) == 3:
        print(result[2])
        print()
        continue
    else:
        ans, m = result

    if(Fs[fn]!=None):
        truly=Fs[fn](b)-Fs[fn](a)
    else:
        truly=None
    print()
    if(mn==0):
        print(ms[mn] + " дал ответ:")
        type=["Левые","Средние","Правые"]
        for i in range(0,3):
            if (truly!=None and abs(truly) > 10**-5):
                print(f"{type[i]}: {ans[i]}, разбиений {m[i]}, "
                  f"погрешность: {abs((ans[i] - truly) / truly) * 100:.4f}%")
            else:
                print(f"{type[i]}: {ans[i]}, разбиений {m[i]}")
        if(truly!=None):
            print(f"Правильный ответ: {truly:.4f}")
    else:
        print(ms[mn] + " дал ответ:", ans)
        print("Число разбиений:", m)
        if(truly!=None ):
            print(f"Правильный ответ: {truly:.4f}")
        if(truly!=None and abs(truly)>10**-5):
            print(f"Относительная погрешность: {abs((ans - truly) / truly) * 100:.4f}%")

    print()