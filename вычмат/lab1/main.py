from simple_iteration_method import *
from enter import *
from readfile import *
from rand import *


def help():
    print("Чтобы ввести данные вручную введите \"enter\"")
    print("Чтобы ввести данные из файла введите \"file\" и следом имя файла на той же или новой строке")
    print("Чтобы сгенерировать случайную матрицу введите \"rand\" и следом число -"
          " размерность матрицы, опционально можно указать точность")
    print("Чтобы сгенерировать случайную матрицу для которой существует решение - "
          "введите \"random\" и следом число - размерность матрицы")
    print("Чтобы выйти из программы введите \"exit\" ")
    print("Чтобы увидеть данную справку ещё раз ввведите \"help\"")
    print()


help()
while True:
    matrix = []
    vector = []
    n = 0
    eps = None
    print("Введите команду: ", end='')
    s = input().strip().lower()
    mas = s.split()
    if (len(mas) == 1):
        s = mas[0]
        arg = None
    elif (len(mas) == 2):
        s = mas[0]
        arg = mas[1]
    elif (len(mas) == 3):
        if (mas[0] == "rand" or mas[0] == "random"):
            s = mas[0]
            arg = mas[1]
            eps = mas[2]
            print(s, arg, eps)
        else:
            print("Вы ввели слишком много параметров, допускается максимум")
            continue
    else:
        print("Вы ввели слишком много параметров, допускается максимум")
        continue
    if s == "help":
        help()
        continue
    elif s == "exit":
        break
    elif s == "rand":
        res = rand(False, arg, eps)
    elif s == "random":
        res = rand(True, arg, eps)
    elif s == "file":
        res = readfile(arg)
    elif s == "enter":
        res = enter()
    else:
        print("Такой команды нет, если нужна справка по командам введите help")
        continue

    if type(res) == str:
        if (res == "Выход"):
            break
        print(res)
        continue
    else:
        matrix, vector, n, eps = res

    ans = solve(matrix, vector, n, eps)
    if type(ans) == str:
        print(ans)
    else:
        cnt, x, err, norm = ans
        print("Норма матрицы:", norm)
        print("Вектор неизвестных х:", x)
        print("Количество итераций:", cnt)
        print("Вектор погрешностей:", err)
    print()
