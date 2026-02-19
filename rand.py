import random
import time


def rand(solvable, arg, eps):
    random.seed(int(time.time()))
    if (arg is None):
        print("Введите  размерность матрицы - натуральное число не превосходящее 20")
    k = 0
    while (True):
        if arg is not None and k == 0:
            inp = str(arg)
            k += 1
        else:
            print("Размерность: ", end=" ")
            inp = input()
        try:
            n = int(inp.strip().replace(',', '.'))
            if n <= 20 and n > 0:
                break
            print("Размерность матрицы должна быть не больше 20 и строго больше нуля")
        except ValueError:
            print("Размерность должна быть целым числом")

    matrix = []
    vector = []
    for i in range(0, n):
        vector.append(random.randint(-100, 100))
    if (eps is None):
        eps = random.uniform(0, 0.1)
    else:
        try:
            eps = float(eps.strip().replace(',', '.'))
            if eps < 0:
                eps = random.uniform(0, 0.1)
        except ValueError:
            eps = random.uniform(0, 0.1)
    if not solvable:
        for i in range(0, n):
            row = []
            for j in range(0, n):
                row.append(random.randint(-100, 100))
            matrix.append(row)
    else:
        midx = []
        mxv = []
        for i in range(0, n):
            max1 = random.randint(-100, -40)
            max2 = random.randint(40, 100)
            if (abs(max1) > abs(max2)):
                mx = max1
            else:
                mx = max2
            mxv.append(mx)
            while (True):
                idx = random.randint(0, n - 1)
                if not (idx in midx):
                    midx.append(idx)
                    break
            summ = 0
            rowm = []
            k = 0.6
            for j in range(0, n):
                if j != idx:
                    rnd = random.randint(int((summ - abs(mx) + 1) * k), int((abs(mx) - summ - 1) * k))
                    summ += abs(rnd)
                    rowm.append(rnd)
                else:
                    rowm.append(mx)
            matrix.append(rowm)

    print(f"Сгенерированная матрица для размерности n= {n}:")
    for i in range(n):
        print(f"{matrix[i]}")
    print(f"Вектор значений: {vector}")
    print(f"Точность ε: {eps}")
    return [matrix, vector, n, eps]
