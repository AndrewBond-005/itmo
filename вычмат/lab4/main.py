import math
from input import *
from funcs import *
from aprox import *
def main():
    print("\n" + "=" * 60)
    print("LAB WORK #4 - FUNCTION APPROXIMATION")
    print("=" * 60)
    while True:
        print("\n1 - Input from console")
        print("2 - Load from file")
        print("0 - Exit")

        choice = input("\nYour choice: ")

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            x, y, n = input_from_console()
        elif choice == "2":
            filename = input("Filename: ")
            x, y, n = input_from_file(filename)
        else:
            print("Invalid choice!")
            continue

        if n < 8 or n > 12:
            print(f"Warning: {n} points. Recommended 8-12.")

        print("\nInput data:")
        print(f"{'#':<4} {'x':<10} {'y':<10}")
        print("-" * 25)
        for i in range(n):
            print(f"{i + 1:<4} {x[i]:<10.3f} {y[i]:<10.3f}")

        print("\n" + "=" * 90)
        print(
            f"{'Function':<15} {'Equation':<45} {'S':<10} {'δ':<10} {'R²':<10} {'r':<8}"
        )
        print("=" * 90)

        results = {}

        # Linear
        try:
            coeffs = linear_approx(x, y, n)
            a0, a1 = coeffs
            phi_vals = compute_phi(x, [a0, a1], 'poly')
            S = sum_of_squares(y, phi_vals)
            delta = math.sqrt(S / n)
            r2 = determination_coefficient(y, phi_vals)
            r = correlation_coefficient(x, y)
            results["Linear"] = (a0, a1, S, delta, r2, r, phi_vals, 'poly', [a0, a1])
            eq = f"{a0:.3f} + {a1:.3f}·x"
            print(f"{'Linear':<15} {eq:<45} {S:<10.3f} {delta:<10.3f} {r2:<10.3f} {r:<8.3f}")
        except Exception as e:
            print(f"{'Linear':<15} {'ERROR':<45} {str(e):<10}")

        # Quadratic
        try:
            coeffs = polinom_approx(x, y, n, 2 + 1)
            a0, a1, a2 = coeffs
            phi_vals = compute_phi(x, [a0, a1, a2], 'poly')
            S = sum_of_squares(y, phi_vals)
            delta = math.sqrt(S / n)
            r2 = determination_coefficient(y, phi_vals)
            results["Quadratic"] = (a0, a1, a2, S, delta, r2, phi_vals, 'poly', [a0, a1, a2])
            eq = f"{a0:.3f} + {a1:.3f}·x + {a2:.3f}·x²"
            print(f"{'Quadratic':<15} {eq:<45} {S:<10.3f} {delta:<10.3f} {r2:<10.3f} {'—':<8}")
        except Exception as e:
            print(f"{'Quadratic':<15} {'ERROR':<45} {str(e):<10}")

        # Cubic
        try:
            coeffs = polinom_approx(x, y, n, 3 + 1)
            a0, a1, a2, a3 = coeffs
            phi_vals = compute_phi(x, [a0, a1, a2, a3], 'poly')
            S = sum_of_squares(y, phi_vals)
            delta = math.sqrt(S / n)
            r2 = determination_coefficient(y, phi_vals)
            results["Cubic"] = (a0, a1, a2, a3, S, delta, r2, phi_vals, 'poly', [a0, a1, a2, a3])
            eq = f"{a0:.3f} + {a1:.3f}·x + {a2:.3f}·x² + {a3:.3f}·x³"
            print(f"{'Cubic':<15} {eq:<45} {S:<10.3f} {delta:<10.3f} {r2:<10.3f} {'—':<8}")
        except Exception as e:
            print(f"{'Cubic':<15} {'ERROR':<45} {str(e):<10}")

        # Exponential
        try:
            coeffs = exponential_approx(x, y, n)
            a, b = coeffs
            phi_vals = compute_phi(x, None, 'exp', a=a, b=b)
            S = sum_of_squares(y, phi_vals)
            delta = math.sqrt(S / n)
            r2 = determination_coefficient(y, phi_vals)
            results["Exponential"] = (a, b, S, delta, r2, phi_vals, 'exp', None)
            eq = f"{a:.3f}·e^({b:.3f}·x)"
            print(f"{'Exponential':<15} {eq:<45} {S:<10.3f} {delta:<10.3f} {r2:<10.3f} {'—':<8}")
        except Exception as e:
            print(f"{'Exponential':<15} {'ERROR':<45} {str(e):<10}")

        # Logarithmic
        try:
            coeffs = logarithmic_approx(x, y, n)
            a, b = coeffs
            phi_vals = compute_phi(x, None, 'log', a=a, b=b)
            S = sum_of_squares(y, phi_vals)
            delta = math.sqrt(S / n)
            r2 = determination_coefficient(y, phi_vals)
            results["Logarithmic"] = (a, b, S, delta, r2, phi_vals, 'log', None)
            eq = f"{a:.3f}·ln(x) + {b:.3f}"
            print(f"{'Logarithmic':<15} {eq:<45} {S:<10.3f} {delta:<10.3f} {r2:<10.3f} {'—':<8}")
        except Exception as e:
            print(f"{'Logarithmic':<15} {'ERROR':<45} {str(e):<10}")

        # Power
        try:
            coeffs = power_approx(x, y, n)
            a, b = coeffs
            phi_vals = compute_phi(x, None, 'power', a=a, b=b)
            S = sum_of_squares(y, phi_vals)
            delta = math.sqrt(S / n)
            r2 = determination_coefficient(y, phi_vals)
            results["Power"] = (a, b, S, delta, r2, phi_vals, 'power', None)
            eq = f"{a:.3f}·x^{b:.3f}"
            print(f"{'Power':<15} {eq:<45} {S:<10.3f} {delta:<10.3f} {r2:<10.3f} {'—':<8}")
        except Exception as e:
            print(f"{'Power':<15} {'ERROR':<45} {str(e):<10}")

        if len(results) == 0:
            print("\nNo approximations computed successfully!")
            input("\nPress Enter to continue...")
            continue

        # Находим лучшую по минимальному δ
        best_name = None
        best_delta = float('inf')
        for name, data in results.items():
            delta = data[3] if len(data) > 3 else data[2]
            if delta < best_delta:
                best_delta = delta
                best_name = name

        #если коэффициент Пирсона > 0.95, то побеждает линейная
        if "Linear" in results:
            pearson_r = results["Linear"][5]  # r хранится на позиции 5
            if pearson_r > 0.95:
                print(f"   Pearson's r = {pearson_r:.4f} > 0.95")
                print("   Data is basically a straight line!")
                print("   Forcing Linear as the best approximation")
                best_name = "Linear"
                best_delta = results["Linear"][3]

        print("\n" + "=" * 90)
        print("BEST APPROXIMATION")
        print("=" * 90)

        if best_name:
            data = results[best_name]
            if best_name == "Linear":
                a0, a1, S, delta, r2, r, _, _, _ = data
                print(f"Function: {best_name}")
                print(f"Equation: φ(x) = {a0:.3f} + {a1:.3f}·x")
                print(f"S = {S:.3f}, δ = {delta:.3f}, R² = {r2:.3f}, r (Pearson) = {r:.3f}")
            elif best_name == "Quadratic":
                a0, a1, a2, S, delta, r2, _, _, _ = data
                print(f"Function: {best_name}")
                print(f"Equation: φ(x) = {a0:.3f} + {a1:.3f}·x + {a2:.3f}·x²")
                print(f"S = {S:.3f}, δ = {delta:.3f}, R² = {r2:.3f}")
            elif best_name == "Cubic":
                a0, a1, a2, a3, S, delta, r2, _, _, _ = data
                print(f"Function: {best_name}")
                print(f"Equation: φ(x) = {a0:.3f} + {a1:.3f}·x + {a2:.3f}·x² + {a3:.3f}·x³")
                print(f"S = {S:.3f}, δ = {delta:.3f}, R² = {r2:.3f}")
            elif best_name == "Exponential":
                a, b, S, delta, r2, _, _, _ = data
                print(f"Function: {best_name}")
                print(f"Equation: φ(x) = {a:.3f}·e^({b:.3f}·x)")
                print(f"S = {S:.3f}, δ = {delta:.3f}, R² = {r2:.3f}")
            elif best_name == "Logarithmic":
                a, b, S, delta, r2, _, _, _ = data
                print(f"Function: {best_name}")
                print(f"Equation: φ(x) = {a:.3f}·ln(x) + {b:.3f}")
                print(f"S = {S:.3f}, δ = {delta:.3f}, R² = {r2:.3f}")
            elif best_name == "Power":
                a, b, S, delta, r2, _, _, _ = data
                print(f"Function: {best_name}")
                print(f"Equation: φ(x) = {a:.3f}·x^{b:.3f}")
                print(f"S = {S:.3f}, δ = {delta:.3f}, R² = {r2:.3f}")

        # Сообщение о качестве R² (исправленное)
        if best_name:
            r2 = results[best_name][4] if len(results[best_name]) > 4 else results[best_name][2]
            if r2 >= 0.95:
                print("High accuracy (R² ≥ 0.95) - model describes phenomenon well")
            elif r2 >= 0.75:
                print("Satisfactory approximation (0.75 ≤ R² < 0.95)")
            elif r2 >= 0.5:
                print("Weak approximation (0.5 ≤ R² < 0.75)")
            else:
                print("Insufficient accuracy (R² < 0.5) - model needs improvement")

         # Вывод таблицы с x, y, φ(x), ε для луч1юшей функции
            print()
            print(f"ПОДРОБНАЯ ТАБЛИЦА ДЛЯ {best_name} АППРОКСИМАЦИИ")
            print("=" * 90)
            print(f"{'#':<4} {'x':<12} {'y (эксп)':<14} {'φ(x)':<14} {'ε = φ(x)-y':<14}")
            print("-" * 60)

            for i in range(n):
                eps = phi_vals[i] - y[i]
                print(f"{i+1:<4} {x[i]:<12.3f} {y[i]:<14.3f} {phi_vals[i]:<14.3f} {eps:<14.3f}")
        # Автоматический переход на следующую итерацию (без лишних вопросов)
        # Если хочешь паузу — раскомментируй строку ниже:
        # input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()