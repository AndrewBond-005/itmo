import tkinter as tk
from tkinter import filedialog
import data.core as core
from views.plot import lines
import calc.newton_finite as newton_fin
import calc.differences as diffs


def export_to_file(message_area, methods_panel=None):
    """
    Открывает диалог сохранения файла и сохраняет:
    - Узлы интерполяции
    - Вычисленные значения (если есть)
    - Таблицы разностей (конечные и разделённые)

    Returns:
        bool: True при успехе, False при ошибке
    """
    x_list = core.get_x()
    y_list = core.get_y()

    # Собираем только валидные точки
    points = []
    for x, y in zip(x_list, y_list):
        if x is not None and y is not None:
            points.append((x, y))

    if not points:
        message_area.add_message("Нет данных для экспорта (нет введённых точек)", "warning")
        return False

    file_path = filedialog.asksaveasfilename(
        title="Сохранить все данные в файл",
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )

    if not file_path:
        return False

    try:
        with open(file_path, 'w', encoding='utf-8') as f:


            # 1. Узлы интерполяции
            f.write("1. УЗЛЫ ИНТЕРПОЛЯЦИИ\n")
            f.write(f"{'№':>4} {'x':>12} {'y':>12}\n")
            for i, (x, y) in enumerate(points):
                f.write(f"{i:>4} {x:>12.6f} {y:>12.6f}\n")


            # 2. Вычисленные значения (если есть)
            compute_x = core.get_compute_x()
            computed_values = core.get_computed_values()

            if compute_x is not None and computed_values:
                f.write("2. ВЫЧИСЛЕННЫЕ ЗНАЧЕНИЯ\n")

                f.write(f"Точка x = {compute_x:.6f}\n\n")
                f.write(f"{'Метод':<20} {'Значение':>15}\n")

                # Порядок методов
                method_order = ["lagrange", "newton_div", "newton_fin"]
                method_names = {"lagrange": "Лагранж", "newton_div": "Ньютон (разд)", "newton_fin": "Ньютон (кон)"}

                for method in method_order:
                    if method in computed_values and computed_values[method] is not None:
                        f.write(f"{method_names[method]:<20} {computed_values[method]:>15.6f}\n")
                f.write("\n")

            # 3. Таблица конечных разностей
            f.write("3. ТАБЛИЦА КОНЕЧНЫХ РАЗНОСТЕЙ\n")

            x_sorted, y_sorted = lines.get_sorted_valid_nodes(core)
            if len(x_sorted) >= 2:
                is_uniform, h = newton_fin.check_step(x_sorted)
                if is_uniform:
                    table = diffs.finite_differences_table(y_sorted)
                    n = len(x_sorted)

                    # Заголовки
                    headers = ["xᵢ", "yᵢ"]
                    for k in range(1, n):
                        headers.append(f"Δ^{k}yᵢ" if k > 1 else "Δyᵢ")

                    # Ширина колонок
                    col_width = 12

                    # Заголовки
                    for hdr in headers:
                        f.write(f"{hdr:>{col_width}}")
                    f.write("\n")
                    f.write("-" * (len(headers) * col_width) + "\n")

                    # Данные
                    for i in range(n):
                        # x_i
                        f.write(f"x{i:>{col_width - 2}}")
                        # y_i
                        f.write(f"{x_sorted[i]:>{col_width}.4f}")
                        # разности
                        for k in range(1, n - i):
                            if k - 1 < len(table) and i < len(table[k - 1]):
                                f.write(f"{table[k - 1][i]:>{col_width}.4f}")
                            else:
                                f.write(f"{'':>{col_width}}")
                        f.write("\n")
                else:
                    f.write("Таблица конечных разностей не определена: шаг неравномерный\n")
            else:
                f.write("Недостаточно точек (<2) для построения таблицы разностей\n")
            f.write("\n")

            # 4. Таблица разделённых разностей
            f.write("4. ТАБЛИЦА РАЗДЕЛЁННЫХ РАЗНОСТЕЙ\n")

            if len(x_sorted) >= 2:
                table = diffs.divided_differences_table(x_sorted, y_sorted)
                n = len(x_sorted)

                # Заголовки
                headers = ["xᵢ", "yᵢ"]
                for k in range(1, n):
                    headers.append(f"f^{k}" if k > 1 else "f¹")

                # Ширина колонок
                col_width = 14

                # Заголовки
                for hdr in headers:
                    f.write(f"{hdr:>{col_width}}")
                f.write("\n")
                f.write("-" * (len(headers) * col_width) + "\n")

                # Данные
                for i in range(n):
                    # x_i
                    f.write(f"x{i:>{col_width - 2}}")
                    # y_i
                    f.write(f"{x_sorted[i]:>{col_width}.4f}")
                    # разделённые разности
                    for k in range(1, n - i):
                        if k - 1 < len(table) and i < len(table[k - 1]):
                            val = table[k - 1][i]
                            if isinstance(val, float) and val != val:  # NaN
                                f.write(f"{'':>{col_width}}")
                            else:
                                f.write(f"{val:>{col_width}.4f}")
                        else:
                            f.write(f"{'':>{col_width}}")
                    f.write("\n")
            else:
                f.write("Недостаточно точек (<2) для построения таблицы разностей\n")
            f.write("\n")


        message_area.add_message(f"Экспортировано {len(points)} точек + таблицы разностей в файл {file_path}", "info")
        return True

    except Exception as e:
        message_area.add_message(f"Ошибка сохранения файла: {e}", "error")
        return False