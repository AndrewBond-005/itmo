import math
def sx(lst):
    return sum(lst)

def sxx(lst):
    return sum(elem * elem for elem in lst)

def sxy(x, y):
    return sum(x[i] * y[i] for i in range(len(x)))

def sxn(lst, power):
    return sum(elem ** power for elem in lst)

def polynomial(x, coeffs):
    result = 0
    for power, coef in enumerate(coeffs):
        result += coef * (x ** power)
    return result

def compute_phi(x, coeffs, func_type, a=None, b=None):
    phi_vals = []
    if func_type == 'poly':
        for xi in x:
            val = 0
            for power, coef in enumerate(coeffs):
                val += coef * (xi ** power)
            phi_vals.append(val)
    elif func_type == 'exp':
        for xi in x:
            phi_vals.append(a * math.exp(b * xi))
    elif func_type == 'log':
        for xi in x:
            phi_vals.append(a * math.log(xi) + b)
    elif func_type == 'power':
        for xi in x:
            phi_vals.append(a * (xi ** b))
    return phi_vals

def sum_of_squares(y, phi_vals):
    return sum((phi_vals[i] - y[i]) ** 2 for i in range(len(y)))

def std_deviation(y, phi_vals):
    n = len(y)
    S = sum_of_squares(y, phi_vals)
    return math.sqrt(S / n)

def determination_coefficient(y, phi_vals):
    n = len(y)
    y_mean = sx(y) / n
    ss_res = sum_of_squares(y, phi_vals)
    ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
    if ss_tot == 0:
        return 1.0
    return 1 - ss_res / ss_tot

def correlation_coefficient(x, y):
    n = len(x)
    sum_x = sx(x)
    sum_y = sx(y)
    sum_xy = sxy(x, y)
    sum_x2 = sxx(x)
    sum_y2 = sxx(y)
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))
    if denominator == 0:
        return 0.0
    return numerator / denominator

def det(m):
    d = 0
    n = len(m)
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    for i in range(0, n):
        a = []
        for j in range(0, n):
            if i != j:
                a.append(m[j][1:])
        d += m[i][0] * (-1) ** i * det(a)
    return d