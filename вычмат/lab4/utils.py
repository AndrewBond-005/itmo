# utils.py
def parse_number(s):
    """Преобразует строку в число float."""
    if not isinstance(s, str):
        s = str(s)
    s = s.strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def format_number(value, decimals=3):
    """Форматирует число в строку."""
    if value is None:
        return ""
    try:
        return f"{value:.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)