import math
def print_results(x, y, n, results):
    print("\n" + "="*60)
    print("APPROXIMATION RESULTS")
    print("="*60)

    for name, data in results.items():
        print(f"\n--- {name} ---")

        if name == "Linear":
            a0, a1, S, r = data
            print(f"phi(x) = {a0:.3f} + {a1:.3f} * x")
            print(f"S = {S:.3f}")
            print(f"r = {r:.3f}")

        elif name == "Quadratic":
            a0, a1, a2, S = data
            print(f"phi(x) = {a0:.3f} + {a1:.3f} * x + {a2:.3f} * x^2")
            print(f"S = {S:.3f}")

        elif name == "Cubic":
            a0, a1, a2, a3, S = data
            print(f"phi(x) = {a0:.3f} + {a1:.3f} * x + {a2:.3f} * x^2 + {a3:.3f} * x^3")
            print(f"S = {S:.3f}")

        elif name == "Exponential":
            a, b, S = data
            print(f"phi(x) = {a:.3f} * e^({b:.3f} * x)")
            print(f"S = {S:.3f}")

        elif name == "Logarithmic":
            a, b, S = data
            print(f"phi(x) = {a:.3f} * ln(x) + {b:.3f}")
            print(f"S = {S:.3f}")

        elif name == "Power":
            a, b, S = data
            print(f"phi(x) = {a:.3f} * x^{b:.3f}")
            print(f"S = {S:.3f}")

    # Находим лучшую (с минимальным S)
    print("\n" + "="*60)
    print("BEST APPROXIMATION")
    print("="*60)

    min_S = float('inf')
    best_name = ""

    for name, data in results.items():
        if name == "Linear":
            S = data[2]
        elif name == "Quadratic":
            S = data[3]
        elif name == "Cubic":
            S = data[4]
        else:
            S = data[2]

        if S < min_S:
            min_S = S
            best_name = name

    print(f"Best function: {best_name}")
    print(f"Minimal S = {min_S:.3f}")

def print_detailed_table(x, y, results):
    """Вывод таблицы для лучшей функции"""
    # Находим лучшую
    min_S = float('inf')
    best_name = ""
    best_data = None

    for name, data in results.items():
        if name == "Linear":
            S = data[2]
        elif name == "Quadratic":
            S = data[3]
        elif name == "Cubic":
            S = data[4]
        else:
            S = data[2]

        if S < min_S:
            min_S = S
            best_name = name
            best_data = data

    # Вычисляем значения phi для лучшей функции
    phi_vals = []

    if best_name == "Linear":
        a0, a1, _, _ = best_data
        for xi in x:
            phi_vals.append(a0 + a1 * xi)

    elif best_name == "Quadratic":
        a0, a1, a2, _ = best_data
        for xi in x:
            phi_vals.append(a0 + a1 * xi + a2 * xi * xi)

    elif best_name == "Cubic":
        a0, a1, a2, a3, _ = best_data
        for xi in x:
            phi_vals.append(a0 + a1 * xi + a2 * xi * xi + a3 * xi ** 3)

    elif best_name == "Exponential":
        a, b, _ = best_data
        for xi in x:
            phi_vals.append(a * math.exp(b * xi))

    elif best_name == "Logarithmic":
        a, b, _ = best_data
        for xi in x:
            phi_vals.append(a * math.log(xi) + b)

    elif best_name == "Power":
        a, b, _ = best_data
        for xi in x:
            phi_vals.append(a * (xi ** b))

    # Выводим таблицу
    print("\n" + "="*70)
    print(f"DETAILED TABLE FOR {best_name} APPROXIMATION")
    print("="*70)
    print(f"{'#':<4} {'x':<10} {'y (exp)':<12} {'phi(x)':<12} {'epsilon':<12}")
    print("-"*55)

    for i in range(len(x)):
        eps = phi_vals[i] - y[i]
        print(f"{i+1:<4} {x[i]:<10.3f} {y[i]:<12.3f} {phi_vals[i]:<12.3f} {eps:<12.3f}")
