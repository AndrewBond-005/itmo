def readfile(arg):
    global input
    global print

    print("Чтобы прочитать файл введите его название с расширением и без кавычек")
    print("Данные в файле должны быть представлены так же как если бы их вводили в консоли")
    print(
        "Т.е. сначала 1 число - размерность , потом матрица - n строк по n чисел, потом вектор значений - строка из n чисел"
        " и на четвёртой строке погрещность - 1 число. Всё через пробел")
    print()
    if arg is None:
        print("Введите название файла: ")
        name = input().strip()
    else:
        name = arg.strip()

    if (name == "exit"):
        return "Выход"
    try:
        # Пытаемся открыть файл
        f = open(name, 'r', encoding='utf-8')
    except FileNotFoundError:
        return f"Ошибка: Файл '{name}' не найден. Проверьте имя файла и путь к нему."

    lines = f.readlines()
    if not lines:
        return "Ошибка: Файл пуст."

    try:
        n = float(lines[0].strip().replace(',', '.'))
        if n > 20 or n <= 0 or not (n.is_integer()):
            return "Размерность матрицы должна быть не больше 20 и строго больше нуля"
        n = int(n)
    except ValueError:
        return "Размерность должна быть целым числом"

    matrix = []
    for i in range(0, n):
        try:
            row = list(map(float, lines[i + 1].strip().replace(',', '.').split()))
            if len(row) != n:
                return f"В строке {i} матрицы должно быть {n} чисел, а получено {len(row)}"
            matrix.append(row)
        except ValueError:
            return f"В строке {i + 2} есть не число"
        except IndexError:
            return f"В файле не хватает строк матрицы"

    try:
        vector = list(map(float, lines[n + 1].replace(',', '.').split()))
    except ValueError:
        return "все элементы вектора занчений должны быть числами"

    try:
        eps = float(lines[n + 2].strip().replace(',', '.'))
        if eps <= 0:
            return "Точность должна быть положительной"
    except ValueError:
        return "Точность должна быть числом"

    return [matrix, vector, n, eps]
