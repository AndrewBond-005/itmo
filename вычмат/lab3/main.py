from rectangle import *
from enter import *
from readfile import *
from rand import *
from funcs import *
from runge import *



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
    res = enter()
    fn, mn, a,b, eps = res
    n=4
    fn-=1
    mn-=1
    ans,m=solve(fs[fn],mn,a,b,n,eps)
    truly=Fs[fn](b)-Fs[fn](a)
    if(mn==0):
        print(ms[mn] + " дал ответ:")
        type=["Левые","Средние","Правые"]
        for i in range(0,3):
            print(f"{type[i]}: {ans[i]}, разбиений {m[i]}, "
                  f"погрешность: {abs((ans[i] - truly) / truly) * 100:.4f}%")
    else:
        print(ms[mn] + " дал ответ:", ans[0])
        print("Число разбиений:", m[0])
        print(f"Правильный ответ: {truly:.4f}")
        print(f"Относительная погрешность: {abs((ans[0] - truly) / truly) * 100:.4f}%")

    print()
