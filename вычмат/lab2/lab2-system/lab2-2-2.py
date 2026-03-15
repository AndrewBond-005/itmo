import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.lines import Line2D
from method import newton
from funcs import fs
import json


def parse_float(value):
    """Преобразует строку в число, поддерживая запятые"""
    if isinstance(value, (int, float)):
        return value
    try:
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        raise ValueError(f"Невозможно преобразовать '{value}' в число")


# Описания систем (обновлено)
systems = [
    (fs[0][0], fs[0][1], "x² + y² = 4, y = 3x²"),
    (fs[1][0], fs[1][1], "sin²(2x) - cos²(x) = y, -sin(2x-1)/2 = y"),
    (fs[2][0], fs[2][1], "log₃(sin(x)+1.01)+2 = y, (9e^(sin(2x+4)/2))/(x+2)-1 = y")
]


def on_system_change(*args):
    idx = func_var.get()
    update_plot(idx=idx)


def solve():
    try:
        x0 = parse_float(x_entry.get())
        y0 = parse_float(y_entry.get())
        eps = parse_float(eps_entry.get())
        idx = func_var.get()

        f, g = fs[idx]
        result = newton(f, g, x0, y0, eps)

        if isinstance(result, str):
            result_label.config(text=f"Ошибка: {result}")
            return

        k, x_res, y_res, ddx, ddy = result

        result_label.config(
            text=f"Ответ: x = {x_res:.8f}, y = {y_res:.8f}\n"
                 f"Итераций: {k}, |Δ| = {max(abs(ddx), abs(ddy)):.2e}"
        )

        update_plot(x_res, y_res, x0, y0, idx)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def update_plot(x_res=None, y_res=None, x0=None, y0=None, idx=0):
    ax.clear()

    f, g = fs[idx]

    # Полная область для расчета (до 10)
    x_full = np.linspace(-10, 10, 400)
    y_full = np.linspace(-10, 10, 400)
    X_full, Y_full = np.meshgrid(x_full, y_full)

    # Вычисляем значения функций на полной области
    Z1_full = np.zeros_like(X_full)
    Z2_full = np.zeros_like(X_full)

    for i in range(len(y_full)):
        for j in range(len(x_full)):
            try:
                Z1_full[i, j] = f(X_full[i, j], Y_full[i, j])
                Z2_full[i, j] = g(X_full[i, j], Y_full[i, j])
            except:
                Z1_full[i, j] = np.nan
                Z2_full[i, j] = np.nan

    # Рисуем линии уровня на полной области
    ax.contour(X_full, Y_full, Z1_full, levels=[0], colors='blue', linewidths=2)
    ax.contour(X_full, Y_full, Z2_full, levels=[0], colors='red', linewidths=2)

    # Элементы для легенды
    legend_elements = [
        Line2D([0], [0], color='blue', linewidth=2, label='f(x,y)=0'),
        Line2D([0], [0], color='red', linewidth=2, label='g(x,y)=0')
    ]

    # Начальная точка
    if x0 is not None and y0 is not None:
        ax.plot(x0, y0, 'go', markersize=8)
        legend_elements.append(Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8,
                                      label='Начальное приближение'))

    # Найденный корень (кружочек вместо звезды)
    if x_res is not None and y_res is not None:
        ax.plot(x_res, y_res, 'ro', markersize=8, markeredgecolor='red', markerfacecolor='red')
        legend_elements.append(
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Найденный корень'))

    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Система {idx + 1}: {systems[idx][2]}')
    ax.grid(True, alpha=0.3)
    ax.legend(handles=legend_elements, loc='upper right')

    # Устанавливаем видимую область [-5, 5] для начального вида
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    canvas.draw()


def clear_plot():
    result_label.config(text="Ответ: не найден")
    idx = func_var.get()
    update_plot(idx=idx)


def import_config():
    """Импортирует конфигурацию из JSON файла"""
    from tkinter import filedialog

    file_path = filedialog.askopenfilename(
        title="Выберите файл конфигурации",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Проверяем структуру файла
        if "system" not in config:
            messagebox.showerror("Ошибка", "В файле не указан номер системы")
            return

        # Устанавливаем систему
        system_idx = config["system"] - 1
        if 0 <= system_idx < len(systems):
            func_var.set(system_idx)
        else:
            messagebox.showwarning("Предупреждение", f"Номер системы должен быть от 1 до {len(systems)}")

        # Устанавливаем начальное приближение
        if "x0" in config:
            x_entry.set(str(config["x0"]).replace('.', ','))
        if "y0" in config:
            y_entry.set(str(config["y0"]).replace('.', ','))

        # Устанавливаем точность
        if "eps" in config:
            eps_entry.set(str(config["eps"]).replace('.', ','))

        messagebox.showinfo("Успех", "Конфигурация успешно загружена")

    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Неверный формат JSON файла")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")


def save_results():
    """Сохраняет результаты в JSON файл"""
    from tkinter import filedialog

    # Проверяем, есть ли результат
    if result_label.cget("text") == "Ответ: не найден":
        messagebox.showwarning("Предупреждение", "Нет результатов для сохранения")
        return

    file_path = filedialog.asksaveasfilename(
        title="Сохранить результаты",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if not file_path:
        return

    try:
        idx = func_var.get()

        # Парсим результат из label
        result_text = result_label.cget("text")
        lines = result_text.split('\n')

        # Извлекаем x и y
        x_str = lines[0].split('x = ')[1].split(',')[0]
        y_str = lines[0].split('y = ')[1]
        x_res = float(x_str)
        y_res = float(y_str)

        # Извлекаем итерации
        iter_str = lines[1].split('Итераций: ')[1].split(',')[0]
        iterations = int(iter_str)

        # Извлекаем невязку
        delta_str = lines[1].split('|Δ| = ')[1]
        delta = float(delta_str)

        output_data = {
            "system": idx + 1,
            "system_description": systems[idx][2],
            "x0": parse_float(x_entry.get()),
            "y0": parse_float(y_entry.get()),
            "eps": parse_float(eps_entry.get()),
            "result": {
                "x": x_res,
                "y": y_res,
                "iterations": iterations,
                "residual": delta
            }
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("Успех", f"Результаты сохранены в {file_path}")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


root = tk.Tk()
root.title("Решение систем уравнений методом Ньютона")
root.geometry("1200x700")

main = ttk.Frame(root, padding="10")
main.pack(fill="both", expand=True)

left = ttk.LabelFrame(main, text="Параметры", padding="10")
left.pack(side="left", fill="y", padx=5)

ttk.Label(left, text="Система уравнений:").pack(anchor="w", pady=5)

func_var = tk.IntVar(value=0)
func_var.trace('w', on_system_change)

for i, (_, _, desc) in enumerate(systems):
    ttk.Radiobutton(left, text=f"{i + 1}. {desc}", variable=func_var, value=i).pack(anchor="w", pady=2)

ttk.Label(left, text="Начальное приближение:").pack(anchor="w", pady=(10, 0))

frame_xy = ttk.Frame(left)
frame_xy.pack(fill="x", pady=5)

ttk.Label(frame_xy, text="x₀ =").pack(side="left")
x_entry = tk.StringVar(value="1")
x_entry_entry = ttk.Entry(frame_xy, textvariable=x_entry, width=10)
x_entry_entry.pack(side="left", padx=5)

ttk.Label(frame_xy, text="y₀ =").pack(side="left", padx=(10, 0))
y_entry = tk.StringVar(value="1")
y_entry_entry = ttk.Entry(frame_xy, textvariable=y_entry, width=10)
y_entry_entry.pack(side="left", padx=5)

ttk.Label(left, text="Точность:").pack(anchor="w", pady=(10, 0))
eps_entry = tk.StringVar(value="0.00001")
eps_entry_entry = ttk.Entry(left, textvariable=eps_entry, width=15)
eps_entry_entry.pack(anchor="w", pady=5)

# Кнопки для файловых операций
file_frame = ttk.LabelFrame(left, text="Файл", padding="5")
file_frame.pack(fill="x", pady=10)

ttk.Button(file_frame, text="Загрузить конфигурацию", command=import_config).pack(fill="x", pady=2)
ttk.Button(file_frame, text="Сохранить результаты", command=save_results).pack(fill="x", pady=2)

# Основные кнопки
ttk.Button(left, text="Найти корень", command=solve).pack(pady=5)
ttk.Button(left, text="Очистить", command=clear_plot).pack(pady=5)

result_label = ttk.Label(left, text="Ответ: не найден", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

right = ttk.LabelFrame(main, text="График", padding="10")
right.pack(side="right", fill="both", expand=True, padx=5)

fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

toolbar = NavigationToolbar2Tk(canvas, right)
toolbar.update()

update_plot(idx=0)
root.mainloop()