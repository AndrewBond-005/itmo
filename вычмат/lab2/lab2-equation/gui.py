import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

warnings.filterwarnings('ignore')

# Импортируем ваши методы
from funcs import fl, fsl
from chord import chord
from newton import newton
from simple_iteration import simple_iteration
from root import check_one_root

# ============ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ============
func_idx = 1
eps = 1e-6
intervals = [[-3, -1.1], [-0.9, 1], [1, 3]]
methods = ["Ньютона", "Хорд", "Простой итерации"]
results = [None, None, None]
iterations = [0, 0, 0]  # для хранения количества итераций


# ============ ФУНКЦИИ ОБРАБОТКИ ============
def parse_float(value):
    """Преобразует строку в число, поддерживая запятые"""
    if isinstance(value, (int, float)):
        return value
    try:
        # Заменяем запятую на точку и преобразуем в float
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        raise ValueError(f"Невозможно преобразовать '{value}' в число")


def update_plot():
    """Обновляет график"""
    global func_idx, results

    # При смене функции очищаем результаты
    old_idx = func_idx
    func_idx = func_var.get()
    if old_idx != func_idx:
        results = [None, None, None]
        iterations = [0, 0, 0]
        for i in range(3):
            res_labels[i].config(text=f"Корень {i + 1}: не найден", foreground="gray")

    ax.clear()
    f = fl[func_idx]

    # Получаем границы интервалов с проверкой
    a_vals = []
    b_vals = []
    for i in range(3):
        try:
            a_vals.append(parse_float(a_vars[i].get()))
            b_vals.append(parse_float(b_vars[i].get()))
        except:
            a_vals.append(intervals[i][0])
            b_vals.append(intervals[i][1])

    x_min = min(-5, min(a_vals))
    x_max = max(5, max(b_vals))

    x = np.linspace(x_min, x_max, 1000)
    try:
        y = [f(xi) for xi in x]
        ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
        ax.set_ylim(-20, 20)  # фиксируем диапазон по y
    except:
        ax.text(0.5, 0.5, 'Ошибка при вычислении функции', ha='center', va='center')

    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

    colors = ['red', 'green', 'orange']
    for i in range(3):
        try:
            a = parse_float(a_vars[i].get())
            b = parse_float(b_vars[i].get())
            ax.axvspan(a, b, alpha=0.2, color=colors[i])
        except:
            pass  # пропускаем если ошибка получения значения

        if results[i] is not None:
            try:
                ax.plot(results[i], 0, 'ro', markersize=8, color=colors[i])
                ax.annotate(f'x{i + 1}', (results[i], 0), xytext=(5, 5),
                            textcoords='offset points', color=colors[i])
            except:
                pass

    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(f'f(x) = {fsl[func_idx - 1]}')
    ax.grid(True, alpha=0.3)

    # Уменьшаем поля графика
    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
    canvas.draw()


def find_roots():
    """Находит корни выбранными методами"""
    global results, func_idx, eps, iterations

    func_idx = func_var.get()

    # Преобразуем точность с поддержкой запятой
    try:
        eps = parse_float(eps_var.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректное значение точности")
        return

    results = [None, None, None]
    iterations = [0, 0, 0]

    for i in range(3):
        try:
            # Преобразуем границы интервала с поддержкой запятой
            a = parse_float(a_vars[i].get())
            b = parse_float(b_vars[i].get())
        except ValueError:
            res_labels[i].config(text=f"Корень {i + 1}: некорректное число", foreground="red")
            continue

        method = method_vars[i].get()

        if a >= b:
            res_labels[i].config(text=f"Корень {i + 1}: ошибка интервала", foreground="red")
            continue

        try:
            # Вызываем соответствующий метод и обрабатываем результат
            if method == "Ньютона":
                x0 = (a + b) / 2
                result = newton(x0, eps, fl[func_idx])
            elif method == "Хорд":
                result = chord(a, b, eps, fl[func_idx])
            else:  # Простой итерации
                result = simple_iteration(fl[func_idx], a, b, eps)

            # ПРОВЕРКА ТИПА РЕЗУЛЬТАТА
            if isinstance(result, str):
                # Метод вернул строку с ошибкой
                res_labels[i].config(text=f"Корень {i + 1}: {result}", foreground="red")
                results[i] = None
                iterations[i] = 0
                continue
            elif isinstance(result, tuple) and len(result) == 2:
                # Успешный результат - распаковываем кортеж
                res, iter_count = result

                # ПРОВЕРКА: если результат - не число
                if not isinstance(res, (int, float)):
                    res_labels[i].config(text=f"Корень {i + 1}: некорректный результат", foreground="red")
                    results[i] = None
                    iterations[i] = 0
                    continue

                results[i] = res
                iterations[i] = iter_count
                f_val = fl[func_idx](res)

                # Форматируем вывод с выравниванием
                text = f"Корень {i + 1}: x = {res:>12.8f}  f(x) = {f_val:>9.2e}  iter = {iter_count:>4d}"
                res_labels[i].config(text=text, foreground="green")
            else:
                # Неожиданный тип результата
                res_labels[i].config(text=f"Корень {i + 1}: неизвестный формат результата", foreground="red")
                results[i] = None
                iterations[i] = 0

        except ZeroDivisionError:
            res_labels[i].config(text=f"Корень {i + 1}: деление на ноль", foreground="red")
        except Exception as e:
            res_labels[i].config(text=f"Корень {i + 1}: {str(e)[:30]}", foreground="red")

    update_plot()


def clear_results():
    """Очищает результаты"""
    global results, iterations
    results = [None, None, None]
    iterations = [0, 0, 0]
    for i in range(3):
        res_labels[i].config(text=f"Корень {i + 1}: не найден", foreground="gray")
    update_plot()


def show_help():
    """Показывает справку"""
    help_text = """Использование:
1. Выберите функцию
2. Задайте интервалы [a, b] для трех корней
3. Выберите метод для каждого корня
4. Задайте точность
5. Нажмите "Найти корни"

Доступные функции:
1. 2.74x³ - 1.93x² - 15.28x - 3.72
2. x³ - 4x - 2
3. exp(2x)/(x²) - 10
4. log(|x|+1,3)/2 - 3sin(|x|+1) + 2.5"""

    messagebox.showinfo("Помощь", help_text)


# ============ СОЗДАНИЕ ОКНА ============
root = tk.Tk()
root.title("Численные методы решения нелинейных уравнений")
root.geometry("1100x650")  # Уменьшил размер окна

main = ttk.Frame(root, padding="5")
main.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# ============ ЛЕВАЯ ПАНЕЛЬ ============
left = ttk.LabelFrame(main, text="Управление", padding="8")
left.grid(row=0, column=0, sticky="nsew", padx=3)

# Выбор функции
ttk.Label(left, text="Выберите функцию:", font=('Arial', 9, 'bold')).grid(row=0, column=0, columnspan=2, pady=3,
                                                                          sticky="w")

func_var = tk.IntVar(value=1)
functions = [
    ("Функция 1: 2.74x³ - 1.93x² - 15.28x - 3.72", 1),
    ("Функция 2: x³ - 4x - 2", 2),
    ("Функция 3: exp(2x+2)/(x+1)² - 15", 3),
    ("Функция 4: 2*log(|x-0.5|+1,3) - 3sin(|x-0.5|)", 4)
]

for i, (text, val) in enumerate(functions):
    rb = ttk.Radiobutton(left, text=text, variable=func_var, value=val)
    rb.grid(row=i + 1, column=0, columnspan=2, sticky="w", pady=1)

func_var.trace('w', lambda *args: update_plot())

ttk.Separator(left, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=8)

# Настройки для корней
ttk.Label(left, text="Настройки для корней:", font=('Arial', 9, 'bold')).grid(row=6, column=0, columnspan=2, pady=3,
                                                                              sticky="w")

a_vars = []
b_vars = []
method_vars = []

for i in range(3):
    frame = ttk.LabelFrame(left, text=f"Корень {i + 1}", padding="3")
    frame.grid(row=7 + i * 2, column=0, columnspan=2, sticky="ew", pady=3)

    ttk.Label(frame, text="Интервал [a, b]:").grid(row=0, column=0, sticky="w", padx=2)

    # Используем StringVar вместо DoubleVar для поддержки запятых
    a_var = tk.StringVar(value=str(intervals[i][0]).replace('.', ','))
    a_vars.append(a_var)
    ttk.Entry(frame, textvariable=a_var, width=7).grid(row=0, column=1, padx=1)

    ttk.Label(frame, text="—").grid(row=0, column=2, padx=1)

    b_var = tk.StringVar(value=str(intervals[i][1]).replace('.', ','))
    b_vars.append(b_var)
    ttk.Entry(frame, textvariable=b_var, width=7).grid(row=0, column=3, padx=1)

    ttk.Label(frame, text="Метод:").grid(row=1, column=0, sticky="w", padx=2, pady=2)

    method_var = tk.StringVar(value=methods[i])
    method_vars.append(method_var)
    ttk.Combobox(frame, textvariable=method_var,
                 values=["Ньютона", "Хорд", "Простой итерации"],
                 state="readonly", width=15).grid(row=1, column=1, columnspan=3, sticky="w", padx=1)


def safe_update(*args):
    """Безопасное обновление графика с обработкой запятых"""
    try:
        # Пробуем получить и преобразовать все значения
        for i in range(3):
            parse_float(a_vars[i].get())
            parse_float(b_vars[i].get())
        update_plot()
    except:
        pass


for var in a_vars + b_vars:
    var.trace('w', safe_update)

ttk.Separator(left, orient="horizontal").grid(row=13, column=0, columnspan=2, sticky="ew", pady=8)

# Точность
ttk.Label(left, text="Точность:").grid(row=14, column=0, sticky="w", pady=3)
# Используем StringVar для точности тоже
eps_var = tk.StringVar(value=str(eps).replace('.', ','))
ttk.Entry(left, textvariable=eps_var, width=12).grid(row=14, column=1, sticky="w", pady=3)

# Кнопки
btn_frame = ttk.Frame(left)
btn_frame.grid(row=15, column=0, columnspan=2, pady=10)

ttk.Button(btn_frame, text="Найти корни", command=find_roots).pack(side="left", padx=3)
ttk.Button(btn_frame, text="Помощь", command=show_help).pack(side="left", padx=3)
ttk.Button(btn_frame, text="Очистить", command=clear_results).pack(side="left", padx=3)
ttk.Button(btn_frame, text="Выход", command=root.quit).pack(side="left", padx=3)

# Результаты
res_frame = ttk.LabelFrame(left, text="Результаты", padding="5")
res_frame.grid(row=16, column=0, columnspan=2, sticky="ew", pady=5)

res_labels = []
for i in range(3):
    label = ttk.Label(res_frame, text=f"Корень {i + 1}: не найден", foreground="gray", font=('Courier', 9))
    label.pack(anchor="w", pady=1, fill="x")
    res_labels.append(label)

# ============ ПРАВАЯ ПАНЕЛЬ (ГРАФИК) ============
right = ttk.LabelFrame(main, text="График функции", padding="5")
right.grid(row=0, column=1, sticky="nsew", padx=3)
main.columnconfigure(1, weight=3)  # Даем графику больше места
main.rowconfigure(0, weight=1)

# Создаем фигуру с уменьшенным размером
fig, ax = plt.subplots(figsize=(6, 4.5))  # Уменьшил размер
plt.subplots_adjust(left=0.08, right=0.97, top=0.95, bottom=0.1)  # Уменьшил поля

# Фрейм для панели инструментов
toolbar_frame = ttk.Frame(right)
toolbar_frame.pack(fill="x", pady=(0, 2))

canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Панель навигации matplotlib
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# ============ ЗАПУСК ============
update_plot()  # первый вызов
root.mainloop()