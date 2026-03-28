def enter():
    print("Данные вводятся в таком порядке: номер функции, номер метода, интервал, точность")
    print("Введите номер функции - целое число от 1 до 4")
    while (True):
        print("Номер функции: ", end=" ")
        inp = input()
        if (inp == "exit"):
            return "Выход"
        try:
            n = float(inp.strip().replace(',', '.'))
            if (n <= 4 and n > 0) and n.is_integer():
                fn = int(n)
                break
            print("Номер функции это число от 1 до 4")
        except ValueError:
            print("Номер должен быть целым числом")

    print("Введите номер метода - целое число от 1 до 3")
    while (True):
        print("Номер метода: ", end=" ")
        inp = input()
        if (inp == "exit"):
            return "Выход"
        try:
            n = float(inp.strip().replace(',', '.'))
            if (n <= 3 and n > 0) and n.is_integer():
                mn = int(n)
                break
            print("Номер метода это число от 1 до 2")
        except ValueError:
            print("Номер должен быть целым числом")

    print("Введите границы области интегрирования - 2 числа записанных через пробел")
    print("Границы:", end=" ")
    while True:
        inp = input()
        if (inp == "exit"):
            return "Выход"
        try:
            v = list(map(float, inp.replace(',', '.').split()))
            if(len(v)==2):
                break
            print("Надо ввести рвоно два числа")
        except ValueError:
            print("Граница это число")
        print("Границы:", end=" ")

    print("Введите точность вычислений ε - положительное число")
    print("Точность:", end=" ")
    while True:
        inp = input()
        if (inp == "exit"):
            return "Выход"
        try:
            eps = float(inp.strip().replace(',', '.'))
            if eps > 0:
                break
            print("Точность должна быть положительной")
        except ValueError:
            print("Точность должна быть числом")
        print("Точность:", end=" ")
    return [fn,mn, v[0],v[1], eps]
