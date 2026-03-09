import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from chord import *
from simple_iteration import *
from newton import *
from funcs import fl, fsl
from help import helps
import warnings

warnings.filterwarnings('ignore')

from root import check_one_root


class RootFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Численные методы решения нелинейных уравнений")
        self.root.geometry("1200x700")

        # Для каждого из трех корней храним выбранный метод
        self.methods_for_roots = [tk.StringVar(value="Ньютона") for _ in range(3)]

        # Переменные для текущей функции
        self.current_func_index = tk.IntVar(value=1)
        self.current_func_index.trace('w', self.update_plot)

        # Интервалы для каждого корня
        self.root_intervals = [
            {"a": tk.DoubleVar(value=-3.0), "b": tk.DoubleVar(value=-1.0)},
            {"a": tk.DoubleVar(value=-1.0), "b": tk.DoubleVar(value=1.0)},
            {"a": tk.DoubleVar(value=1.0), "b": tk.DoubleVar(value=3.0)}
        ]

        # Точность
        self.eps = tk.DoubleVar(value=1e-6)

        # Результаты
        self.results = [None, None, None]

        self.setup_ui()
        self.update_plot()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Левая панель с управлением
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Выбор функции
        ttk.Label(control_frame, text="Выберите функцию:", font=('Arial', 10, 'bold')).grid(row=0, column=0,
                                                                                            columnspan=2, pady=5)

        functions = [
            ("Функция 1: 2.74x³ - 1.93x² - 15.28x - 3.72", 1),
            ("Функция 2: x³ - 2x² - 4x + 8", 2),
            ("Функция 3: sin(x) + cos(x²)", 3)
        ]

        for i, (text, val) in enumerate(functions):
            ttk.Radiobutton(
                control_frame,
                text=text,
                variable=self.current_func_index,
                value=val
            ).grid(row=i + 1, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Разделитель
        ttk.Separator(control_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E),
                                                               pady=10)

        # Настройки для каждого корня
        ttk.Label(control_frame, text="Настройки для корней:", font=('Arial', 10, 'bold')).grid(row=5, column=0,
                                                                                                columnspan=2, pady=5)

        for root_idx in range(3):
            self.create_root_settings(control_frame, root_idx)

        # Разделитель
        ttk.Separator(control_frame, orient='horizontal').grid(row=12, column=0, columnspan=2, sticky=(tk.W, tk.E),
                                                               pady=10)

        # Точность
        ttk.Label(control_frame, text="Точность:").grid(row=13, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.eps, width=15).grid(row=13, column=1, sticky=tk.W, pady=5)

        # Кнопки управления
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=14, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Найти корни", command=self.find_roots).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Помощь", command=self.show_help).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выход", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        # Результаты
        results_frame = ttk.LabelFrame(control_frame, text="Результаты", padding="5")
        results_frame.grid(row=15, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.result_labels = []
        for i in range(3):
            label = ttk.Label(results_frame, text=f"Корень {i + 1}: не найден", foreground="gray")
            label.pack(anchor=tk.W, pady=2)
            self.result_labels.append(label)

        # Правая панель с графиком
        plot_frame = ttk.LabelFrame(main_frame, text="График функции", padding="10")
        plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Создаем фигуру для графика
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def create_root_settings(self, parent, root_idx):
        """Создает настройки для конкретного корня"""
        frame = ttk.LabelFrame(parent, text=f"Корень {root_idx + 1}", padding="5")
        frame.grid(row=6 + root_idx * 2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Интервал
        ttk.Label(frame, text="Инвал [a, b]:").grid(row=0, column=0, sticky=tk.W, padx=5)

        a_entry = ttk.Entry(frame, textvariable=self.root_intervals[root_idx]["a"], width=8)
        a_entry.grid(row=0, column=1, padx=2)

        ttk.Label(frame, text="—").grid(row=0, column=2)

        b_entry = ttk.Entry(frame, textvariable=self.root_intervals[root_idx]["b"], width=8)
        b_entry.grid(row=0, column=3, padx=2)

        # Выбор метода
        ttk.Label(frame, text="Метод:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        methods = ["Ньютона", "Хорд", "Простой итерации"]
        method_combo = ttk.Combobox(
            frame,
            textvariable=self.methods_for_roots[root_idx],
            values=methods,
            state="readonly",
            width=15
        )
        method_combo.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=2, pady=5)

    def update_plot(self, *args):
        """Обновляет график функции"""
        self.ax.clear()

        func_idx = self.current_func_index.get()
        f = fl[func_idx]

        # Определяем диапазон для графика
        x_min = min(self.root_intervals[0]["a"].get(), -5)
        x_max = max(self.root_intervals[2]["b"].get(), 5)

        x = np.linspace(x_min, x_max, 1000)
        try:
            y = [f(xi) for xi in x]
            self.ax.plot(x, y, 'b-', linewidth=2, label=f'f(x)')

            # Отмечаем нулевую линию
            self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
            self.ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

            # Отмечаем интервалы для корней
            colors = ['red', 'green', 'orange']
            for i, interval in enumerate(self.root_intervals):
                a = interval["a"].get()
                b = interval["b"].get()
                self.ax.axvspan(a, b, alpha=0.2, color=colors[i], label=f'Интервал корня {i + 1}')

            # Если есть результаты, отмечаем их
            for i, result in enumerate(self.results):
                if result is not None:
                    self.ax.plot(result, 0, 'ro', markersize=8, color=colors[i])
                    self.ax.annotate(f'x{i + 1}', (result, 0), xytext=(5, 5),
                                     textcoords='offset points', fontsize=10, color=colors[i])

            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.set_title(f'График функции {fsl[func_idx]}')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend(loc='best')

        except Exception as e:
            self.ax.text(0.5, 0.5, f'Ошибка при построении графика:\n{str(e)}',
                         ha='center', va='center', transform=self.ax.transAxes)

        self.canvas.draw()

    def find_roots(self):
        """Находит все три корня выбранными методами"""
        func_idx = self.current_func_index.get()
        eps = self.eps.get()

        self.results = [None, None, None]

        for root_idx in range(3):
            a = self.root_intervals[root_idx]["a"].get()
            b = self.root_intervals[root_idx]["b"].get()
            method = self.methods_for_roots[root_idx].get()

            if a >= b:
                messagebox.showerror("Ошибка", f"Для корня {root_idx + 1} левая граница должна быть меньше правой")
                continue

            # Проверяем наличие корня на интервале
            try:
                roots_count = check_one_root(fl[func_idx], a, b)
                if roots_count != 1:
                    messagebox.showwarning("Предупреждение",
                                           f"На интервале [{a}, {b}] для корня {root_idx + 1} ожидается 1 корень, найдено {roots_count}")
            except:
                pass

            try:
                # Вызываем соответствующий метод
                if method == "Ньютона":
                    x0 = (a + b) / 2
                    result = newton(x0, eps, func_idx)
                elif method == "Хорд":
                    result = chord(a, b, eps, func_idx)
                else:  # Простой итерации
                    x0 = (a + b) / 2
                    result = simple_iteration(func_idx, a, b, eps)
                    iterations = "N/A"
                iterations=0
                self.results[root_idx] = result

                # Обновляем метку результата
                f_value = fl[func_idx](result)
                self.result_labels[root_idx].config(
                    text=f"Корень {root_idx + 1}: x = {result:.8f}  f(x) = {f_value:.2e}",
                    foreground="green"
                )

            except Exception as e:
                self.result_labels[root_idx].config(
                    text=f"Корень {root_idx + 1}: Ошибка - {str(e)[:50]}",
                    foreground="red"
                )

        self.update_plot()

    def clear_results(self):
        """Очищает результаты"""
        self.results = [None, None, None]
        for i, label in enumerate(self.result_labels):
            label.config(text=f"Корень {i + 1}: не найден", foreground="gray")
        self.update_plot()

    def show_help(self):
        """Показывает справку"""
        help_text = """Инструкция по использованию:

1. Выберите функцию из списка
2. Для каждого из трех корней задайте интервал [a, b]
3. Выберите метод для каждого корня
4. Задайте точность вычислений
5. Нажмите "Найти корни"

Методы:
- Ньютона: быстрая сходимость, требует хорошего начального приближения
- Хорд: надежный метод, гарантированная сходимость
- Простой итерации: требует приведения к виду x = φ(x)

Корни считаются независимо для каждого интервала."""

        messagebox.showinfo("Помощь", help_text)


def main():
    root = tk.Tk()
    app = RootFinderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()