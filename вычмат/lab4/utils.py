# Константы для форматирования
DEFAULT_DECIMALS = 3

def parse_number(s):
    """
    Преобразует строку в число float.
    Поддерживает запятую как десятичный разделитель.
    Возвращает None, если преобразование невозможно.
    """
    if not isinstance(s, str):
        s = str(s)
    s = s.strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def format_number(value, decimals=DEFAULT_DECIMALS):
    """
    Форматирует число в строку с заданным количеством знаков после запятой.
    """
    if value is None:
        return ""
    try:
        return f"{value:.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)