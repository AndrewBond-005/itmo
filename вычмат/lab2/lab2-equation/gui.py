import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import json
warnings.filterwarnings('ignore')
from funcs import fl, fsl
from chord import chord
from help import *
from newton import newton
from simple_iteration import simple_iteration
from root import *

func_idx = 1
eps = 1e-6
intervals = [[-3, -0.9], [-0.9, 1], [1, 3]]
methods = ["Ньютона", "Хорд", "Простой итерации"]
results = [None, None, None]
iterations = [0, 0, 0]

def parse_float(value):
    if isinstance(value, (int, float)):
        return value
    try:
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        raise ValueError(f"Невозможно преобразовать '{value}' в число")

def import_config():
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
        if "function" not in config:
            messagebox.showerror("Ошибка", "В файле не указана функция")
            return
        if "roots" not in config or len(config["roots"]) != 3:
            messagebox.showerror("Ошибка", "В файле должны быть данные для 3 корней")
            return
        func_idx = config["function"]
        if 1 <= func_idx <= 4:
            func_var.set(func_idx)
        else:
            messagebox.showwarning("Предупреждение", "Номер функции должен быть от 1 до 4, используется значение по умолчанию")
        if "eps" in config:
            eps_val = config["eps"]
            eps_var.set(str(eps_val).replace('.', ','))
        method_map = {
            "newton": "Ньютона",
            "chord": "Хорд",
            "simple_iteration": "Простой итерации",
            "Ньютона": "Ньютона",
            "Хорд": "Хорд",
            "Простой итерации": "Простой итерации"
        }
        for i, root_data in enumerate(config["roots"]):
            if i >= 3:
                break
            if "a" in root_data:
                a_val = root_data["a"]
                a_vars[i].set(str(a_val).replace('.', ','))
            if "b" in root_data:
                b_val = root_data["b"]
                b_vars[i].set(str(b_val).replace('.', ','))
            if "method" in root_data:
                method = root_data["method"]
                if method in method_map:
                    method_vars[i].set(method_map[method])
        update_plot()
        clear_results()
        messagebox.showinfo("Успех", "Конфигурация успешно загружена")
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Неверный формат JSON файла")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

def save_results():
    from tkinter import filedialog
    if all(r is None for r in results):
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
        roots_data = []
        for i in range(3):
            if results[i] is not None:
                root_data = {
                    "root": round(results[i], 8),
                    "f_value": float(f"{fl[func_idx](results[i]):.2e}"),
                    "iterations": iterations[i]
                }
            else:
                root_data = {
                    "root": None,
                    "f_value": None,
                    "iterations": 0
                }
            roots_data.append(root_data)
        output_data = {
            "function_id": func_idx,
            "function_string": fsl[func_idx - 1],
            "eps": eps,
            "roots": roots_data
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", f"Результаты сохранены в {file_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

def update_plot():
    global func_idx, results
    old_idx = func_idx
    func_idx = func_var.get()
    if old_idx != func_idx:
        results = [None, None, None]
        iterations = [0, 0, 0]
        for i in range(3):
            res_labels[i].config(text=f"Корень {i + 1}: не найден", foreground="gray")
    ax.clear()
    f = fl[func_idx]
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
        ax.set_ylim(-20, 20)
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
            pass
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
    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
    canvas.draw()


def find_roots():
    global results, func_idx, eps, iterations
    func_idx = func_var.get()
    try:
        eps = parse_float(eps_var.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректное значение точности")
        return
    results = [None, None, None]
    iterations = [0, 0, 0]
    for i in range(3):
        try:
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
            roots_count = check_one_root(fl[func_idx], a, b)
            if roots_count != 1:
                res_labels[i].config(text=f"Корень {i + 1}: должен быть 1 корень, найдено {roots_count}",
                                     foreground="red")
                continue
        except ZeroDivisionError:
            res_labels[i].config(text=f"Корень {i + 1}: ошибка при проверке корней", foreground="red")
            continue
        except Exception as e:
            res_labels[i].config(text=f"Корень {i + 1}: ошибка проверки: {str(e)[:20]}", foreground="red")
            continue
        try:
            if method == "Ньютона":
                x0 = (a + b) / 2
                result = newton(a, b, x0, eps, fl[func_idx])
            elif method == "Хорд":
                result = chord(a, b, eps, fl[func_idx])
            else:
                result = simple_iteration(fl[func_idx], a, b, eps)
            if isinstance(result, str):
                res_labels[i].config(text=f"Корень {i + 1}: {result}", foreground="red")
                results[i] = None
                iterations[i] = 0
                continue
            elif isinstance(result, tuple) and len(result) == 2:
                res, iter_count = result
                if not isinstance(res, (int, float)):
                    res_labels[i].config(text=f"Корень {i + 1}: некорректный результат", foreground="red")
                    results[i] = None
                    iterations[i] = 0
                    continue
                results[i] = res
                iterations[i] = iter_count
                f_val = fl[func_idx](res)
                text = f"Корень {i + 1}: x = {res:>12.8f}  f(x) = {f_val:>9.2e}  iter = {iter_count:>4d}"
                res_labels[i].config(text=text, foreground="green")
            else:
                res_labels[i].config(text=f"Корень {i + 1}: неизвестный формат результата", foreground="red")
                results[i] = None
                iterations[i] = 0
        except ZeroDivisionError:
            res_labels[i].config(text=f"Корень {i + 1}: деление на ноль", foreground="red")
        except Exception as e:
            res_labels[i].config(text=f"Корень {i + 1}: {str(e)[:30]}", foreground="red")

    update_plot()
def clear_results():
    global results, iterations
    results = [None, None, None]
    iterations = [0, 0, 0]
    for i in range(3):
        res_labels[i].config(text=f"Корень {i + 1}: не найден", foreground="gray")
    update_plot()

def show_help():
    help_text = helps()
    messagebox.showinfo("Помощь", help_text)

root = tk.Tk()
root.title("Численные методы решения нелинейных уравнений")
root.geometry("1100x650")
main = ttk.Frame(root, padding="5")
main.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

left = ttk.LabelFrame(main, text="Управление", padding="8")
left.grid(row=0, column=0, sticky="nsew", padx=3)

ttk.Label(left, text="Выберите функцию:", font=('Arial', 9, 'bold')).grid(row=0, column=0, columnspan=2, pady=3, sticky="w")
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

ttk.Label(left, text="Настройки для корней:", font=('Arial', 9, 'bold')).grid(row=6, column=0, columnspan=2, pady=3, sticky="w")
a_vars = []
b_vars = []
method_vars = []
for i in range(3):
    frame = ttk.LabelFrame(left, text=f"Корень {i + 1}", padding="3")
    frame.grid(row=7 + i * 2, column=0, columnspan=2, sticky="ew", pady=3)
    ttk.Label(frame, text="Интервал [a, b]:").grid(row=0, column=0, sticky="w", padx=2)
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
    try:
        for i in range(3):
            parse_float(a_vars[i].get())
            parse_float(b_vars[i].get())
        update_plot()
    except:
        pass

for var in a_vars + b_vars:
    var.trace('w', safe_update)
ttk.Separator(left, orient="horizontal").grid(row=13, column=0, columnspan=2, sticky="ew", pady=8)

ttk.Label(left, text="Точность:").grid(row=14, column=0, sticky="w", pady=3)
eps_var = tk.StringVar(value=str(eps).replace('.', ','))
ttk.Entry(left, textvariable=eps_var, width=12).grid(row=14, column=1, sticky="w", pady=3)

import_save_frame = ttk.Frame(left)
import_save_frame.grid(row=15, column=0, columnspan=2, pady=5)
ttk.Button(import_save_frame, text="Импорт", command=import_config, width=10).pack(side="left", padx=5)
ttk.Button(import_save_frame, text="Сохранить", command=save_results, width=10).pack(side="left", padx=5)

btn_frame = ttk.Frame(left)
btn_frame.grid(row=16, column=0, columnspan=2, pady=5)
ttk.Button(btn_frame, text="Найти корни", command=find_roots).pack(side="left", padx=3)
ttk.Button(btn_frame, text="Помощь", command=show_help).pack(side="left", padx=3)
ttk.Button(btn_frame, text="Очистить", command=clear_results).pack(side="left", padx=3)
ttk.Button(btn_frame, text="Выход", command=root.quit).pack(side="left", padx=3)

res_frame = ttk.LabelFrame(left, text="Результаты", padding="5")
res_frame.grid(row=17, column=0, columnspan=2, sticky="ew", pady=5)
res_labels = []
for i in range(3):
    label = ttk.Label(res_frame, text=f"Корень {i + 1}: не найден", foreground="gray", font=('Courier', 9))
    label.pack(anchor="w", pady=1, fill="x")
    res_labels.append(label)

right = ttk.LabelFrame(main, text="График функции", padding="5")
right.grid(row=0, column=1, sticky="nsew", padx=3)
main.columnconfigure(1, weight=3)
main.rowconfigure(0, weight=1)

fig, ax = plt.subplots(figsize=(6, 4.5))
plt.subplots_adjust(left=0.08, right=0.97, top=0.95, bottom=0.1)
toolbar_frame = ttk.Frame(right)
toolbar_frame.pack(fill="x", pady=(0, 2))
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

update_plot()
root.mainloop()