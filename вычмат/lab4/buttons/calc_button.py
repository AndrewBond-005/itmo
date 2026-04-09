# Константы кнопки вычисления
import tkinter as tk
from tkinter import ttk

BUTTON_CALC_COLOR = "#009500"
BUTTON_CALC_DARKER_COLOR = "#006400"
BUTTON_CALC_TEXT = "Вычислить"
BUTTON_PADDING = 5

# Настройки границы кнопки вычисления
BUTTON_CALC_BORDER_WIDTH = 2
BUTTON_CALC_BORDER_COLOR = "#000000"
BUTTON_CALC_RELIEF = tk.RIDGE


from approximation_logic import (
    compute_all_approximations,
    find_best_approximation,
    format_results_text,
    get_quality_color,
    generate_function_points, compute_phi_values
)


def setup_calc_button(parent, table, graph, results_text, results_table):
    """Создаёт и настраивает кнопку "Вычислить"."""
    btn = tk.Button(
        parent,
        text=BUTTON_CALC_TEXT,
        bg=BUTTON_CALC_COLOR,
        fg="white",
        relief=BUTTON_CALC_RELIEF,
        bd=BUTTON_CALC_BORDER_WIDTH,
        highlightbackground=BUTTON_CALC_BORDER_COLOR,
        highlightcolor=BUTTON_CALC_BORDER_COLOR,
        highlightthickness=BUTTON_CALC_BORDER_WIDTH,
        padx=10,
        pady=2,
        activebackground=BUTTON_CALC_DARKER_COLOR,
        activeforeground="white",
        command=lambda: on_calc_click(btn, table, graph, results_text, results_table)
    )
    btn.pack(pady=BUTTON_PADDING)
    return btn


def on_calc_click(btn, table, graph, results_text, results_table):
    """Обработчик нажатия кнопки "Вычислить"."""
    data = table.get_valid_data()

    results_text.delete(1.0, tk.END)
    results_table.clear()
    table.clear_phi_epsilon()

    if len(data) < 8:
        results_text.insert(tk.END, "Недостаточно точек (нужно ≥4)\n", "error")
        results_text.tag_config("error", foreground="red")
        return

    x_values = [item['x'] for item in data]
    y_values = [item['y'] for item in data]

    graph.clear()
    graph.plot_points(x_values, y_values)

    approximations = compute_all_approximations(x_values, y_values)

    if not approximations:
        results_text.insert(tk.END, "Не удалось вычислить ни одной аппроксимации\n", "error")
        results_text.tag_config("error", foreground="red")
        return

    results_table.update_results(approximations)

    best = find_best_approximation(approximations)

    results_text.insert(tk.END, format_results_text(best))

    # Вычисляем φ(x) и ε для лучшей функции
    phi_values = compute_phi_values(x_values, best)
    epsilon_values = [y_values[i] - phi_values[i] for i in range(len(y_values))]
    table.update_phi_epsilon(phi_values, epsilon_values)

    x_range, y_range = generate_function_points(x_values, best)
    if x_range and y_range:
        graph.plot_function(x_range, y_range)