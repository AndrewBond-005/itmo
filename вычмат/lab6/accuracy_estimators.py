from methods import euler, runge_kutta4
class AccuracyEstimator:

    @staticmethod
    def runge_error(method_func, f, x0, y0, xn, h, p):
        _, ys_h = method_func(f, x0, y0, xn, h)
        _, ys_h2 = method_func(f, x0, y0, xn, h / 2)
        ys_h2_coarse = ys_h2[::2]
        n = min(len(ys_h), len(ys_h2_coarse))
        errors = [
            abs(ys_h2_coarse[i] - ys_h[i]) / (2 ** p - 1)
            for i in range(n)
        ]
        max_err = max(errors) if errors else 0.0
        return max_err

    @staticmethod
    def exact_error(xs, ys, exact_func, x0, y0):
        errors = [abs(exact_func(xs[i], x0, y0) - ys[i]) for i in range(len(xs))]
        max_err = max(errors) if errors else 0.0
        return max_err

    @staticmethod
    def runge_error_with_adaptation(method_func, f, x0, y0, xn, eps, p, h_start=0.1, max_iter=10):

        h = h_start
        error = float('inf')
        for iteration in range(max_iter):
            xs, ys = method_func(f, x0, y0, xn, h)
            xs2, ys2 = method_func(f, x0, y0, xn, h / 2)
            ys2_coarse = ys2[::2]
            n = min(len(ys), len(ys2_coarse))
            errors = [abs(ys2_coarse[i] - ys[i]) for i in range(n)]
            max_error = max(errors) if errors else 0.0
            error = max_error / (2 ** p - 1)
            if error <= eps:
                return xs, ys, h, error
            h = h / 2
        xs, ys = method_func(f, x0, y0, xn, h)
        return xs, ys, h, error