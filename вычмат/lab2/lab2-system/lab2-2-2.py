import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from method import newton

# Импортируем системы уравнений
from funcs import fs  # fs = [(f1,g1), (f2,g2), (f3,g3)]


# ============ ФУНКЦИИ ============
def solve():
    try:
        x0 = float(x_entry.get())
        y0 = float(y_entry.get())
        eps = float(eps_entry.get())
        idx = func_var.get()

        f, g = fs[idx]
        k, x, y,ddx,ddy = newton(f, g, x0, y0, eps)

        result_label.config(text=f"Ответ: x = {x:.8f}, y = {y:.8f}")

        # Обновляем график с результатом
        update_plot(x, y, x0, y0, idx)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def update_plot(x_res=None, y_res=None, x0=None, y0=None, idx=0):
    ax.clear()

    f, g = fs[idx]

    # Сетка для графика
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)

    # Вычисляем значения функций
    Z1 = np.array([[f(X[i, j], Y[i, j]) for j in range(len(x))] for i in range(len(y))])
    Z2 = np.array([[g(X[i, j], Y[i, j]) for j in range(len(x))] for i in range(len(y))])

    # Рисуем линии уровня
    ax.contour(X, Y, Z1, levels=[0], colors='blue', linewidths=2)
    ax.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2)

    # Начальная точка
    if x0 is not None and y0 is not None:
        ax.plot(x0, y0, 'go', markersize=8, label='Начальное приближение')

    # Найденный корень
    if x_res is not None and y_res is not None:
        ax.plot(x_res, y_res, 'r*', markersize=12, label='Найденный корень')

    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Решение системы уравнений')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.axis('equal')
    canvas.draw()


# ============ ИНТЕРФЕЙС ============
root = tk.Tk()
root.title("Решение систем уравнений методом Ньютона")
root.geometry("1200x700")

main = ttk.Frame(root, padding="10")
main.pack(fill="both", expand=True)

# Левая панель
left = ttk.LabelFrame(main, text="Параметры", padding="10")
left.pack(side="left", fill="y", padx=5)

# Выбор системы
ttk.Label(left, text="Система уравнений:").pack(anchor="w", pady=5)

func_var = tk.IntVar(value=0)
systems = [
    "Система 1: x² + y² = 4, y = 3x²",
    "Система 2: ...",
    "Система 3: ..."
]

for i, text in enumerate(systems):
    ttk.Radiobutton(left, text=text, variable=func_var, value=i).pack(anchor="w", pady=2)

# Начальное приближение
ttk.Label(left, text="Начальное приближение:").pack(anchor="w", pady=(10, 0))

frame_xy = ttk.Frame(left)
frame_xy.pack(fill="x", pady=5)

ttk.Label(frame_xy, text="x₀ =").pack(side="left")
x_entry = ttk.Entry(frame_xy, width=10)
x_entry.pack(side="left", padx=5)
x_entry.insert(0, "-1")

ttk.Label(frame_xy, text="y₀ =").pack(side="left", padx=(10, 0))
y_entry = ttk.Entry(frame_xy, width=10)
y_entry.pack(side="left", padx=5)
y_entry.insert(0, "2")

# Точность
ttk.Label(left, text="Точность:").pack(anchor="w", pady=(10, 0))
eps_entry = ttk.Entry(left, width=15)
eps_entry.pack(anchor="w", pady=5)
eps_entry.insert(0, "0.00001")

# Кнопка
ttk.Button(left, text="Найти корень", command=solve).pack(pady=15)

# Результат
result_label = ttk.Label(left, text="Ответ: не найден", font=("Arial", 10, "bold"))
result_label.pack(pady=10)

# Правая панель (график)
right = ttk.LabelFrame(main, text="График", padding="10")
right.pack(side="right", fill="both", expand=True, padx=5)

fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Панель инструментов для масштабирования
toolbar = NavigationToolbar2Tk(canvas, right)
toolbar.update()

# Первоначальный график
update_plot(idx=0)

root.mainloop()