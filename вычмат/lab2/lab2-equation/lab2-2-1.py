from chord import *
from help import *
from simple_iteration import *
from parser import *
from newton import *

helps()
print("Введите номер уравнения, границы интервалов и точность")
while True:
    s = input()
    res = parse(s)
    if type(res) == str:
        if(res=="exit"):
            exit()
        if (res == "help"):
            help()
            continue
        print(res)
        continue
    n, a, b, eps = res
    try:
        roots = check_one_root(fl[n], a, b)
        if roots != 1:
            print( f"На указанном промежтке должен быть ровно один корень, сейчас их {roots}")
            continue
        print(f"Уравнение {fsl[n-1]}, ищем от {a} до {b} с точностью {eps}:")
    except ZeroDivisionError:
        print("Произошло деление на ноль в вычилениях. " +
          "Уточните корни так чтобы ноль не входил в интервал изоляции корня")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка {e}")

    try:
        x=chord(a,b,eps,fl[n])
        print("Ответ метода простой итерации:", x,fl[n](x))
    except ZeroDivisionError:
        print("Произошло деление на ноль в вычилениях. " +
          "Уточните корни так чтобы ноль не входил в интервал изоляции корня")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка {e}")

    try:
        x=chord(a,b,eps,fl[n])
        print("Ответ метода хорд:", x, fl[n](x))
    except ZeroDivisionError:
        print("Произошло деление на ноль в вычилениях. "+
              "Уточните корни так чтобы ноль не входил в интервал изоляции корня")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка {e}")

    try:
        x=chord(a,b,eps,fl[n])
        print("Ответ метода Ньютона:", x, fl[n](x))
    except ZeroDivisionError:
        print("Произошло деление на ноль в вычилениях. "+
              "Уточните корни так чтобы ноль не входил в интервал изоляции корня")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка {e}")
