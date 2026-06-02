import math

class ODE3:
    label = "y' = -2xy"
    @staticmethod
    def f(x: float, y: float) -> float:
        return -2 * x * y

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        # Решение: y = y0 * e^(-(x^2 - x0^2))
        return y0 * math.exp(-(x**2 - x0**2))

class ODE4:
    label = "y' = cos(x)"

    @staticmethod
    def f(x: float, y: float) -> float:
        return math.cos(x)

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        # Решение: y = y0 + sin(x) - sin(x0)
        return y0 + math.sin(x) - math.sin(x0)


class ODE8:
    label = "y' = 2xy + x³"

    @staticmethod
    def f(x: float, y: float) -> float:
        return 2 * x * y + x**3

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        # Решение: y = (y0 + (x0^2+1)/2) * e^(x^2-x0^2) - (x^2+1)/2
        return (y0 + (x0**2 + 1)/2) * math.exp(x**2 - x0**2) - (x**2 + 1)/2


class ODE9:
    label = "y' = sin(x) * y"

    @staticmethod
    def f(x: float, y: float) -> float:
        return math.sin(x) * y

    @staticmethod
    def exact(x: float, x0: float, y0: float) -> float:
        # Решение: y = y0 * e^(cos(x0) - cos(x))
        return y0 * math.exp(math.cos(x0) - math.cos(x))



ODE_LIST = [ ODE3, ODE4, ODE8, ODE9]