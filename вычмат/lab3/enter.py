from funcs import *


def enter():
    print("Данные вводятся в таком порядке: номер функции, номер метода, интервал, точность")
    print(f"Введите номер функции - целое число от 1 до {len(fs)}")
    while True:
        print("Номер функции: ", end=" ")
        inp = input().strip()
        if inp.lower() == "exit":
            return None
        try:
            n = float(inp.replace(',', '.'))
            if n.is_integer() and 1 <= n <= len(fs):
                fn = int(n)
                break
            print(f"Номер функции это число от 1 до {len(fs)}")
        except ValueError:
            print("Номер должен быть целым числом")

    print("Введите номер метода - целое число от 1 до 4")
    print("  1 - Метод прямоугольников")
    print("  2 - Метод трапеций")
    print("  3 - Метод Симпсона")
    print("  4 - Все три метода")
    while True:
        print("Номер метода: ", end=" ")
        inp = input().strip()
        if inp.lower() == "exit":
            return None
        try:
            n = float(inp.replace(',', '.'))
            if n.is_integer() and 1 <= n <= 4:
                mn = int(n)
                break
            print("Номер метода это число от 1 до 4")
        except ValueError:
            print("Номер должен быть целым числом")

    print("Введите границы области интегрирования - 2 числа записанных через пробел")
    print("Границы:", end=" ")
    while True:
        inp = input().strip()
        if inp.lower() == "exit":
            return None
        try:
            v = list(map(float, inp.replace(',', '.').split()))
            if len(v) == 2:
                break
            print("Надо ввести ровно два числа")
        except ValueError:
            print("Граница это число")
        print("Границы:", end=" ")

    print("Введите точность вычислений ε - положительное число")
    print("Точность:", end=" ")
    while True:
        inp = input().strip()
        if inp.lower() == "exit":
            return None
        try:
            eps = float(inp.replace(',', '.'))
            if eps > 0:
                break
            print("Точность должна быть положительной")
        except ValueError:
            print("Точность должна быть числом")
        print("Точность:", end=" ")

    return [fn, mn, v[0], v[1], eps]