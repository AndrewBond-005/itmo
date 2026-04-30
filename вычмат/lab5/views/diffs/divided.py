import calc.differences as diffs


def format_divided_table(x_sorted, y_sorted):
    if len(x_sorted) < 2:
        return "Недостаточно точек (<2) для построения таблицы разностей"

    table = diffs.divided_differences_table(x_sorted, y_sorted)
    n = len(x_sorted)

    # Заголовки
    headers = ["xᵢ", "yᵢ"]
    for k in range(1, n):
        headers.append(f"f^{k}" if k > 1 else "f¹")

    # Строки данных
    rows = []
    for i in range(n):
        row = [f"x{i}", f"{x_sorted[i]:.3f}"]
        # В строке i должно быть n - i числовых значений
        for k in range(1, n - i):
            if k - 1 < len(table) and i < len(table[k - 1]):
                val = table[k - 1][i]
                if isinstance(val, float) and val != val:
                    row.append("")
                else:
                    row.append(f"{val:.3f}")
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