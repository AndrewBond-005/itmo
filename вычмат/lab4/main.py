from input import *
from out import *
from aprox import *
def main():
    while True:
        print("\n" + "="*50)
        print("LAB WORK #4 - FUNCTION APPROXIMATION")
        print("="*50)

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
        print("-"*25)
        for i in range(n):
            print(f"{i+1:<4} {x[i]:<10.3f} {y[i]:<10.3f}")

        print("\nComputing approximations...")

        results = {}

        # Linear (считаем S и r отдельно)
        try:
            coeffs = linear_approx(x, y, n)
            if coeffs:
                a0, a1 = coeffs
                phi_vals = compute_phi(x, [a0, a1], 'poly')
                S = sum_of_squares(y, phi_vals)
                r = correlation_coefficient(x, y)
                results["Linear"] = (a0, a1, S, r)
                print("  Linear - OK")
            else:
                print("  Linear - FAILED")
        except Exception as e:
            print(f"  Linear - ERROR: {e}")

        # Quadratic (считаем S отдельно)
        try:
            coeffs = polinom_approx(x, y, n,2+1)
            if coeffs:
                a0, a1, a2 = coeffs
                phi_vals = compute_phi(x, [a0, a1, a2], 'poly')
                S = sum_of_squares(y, phi_vals)
                results["Quadratic"] = (a0, a1, a2, S)
                print("  Quadratic - OK")
            else:
                print("  Quadratic - FAILED")
        except Exception as e:
            print(f"  Quadratic - ERROR: {e}")

        # Cubic (считаем S отдельно)
        try:
            coeffs = polinom_approx(x, y, n,3+1)
            if coeffs:
                a0, a1, a2, a3 = coeffs
                phi_vals = compute_phi(x, [a0, a1, a2, a3], 'poly')
                S = sum_of_squares(y, phi_vals)
                results["Cubic"] = (a0, a1, a2, a3, S)
                print("  Cubic - OK")
            else:
                print("  Cubic - FAILED")
        except Exception as e:
            print(f"  Cubic - ERROR: {e}")

        # Exponential (считаем S отдельно)
        try:
            coeffs = exponential_approx(x, y, n)
            if coeffs:
                a, b = coeffs
                phi_vals = compute_phi(x, None, 'exp', a=a, b=b)
                S = sum_of_squares(y, phi_vals)
                results["Exponential"] = (a, b, S)
                print("  Exponential - OK")
            else:
                print("  Exponential - FAILED")
        except Exception as e:
            print(f"  Exponential - ERROR: {e}")

        # Logarithmic (считаем S отдельно)
        try:
            coeffs = logarithmic_approx(x, y, n)
            if coeffs:
                a, b = coeffs
                phi_vals = compute_phi(x, None, 'log', a=a, b=b)
                S = sum_of_squares(y, phi_vals)
                results["Logarithmic"] = (a, b, S)
                print("  Logarithmic - OK")
            else:
                print("  Logarithmic - FAILED")
        except Exception as e:
            print(f"  Logarithmic - ERROR: {e}")

        # Power (считаем S отдельно)
        try:
            coeffs = power_approx(x, y, n)
            if coeffs:
                a, b = coeffs
                phi_vals = compute_phi(x, None, 'power', a=a, b=b)
                S = sum_of_squares(y, phi_vals)
                results["Power"] = (a, b, S)
                print("  Power - OK")
            else:
                print("  Power - FAILED")
        except Exception as e:
            print(f"  Power - ERROR: {e}")

        if len(results) == 0:
            print("\nNo approximations computed successfully!")
            continue

        print_results(x, y, n, results)

        show = input("\nShow detailed table? (y/n): ")
        if show.lower() == 'y':
            print_detailed_table(x, y, results)

        print("\n" + "-"*50)
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()