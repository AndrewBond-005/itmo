from root import *
from funcs import *


def parse(s):
    parts = s.strip().split()
    if not parts:
        return "Вы ничего не ввели"
    if "exit" in parts:
        print("Выход из программы")
        return "exit"
    if "help" in parts:
        return "help"
    if len(parts) != 4:
        return "Ошибка: нужно ввести 4 числа"
    try:
        parts = [p.replace(',', '.') for p in parts]
        n, a, b, eps = int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
        if (a >= b):
            return "левая граница должна быть меньше правой"
    except ValueError:
        return "Ошибка: не удалось преобразовать в числа"
    return n, a, b, eps
