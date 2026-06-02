from methods import euler, runge_kutta4


class AccuracyEstimator:

    @staticmethod
    def runge_error(method_func, f, x0, y0, xn, h, p):
        print(f"[runge_error] Запуск с h={h}, p={p}")
        _, ys_h = method_func(f, x0, y0, xn, h)
        print(f"[runge_error] Решено с h={h}, точек={len(ys_h)}")

        _, ys_h2 = method_func(f, x0, y0, xn, h / 2)
        print(f"[runge_error] Решено с h/2={h / 2}, точек={len(ys_h2)}")

        ys_h2_coarse = ys_h2[::2]
        n = min(len(ys_h), len(ys_h2_coarse))
        print(f"[runge_error] Сравнение {n} точек")

        errors = [
            abs(ys_h2_coarse[i] - ys_h[i]) / (2 ** p - 1)
            for i in range(n)
        ]
        max_err = max(errors) if errors else 0.0
        print(f"[runge_error] Макс. погрешность = {max_err:.6e}")
        return max_err

    @staticmethod
    def exact_error(xs, ys, exact_func, x0, y0):
        print(f"[exact_error] Проверка {len(xs)} точек")
        errors = [abs(exact_func(xs[i], x0, y0) - ys[i]) for i in range(len(xs))]
        max_err = max(errors) if errors else 0.0
        print(f"[exact_error] Макс. погрешность = {max_err:.6e}")
        return max_err

    @staticmethod
    def runge_error_with_adaptation(method_func, f, x0, y0, xn, eps, p, h_start=0.1, max_iter=10):
        """
        Решение ОДУ с автоматическим подбором шага по правилу Рунге.
        Возвращает: (xs, ys, final_h, error)
        """
        h = h_start
        error = float('inf')

        print(f"\n[adaptation] НАЧАЛО: метод={method_func.__name__}, p={p}, eps={eps:.2e}, h_start={h}")
        print(f"[adaptation] Интервал: [{x0}, {xn}], y0={y0}")

        for iteration in range(max_iter):
            print(f"\n[adaptation] Итерация {iteration + 1}/{max_iter}, текущий h={h:.8f}")

            # Решаем с шагом h
            print(f"[adaptation] Решение с шагом h={h}...")
            xs, ys = method_func(f, x0, y0, xn, h)
            print(f"[adaptation] Готово: {len(xs)} точек, y_last={ys[-1]:.6f}")

            # Решаем с шагом h/2
            print(f"[adaptation] Решение с шагом h/2={h / 2}...")
            xs2, ys2 = method_func(f, x0, y0, xn, h / 2)
            print(f"[adaptation] Готово: {len(xs2)} точек, y_last={ys2[-1]:.6f}")

            # Берём значения в одинаковых узлах (каждый второй из мелкой сетки)
            ys2_coarse = ys2[::2]
            n = min(len(ys), len(ys2_coarse))
            print(f"[adaptation] Сравнение {n} точек")

            # Оценка погрешности по правилу Рунге
            errors = [abs(ys2_coarse[i] - ys[i]) for i in range(n)]
            max_error = max(errors) if errors else 0.0
            error = max_error / (2 ** p - 1)
            print(f"[adaptation] max_error={max_error:.6e}, error={error:.6e}")

            if error <= eps:
                print(f"[adaptation] УСПЕХ! Точность достигнута на итерации {iteration + 1}, h={h:.8f}")
                return xs, ys, h, error

            # Точность не достигнута — уменьшаем шаг
            print(f"[adaptation] Точность НЕ достигнута, уменьшаем h: {h:.8f} -> {h / 2:.8f}")
            h = h / 2
            print(f"[adaptation] Новый h={h:.8f}")

        # После всех итераций возвращаем последний результат
        print(f"[adaptation] Исчерпаны итерации ({max_iter}), возвращаем последний результат")
        xs, ys = method_func(f, x0, y0, xn, h)
        return xs, ys, h, error