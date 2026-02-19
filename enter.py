def enter():
    print("Сначала вводится размерность матрицы потом её коэффиценты. Далее вектор значений и следом точность")
    print()
    print("Введите  размерность матрицы - натуральное число не превосходящее 20")
    while (True):
        print("Размерность: ", end=" ")
        inp = input()
        if (inp == "exit"):
            return "Выход"
        try:
            n = float(inp.strip().replace(',', '.'))
            if (n <= 20 and n > 0) and n.is_integer():
                n = int(n)
                break
            print("Размерность матрицы должна быть не больше 20 и строго больше нуля")
        except ValueError:
            print("Размерность должна быть целым числом")

    matrix = []
    for i in range(n):
        while True:
            print(f"Строка {i + 1}: ", end='')
            try:
                row = list(map(float, input().replace(',', '.').split()))
                if len(row) != n:
                    print(f"Ошибка! Нужно ввести {n} чисел.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("Ошибка! Все элементы должны быть числами.")

    print("Введите вектор значений - n чисел записанных через пробел")
    print("Вектор значений:", end=" ")
    while True:
        inp = input()
        if (inp == "exit"):
            return "Выход"
        try:
            vector = list(map(float, inp.replace(',', '.').split()))
            break
        except ValueError:
            print("все элементы вектора занчений должны быть числами")
        print("Вектор значений:", end=" ")

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
    return [matrix, vector, n, eps]
