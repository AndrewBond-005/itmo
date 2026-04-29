def format_number(value, precision=3):
    """Форматирует число с заданной точностью"""
    if value is None or (isinstance(value, float) and (value != value)):  # проверка на NaN
        return ""
    if isinstance(value, float):
        return f"{value:>{precision + 4}.{precision}f}"
    return f"{value:>{precision + 4}}"


def column_widths(table_data, headers):
    """Вычисляет максимальную ширину для каждой колонки"""
    widths = [len(h) for h in headers]

    for row in table_data:
        for i, cell in enumerate(row):
            if i < len(widths):
                cell_str = format_number(cell) if isinstance(cell, (int, float)) else str(cell)
                widths[i] = max(widths[i], len(cell_str))

    return widths


def format_row(cells, widths):
    """Форматирует строку с выравниванием"""
    formatted = []
    for i, cell in enumerate(cells):
        if i < len(widths):
            if isinstance(cell, (int, float)):
                formatted.append(format_number(cell))
            else:
                formatted.append(f"{str(cell):>{widths[i]}}")
        else:
            formatted.append("")
    return "  ".join(formatted)