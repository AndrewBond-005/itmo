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
    print("   f6(x) = ln|x-1| - x                      — разрыв в x = 1, не симметричная ")
    print("   f7(x) = 0.5*(9*e^(sin(5x+4)/2) / (x+2)^(1/3)) — разрыв в x = -2, не симметричная")
    print()


help()
while True:
    print()
    res = enter()
    if(res==None):
        sys.exit(1)
    fn, mnin, a, b, eps = res
    n = 4
    fn -= 1
    mn = mnin - 1
    if mn == 3:
        for method_idx in range(3):
            print(f"\n{ms[method_idx]}")
            result = solve(fn, method_idx, a, b, n, eps)
            if len(result) == 3:
                print(result[2])
                print()
                continue
            ans, m = result
            if Fs[fn] is not None:
                truly = Fs[fn](b) - Fs[fn](a)
            else:
                truly = None
            if method_idx == 0:
                types = ["Левые", "Средние", "Правые"]
                for i in range(3):
                    if truly is not None and abs(truly) > 1e-5:
                        rel_err = abs((ans[i] - truly) / truly) * 100
                        print(f"{types[i]}: {ans[i]:.10f}, разбиений {m[i]}, "
                              f"погрешность: {rel_err:.4f}%")
                    else:
                        print(f"{types[i]}: {ans[i]:.10f}, разбиений {m[i]}")
            else:  # Трапеции или Симпсон
                print(f"Результат: {ans:.10f}")
                print(f"Число разбиений: {m}")
                if truly is not None and abs(truly) > 1e-5:
                    rel_err = abs((ans - truly) / truly) * 100
                    print(f"Относительная погрешность: {rel_err:.4f}%")
            if truly is not None:
                print(f"Правильный ответ: {truly:.10f}")
    else:
        result = solve(fn, mn, a, b, n, eps)
        if len(result) == 3:
            print(result[2])
            print()
            continue
        ans, m = result
        if Fs[fn] is not None:
            truly = Fs[fn](b) - Fs[fn](a)
        else:
            truly = None
        print()
        if mn == 0:
            print(ms[mn] + " дал ответ:")
            types = ["Левые", "Средние", "Правые"]
            for i in range(3):
                if truly is not None and abs(truly) > 1e-5:
                    rel_err = abs((ans[i] - truly) / truly) * 100
                    print(f"{types[i]}: {ans[i]:.10f}, разбиений {m[i]}, "
                          f"погрешность: {rel_err:.4f}%")
                else:
                    print(f"{types[i]}: {ans[i]:.10f}, разбиений {m[i]}")
        else:
            print(ms[mn] + " дал ответ:", f"{ans:.10f}")
            print("Число разбиений:", m)
        if truly is not None:
            print(f"Правильный ответ: {truly:.10f}")
            if abs(truly) > 1e-5 and mn != 0:
                rel_err = abs((ans - truly) / truly) * 100
                print(f"Относительная погрешность: {rel_err:.4f}%")