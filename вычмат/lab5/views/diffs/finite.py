import calc.differences as diffs
import calc.newton_finite as newton_fin


def format_finite_table(x_sorted, y_sorted):
    """
    Форматирует таблицу конечных разностей

    Returns:
        str: отформатированная таблица
    """
    if len(x_sorted) < 2:
        return "Недостаточно точек (<2) для построения таблицы разностей"

    # Проверка равномерности шага
    is_uniform, h = newton_fin.check_uniform_step(x_sorted)
    if not is_uniform:
        return "Таблица конечных разностей не определена: шаг неравномерный"

    # Получаем таблицу разностей
    table = diffs.finite_differences_table(y_sorted)
    n = len(table)

    # Формируем заголовки
    headers = ["xᵢ", "yᵢ"]
    for i in range(1, n):
        if i == 1:
            headers.append("Δyᵢ")
        else:
            headers.append(f"Δ{i}yᵢ")

    # Формируем строки таблицы
    rows = []
    for i in range(n):
        row = [f"x{i}", x_sorted[i], table[i][0]] + [table[i][j] if j < len(table[i]) else None for j in
                                                     range(1, n - i)]
        rows.append(row)

    # Вычисляем ширины колонок
    max_widths = [0] * (n + 2)
    for j, header in enumerate(headers):
        max_widths[j] = max(max_widths[j], len(header))

    for row in rows:
        for j, cell in enumerate(row):
            if j < len(max_widths) and cell is not None:
                if isinstance(cell, float):
                    cell_str = f"{cell:8.3f}"
                else:
                    cell_str = str(cell)
                max_widths[j] = max(max_widths[j], len(cell_str))

    # Формируем вывод
    lines = []

    # Заголовки
    header_line = "  ".join(f"{h:>{max_widths[i]}}" for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-" * len(header_line))

    # Строки
    for row in rows:
        cells = []
        for j, cell in enumerate(row):
            if j < len(max_widths):
                if cell is None:
                    cells.append(" " * max_widths[j])
                elif isinstance(cell, float):
                    cells.append(f"{cell:>{max_widths[j]}.3f}")
                else:
                    cells.append(f"{str(cell):>{max_widths[j]}}")
        lines.append("  ".join(cells))

    return "\n".join(lines)