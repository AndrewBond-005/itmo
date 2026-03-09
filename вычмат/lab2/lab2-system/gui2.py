import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from method import *

def f(x, y):
    return x ** 2 + y ** 2 - 4


def g(x, y):
    return y - 3 * x ** 2
def find_all_roots(x_range=(-2, 2), y_range=(-2, 2), step=0.2, eps=0.00001):
    """Находит все корни системы, запуская метод из разных начальных точек"""
    roots = []  # список найденных уникальных корней
    start_points = []  # список стартовых точек
    root_indices = []  # индекс корня для каждой стартовой точки

    # Сетка начальных точек
    x_starts = np.arange(x_range[0], x_range[1] + step, step)
    y_starts = np.arange(y_range[0], y_range[1] + step, step)

    for x0 in x_starts:
        for y0 in y_starts:
            k,root,ddx,ddy = newton(f, g, x0, y0, eps)

            if root is not None:
                # Проверяем, нашли ли мы уже этот корень
                found = False
                for i, r in enumerate(roots):
                    if sqrt((r[0] - root[0]) ** 2 + (r[1] - root[1]) ** 2) < 0.01:
                        root_indices.append(i)
                        found = True
                        break

                if not found:
                    roots.append(root)
                    root_indices.append(len(roots) - 1)

                start_points.append((x0, y0))

    return roots, start_points, root_indices


def plot_system(roots, start_points, root_indices):
    """Рисует график системы и стартовые точки"""
    plt.figure(figsize=(10, 8))

    # Создаем сетку для контуров
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)

    # Вычисляем значения функций
    Z1 = f(X, Y)
    Z2 = g(X, Y)

    # Рисуем линии уровня f(x,y)=0
    plt.contour(X, Y, Z1, levels=[0], colors='blue', linewidths=2, label='f(x,y)=0')
    # Рисуем линии уровня g(x,y)=0
    plt.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2, label='g(x,y)=0')

    # Отмечаем найденные корни
    colors = ['green', 'orange', 'purple', 'brown', 'pink', 'gray']
    for i, root in enumerate(roots):
        plt.plot(root[0], root[1], 'o', color=colors[i % len(colors)],
                 markersize=10, label=f'Корень {i + 1}: ({root[0]:.3f}, {root[1]:.3f})')

    # Отмечаем стартовые точки цветом в зависимости от того, к какому корню сошлись
    for i, (x0, y0) in enumerate(start_points):
        color_idx = root_indices[i] % len(colors)
        plt.plot(x0, y0, '.', color=colors[color_idx], markersize=3, alpha=0.6)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Решение системы уравнений методом Ньютона из разных начальных точек')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.show()


# Находим все корни
print("Поиск корней системы:")
print("f(x,y) = x² + y² - 4 = 0")
print("g(x,y) = y - 3x² = 0")
print("-" * 50)

roots, start_points, root_indices = find_all_roots(
    x_range=(-2, 2),
    y_range=(-2, 2),
    step=0.2,
    eps=0.00001
)

# Выводим найденные корни
print(f"\nНайдено {len(roots)} уникальных корней:")
for i, root in enumerate(roots):
    print(f"Корень {i + 1}: x = {root[0]:.6f}, y = {root[1]:.6f}")
    print(f"  Проверка: f(x,y) = {f(root[0], root[1]):.2e}, g(x,y) = {g(root[0], root[1]):.2e}")

print(f"\nВсего стартовых точек: {len(start_points)}")

# Строим график
plot_system(roots, start_points, root_indices)

# Дополнительно покажем области притяжения
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
x = np.linspace(-2.5, 2.5, 50)
y = np.linspace(-2.5, 2.5, 50)
X, Y = np.meshgrid(x, y)
Z1 = f(X, Y)
Z2 = g(X, Y)
plt.contour(X, Y, Z1, levels=[0], colors='blue', linewidths=2)
plt.contour(X, Y, Z2, levels=[0], colors='red', linewidths=2)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Линии уровня функций')
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.subplot(1, 2, 2)
for i, (x0, y0) in enumerate(start_points):
    color_idx = root_indices[i] % len(colors)
    plt.plot(x0, y0, '.', color=colors[color_idx % len(colors)], markersize=4)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Области притяжения корней')
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.tight_layout()
plt.show()