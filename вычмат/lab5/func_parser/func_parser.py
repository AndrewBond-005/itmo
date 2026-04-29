import sympy as sp


def parse_function(expr: str):
    """
    Принимает строку вида "sin(x)", "x**2", "exp(x)", "log(x)".
    Возвращает callable f(x) или выбрасывает ValueError.

    Поддерживается:
    - Арифметика: + - * / **
    - Тригонометрия: sin, cos, tan, asin, acos, atan
    - Логарифмы: log, ln
    - Экспонента: exp
    - Степень: sqrt, x**2
    - Константы: pi, E
    """
    x = sp.Symbol('x')
    try:
        expr_sym = sp.sympify(expr)
        func = sp.lambdify(x, expr_sym, modules='numpy')
        return func
    except Exception as e:
        raise ValueError(f"Ошибка парсинга функции '{expr}': {e}")