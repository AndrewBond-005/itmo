import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from method import newton
from funcs import systems


def solve():
    try:
        x0 = float(x_entry.get())
        y0 = float(y_entry.get())
        eps = float(eps_entry.get())
        idx = system_var.get()
        f, g, desc = systems[idx]

        res = newton(f, g, x0, y0, eps)

        if isinstance(res, str):
            result_label.config(text=f"Ошибка: {res}")
            return

        k, root, ddx, ddy = res

        result_label.config(
            text=f"Корень: x = {root[0]:.8f}, y = {root[1]:.8f}\n"
                 f"Итераций: {k}, |Δ| = {max(abs(ddx), abs(ddy)):.2e}"
        )

        # Обновляем график
        update_plot(f, g, x0, y0, root, idx)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def update_plot(f, g, x0, y0, root_point=None, idx=0):
    ax.clear()

    # Сетка для графика
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)

    # Вычисляем значения функций
    Z1 = np.array([[f(X[i, j], Y[i, j]) for j in range(len(x))] for i in range(len(y))])
    Z2 = np.array([[g(X[i, j], Y[i, j]) for j in range(len(x))] for i in range(len(y))])

    # Рисуем линии уровня
    ax.contour(X, Y, Z1, levels=[0], colors='blue', linewidths=2, label='f(x,y)=0')
    ax.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2, label='g(x,y)=0')

    # Начальная точка
    ax.plot(x0, y0, 'go', markersize=8, label='Начальное приближение')

    # Найденный корень
    if root_point:
        ax.plot(root_point[0], root_point[1], 'r*', markersize=12, label='Найденный корень')

    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Система {idx + 1}: {systems[idx][2]}')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    canvas.draw()


# Интерфейс
root = tk.Tk()
root.title("Решение систем уравнений методом Ньютона")
root.geometry("1200x700")

main = ttk.Frame(root, padding="10")
main.pack(fill="both", expand=True)

# Левая панель (управление)
left = ttk.LabelFrame(main, text="Параметры", padding="10")
left.pack(side="left", fill="y", padx=5)

# Выбор системы
ttk.Label(left, text="Выберите систему:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=5)

system_var = tk.IntVar(value=0)
for i, (_, _, desc) in enumerate(systems):
    ttk.Radiobutton(left, text=f"{i + 1}. {desc}", variable=system_var, value=i).pack(anchor="w", pady=2)

# Разделитель
ttk.Separator(left, orient='horizontal').pack(fill='x', pady=10)

# Начальное приближение
ttk.Label(left, text="Начальное приближение:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=5)

frame_xy = ttk.Frame(left)
frame_xy.pack(fill="x", pady=5)

ttk.Label(frame_xy, text="x₀ =").pack(side="left")
x_entry = ttk.Entry(frame_xy, width=10)
x_entry.pack(side="left", padx=5)
x_entry.insert(0, "1")

ttk.Label(frame_xy, text="y₀ =").pack(side="left", padx=(10, 0))
y_entry = ttk.Entry(frame_xy, width=10)
y_entry.pack(side="left", padx=5)
y_entry.insert(0, "2")

# Точность
ttk.Label(left, text="Точность:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(10, 0))
eps_entry = ttk.Entry(left, width=15)
eps_entry.pack(anchor="w", pady=5)
eps_entry.insert(0, "0.00001")

# Кнопка
ttk.Button(left, text="Найти корень", command=solve).pack(pady=15)

# Результат
result_label = ttk.Label(left, text="", font=("Arial", 10))
result_label.pack(pady=10)

# Правая панель (график)
right = ttk.LabelFrame(main, text="График", padding="10")
right.pack(side="right", fill="both", expand=True, padx=5)

# Создаем график
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Панель инструментов для масштабирования
toolbar = NavigationToolbar2Tk(canvas, right)
toolbar.update()

# Первоначальный график
f, g, _ = systems[0]
update_plot(f, g, 1, 2)

root.mainloop()