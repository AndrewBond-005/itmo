import calc.differences as diffs
import calc.newton_finite as newton_fin


def format_finite_table(x_sorted, y_sorted):
    if len(x_sorted) < 2:
        return "Недостаточно точек (<2) для построения таблицы разностей"

    is_uniform, h = newton_fin.check_step(x_sorted)
    if not is_uniform:
        return "Таблица конечных разностей не определена: шаг неравномерный"

    table = diffs.finite_differences_table(y_sorted)
    n = len(x_sorted)

    # Заголовки - всего n столбцов (x_i, y_i, Δy_i, Δ²y_i, ..., Δ^(n-1)y_i)
    headers = ["xᵢ", "yᵢ"]
    for k in range(1, n):
        headers.append(f"Δ^{k}yᵢ" if k > 1 else "Δyᵢ")

    # Строки данных
    rows = []
    for i in range(n):
        row = [f"x{i}", f"{x_sorted[i]:.3f}"]
        # В строке i должно быть n - i "числовых" столбцов (y_i + разности)
        # Но первый числовой столбец (y_i) уже добавлен, остаётся (n - i - 1) разностей
        for k in range(1, n - i):  # k - порядок разности
            if k - 1 < len(table) and i < len(table[k - 1]):
                row.append(f"{table[k - 1][i]:.3f}")
            else:
                row.append("")
        rows.append(row)

    # Находим максимальную ширину для каждого столбца
    max_widths = []
    for j in range(len(headers)):
        max_len = len(headers[j])
        for row in rows:
            if j < len(row) and len(row[j]) > max_len:
                max_len = len(row[j])
        max_widths.append(max_len + 1)

    # Формируем вывод
    lines = []
    header_line = "".join(f"{headers[i]:>{max_widths[i]}}" for i in range(len(headers)))
    lines.append(header_line)
    lines.append("-" * len(header_line))

    for row in rows:
        line = ""
        for j in range(len(headers)):
            if j < len(row):
                line += f"{row[j]:>{max_widths[j]}}"
            else:
                line += " " * max_widths[j]
        lines.append(line)

    return "\n".join(lines)