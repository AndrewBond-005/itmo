# Константы для аппроксимации
POLY_DEGREE = 3  # Степень полинома + 1 (3 = 2-я степень)
R_THRESHOLD = 0.95
POLY_DEGREE_3=4
from aprox import *
from funcs import *
from utils import format_number
import math


def compute_all_approximations(x_values, y_values):
    """
    Вычисляет все доступные типы аппроксимаций.
    Возвращает список словарей с параметрами каждой аппроксимации.
    """
    n = len(x_values)
    approximations = []

    # Линейная
    try:
        a, b = linear_approx(x_values, y_values, n)
        coeffs = (a, b)
        phi_vals = compute_phi(x_values, coeffs, 'poly')
        S = sum_of_squares(y_values, phi_vals)
        sigma = std_deviation(y_values, phi_vals)
        R2 = determination_coefficient(y_values, phi_vals)
        r = correlation_coefficient(x_values, y_values)

        approximations.append({
            'name': 'Линейная',
            'coeffs': coeffs,
            'func_type': 'poly',
            'S': S,
            'sigma': sigma,
            'R2': R2,
            'r': r,
            'formula': f"y = {format_number(b)}x + {format_number(a)}"
        })
    except:
        pass

    # Квадратичная
    if n >= 3:
        try:
            coeffs = polinom_approx(x_values, y_values, n, POLY_DEGREE)
            phi_vals = compute_phi(x_values, coeffs, 'poly')
            S = sum_of_squares(y_values, phi_vals)
            sigma = std_deviation(y_values, phi_vals)
            R2 = determination_coefficient(y_values, phi_vals)
            r = correlation_coefficient(x_values, y_values)

            formula = f"y = {format_number(coeffs[0])}"
            for i in range(1, len(coeffs)):
                if coeffs[i] >= 0:
                    formula += f" + {format_number(coeffs[i])}x^{i}"
                else:
                    formula += f" - {format_number(abs(coeffs[i]))}x^{i}"

            approximations.append({
                'name': 'Квадратичная',
                'coeffs': coeffs,
                'func_type': 'poly',
                'S': S,
                'sigma': sigma,
                'R2': R2,
                'r': r,
                'formula': formula
            })
        except:
            pass

    if n >= 4:
        try:
            coeffs = polinom_approx(x_values, y_values, n, POLY_DEGREE_3)
            phi_vals = compute_phi(x_values, coeffs, 'poly')
            S = sum_of_squares(y_values, phi_vals)
            sigma = std_deviation(y_values, phi_vals)
            R2 = determination_coefficient(y_values, phi_vals)
            r = correlation_coefficient(x_values, y_values)

            formula = f"y = {format_number(coeffs[0])}"
            for i in range(1, len(coeffs)):
                if coeffs[i] >= 0:
                    formula += f" + {format_number(coeffs[i])}x^{i}"
                else:
                    formula += f" - {format_number(abs(coeffs[i]))}x^{i}"

            approximations.append({
                'name': 'Кубическая',
                'coeffs': coeffs,
                'func_type': 'poly',
                'S': S,
                'sigma': sigma,
                'R2': R2,
                'r': r,
                'formula': formula
            })
        except:
            pass


    # Экспоненциальная
    try:
        if all(y > 0 for y in y_values):
            a, b = exponential_approx(x_values, y_values, n)
            phi_vals = compute_phi(x_values, None, 'exp', a, b)
            S = sum_of_squares(y_values, phi_vals)
            sigma = std_deviation(y_values, phi_vals)
            R2 = determination_coefficient(y_values, phi_vals)
            r = correlation_coefficient(x_values, y_values)

            approximations.append({
                'name': 'Экспоненциальная',
                'coeffs': (a, b),
                'func_type': 'exp',
                'S': S,
                'sigma': sigma,
                'R2': R2,
                'r': r,
                'formula': f"y = {format_number(a)} * e^({format_number(b)}x)"
            })
    except:
        pass

    # Логарифмическая
    try:
        if all(x > 0 for x in x_values):
            a, b = logarithmic_approx(x_values, y_values, n)
            phi_vals = compute_phi(x_values, None, 'log', a, b)
            S = sum_of_squares(y_values, phi_vals)
            sigma = std_deviation(y_values, phi_vals)
            R2 = determination_coefficient(y_values, phi_vals)
            r = correlation_coefficient(x_values, y_values)

            approximations.append({
                'name': 'Логарифмическая',
                'coeffs': (a, b),
                'func_type': 'log',
                'S': S,
                'sigma': sigma,
                'R2': R2,
                'r': r,
                'formula': f"y = {format_number(a)} * ln(x) + {format_number(b)}"
            })
    except:
        pass

    # Степенная
    try:
        if all(x > 0 and y > 0 for x, y in zip(x_values, y_values)):
            a, b = power_approx(x_values, y_values, n)
            phi_vals = compute_phi(x_values, None, 'power', a, b)
            S = sum_of_squares(y_values, phi_vals)
            sigma = std_deviation(y_values, phi_vals)
            R2 = determination_coefficient(y_values, phi_vals)
            r = correlation_coefficient(x_values, y_values)

            approximations.append({
                'name': 'Степенная',
                'coeffs': (a, b),
                'func_type': 'power',
                'S': S,
                'sigma': sigma,
                'R2': R2,
                'r': r,
                'formula': f"y = {format_number(a)} * x^{format_number(b)}"
            })
    except:
        pass

    return approximations


def find_best_approximation(approximations, r_threshold=R_THRESHOLD):
    """
    Выбирает лучшую аппроксимацию.
    Если у линейной |r| > r_threshold - выбираем линейную.
    Иначе - по R².
    """
    if not approximations:
        return None

    linear = next((a for a in approximations if a['name'] == 'Линейная'), None)

    if linear and abs(linear.get('r', 0)) > r_threshold:
        return linear

    return max(approximations, key=lambda x: x['R2'])


def format_results_text(best):
    """Формирует форматированный текст с результатами аппроксимации."""
    if best is None:
        return "Не удалось вычислить аппроксимацию"

    lines = []
    lines.append(f"Лучшая функция: {best['name']}")
    lines.append(f"{best['formula']}")
    lines.append("")
    lines.append("Параметры:")
    lines.append(f"Сумма квадратов отклонений (S): {format_number(best['S'], 6)}")
    lines.append(f"Среднеквадратическое отклонение (δ): {format_number(best['sigma'], 6)}")
    lines.append(f"Коэффициент детерминации (R²): {format_number(best['R2'], 6)}")
    if best['name'] == 'Линейная':
        lines.append(f"Коэффициент корреляции (r): {format_number(best['r'], 6)}")
    # Оценка качества
    if best['R2'] > 0.95:
        quality = "Отличная"
    elif best['R2'] > 0.8:
        quality = "Хорошая"
    elif best['R2'] > 0.6:
        quality = "Удовлетворительная"
    else:
        quality = "Плохая"

    lines.append(f"Оценка качества: {quality}")

    return "\n".join(lines)


def get_quality_color(R2):
    """Возвращает цвет для оценки качества."""
    if R2 > 0.95:
        return "darkgreen"
    elif R2 > 0.8:
        return "green"
    elif R2 > 0.6:
        return "orange"
    else:
        return "red"


def generate_function_points(x_values, best):
    """Генерирует точки для построения графика функции."""
    if not x_values or best is None:
        return [], []

    min_x, max_x = min(x_values), max(x_values)
    x_range = []
    step = (max_x - min_x) / 100
    x = min_x - 2
    while x <= max_x + 2:
        x_range.append(x)
        x += step

    if best['func_type'] == 'poly':
        y_range = [polynomial(xi, best['coeffs']) for xi in x_range]
    elif best['func_type'] == 'exp':
        y_range = [best['coeffs'][0] * math.exp(best['coeffs'][1] * xi) for xi in x_range]
    elif best['func_type'] == 'log':
        y_range = [best['coeffs'][0] * math.log(xi) + best['coeffs'][1] for xi in x_range if xi > 0]
        x_range = [xi for xi in x_range if xi > 0]
    elif best['func_type'] == 'power':
        y_range = [best['coeffs'][0] * (xi ** best['coeffs'][1]) for xi in x_range if xi > 0]
        x_range = [xi for xi in x_range if xi > 0]
    else:
        return [], []

    return x_range, y_range

def compute_phi_values(x_values, best):
    """Вычисляет значения φ(x) для лучшей функции."""
    if best['func_type'] == 'poly':
        return [polynomial(x, best['coeffs']) for x in x_values]
    elif best['func_type'] == 'exp':
        return [best['coeffs'][0] * math.exp(best['coeffs'][1] * x) for x in x_values]
    elif best['func_type'] == 'log':
        return [best['coeffs'][0] * math.log(x) + best['coeffs'][1] for x in x_values]
    elif best['func_type'] == 'power':
        return [best['coeffs'][0] * (x ** best['coeffs'][1]) for x in x_values]
    return []