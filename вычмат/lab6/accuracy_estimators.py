"""
Оценка точности численных методов
"""

class AccuracyEstimator:
    """
    Оценка точности:
      - правило Рунге для одношаговых методов (Эйлер, РК4)
      - сравнение с точным решением для многошагового метода (Адамс)
    """

    @staticmethod
    def runge_error(method_func, f, x0, y0, xn, h, p):
        """
        Правило Рунге:
            err_i ≈ |y_h(x_i) - y_{h/2}(x_i)| / (2^p - 1)
        где p — порядок метода.
        Возвращает максимальную погрешность.
        """
        _, ys_h  = method_func(f, x0, y0, xn, h)
        _, ys_h2 = method_func(f, x0, y0, xn, h/2)

        ys_h2_coarse = ys_h2[::2]
        n = min(len(ys_h), len(ys_h2_coarse))

        errors = [
            abs(ys_h2_coarse[i] - ys_h[i]) / (2**p - 1)
            for i in range(n)
        ]
        return max(errors) if errors else 0.0

    @staticmethod
    def exact_error(xs, ys, exact_func, x0, y0):
        """ε = max|y_i^точн − y_i| для 0 ≤ i ≤ n"""
        errors = [abs(exact_func(xs[i], x0, y0) - ys[i]) for i in range(len(xs))]
        return max(errors) if errors else 0.0