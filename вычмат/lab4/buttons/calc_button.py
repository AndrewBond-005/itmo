# Константы кнопки вычисления
BUTTON_CALC_COLOR = "green"
BUTTON_CALC_TEXT = "Вычислить"
BUTTON_PADDING = 5

import tkinter as tk
from tkinter import ttk
from approximation_logic import (
    compute_all_approximations,
    find_best_approximation,
    format_results_text,
    get_quality_color,
    generate_function_points
)


def setup_calc_button(parent, table, graph, results_text, results_table):
    """Создаёт и настраивает кнопку "Вычислить"."""
    style = ttk.Style()
    style.configure("Calc.TButton", background=BUTTON_CALC_COLOR)

    btn = ttk.Button(
        parent,
        text=BUTTON_CALC_TEXT,
        style="Calc.TButton",
        command=lambda: on_calc_click(table, graph, results_text, results_table)
    )
    btn.pack(pady=BUTTON_PADDING)
    return btn


def on_calc_click(table, graph, results_text, results_table):
    """Обработчик нажатия кнопки "Вычислить"."""
    # Получаем данные из таблицы
    data = table.get_valid_data()

    # Очищаем предыдущие результаты
    results_text.delete(1.0, tk.END)
    results_table.clear()

    # Проверяем количество точек
    if len(data) < 4:
        results_text.insert(tk.END, "Недостаточно точек (нужно ≥4)\n", "error")
        results_text.tag_config("error", foreground="red")
        return

    # Извлекаем x и y
    x_values = [item['x'] for item in data]
    y_values = [item['y'] for item in data]

    # Очищаем график и рисуем точки
    graph.clear()
    graph.plot_points(x_values, y_values)

    # Вычисляем аппроксимации
    approximations = compute_all_approximations(x_values, y_values)

    if not approximations:
        results_text.insert(tk.END, "Не удалось вычислить ни одной аппроксимации\n", "error")
        results_text.tag_config("error", foreground="red")
        return

    # Заполняем таблицу результатов
    results_table.update_results(approximations)

    # Находим лучшую
    best = find_best_approximation(approximations)

    # Выводим результаты
    results_text.insert(tk.END, format_results_text(best))

    # Рисуем функцию на графике
    x_range, y_range = generate_function_points(x_values, best)
    if x_range and y_range:
        graph.plot_function(x_range, y_range)