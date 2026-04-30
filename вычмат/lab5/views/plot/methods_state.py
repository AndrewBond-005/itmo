class MethodsState:
    """Состояние включения/выключения методов интерполяции"""

    def __init__(self):
        self.lagrange_enabled = True
        self.newton_div_enabled = True
        self.newton_fin_enabled = True
        self.stirling_enabled = True
        self.bessel_enabled = True
        self.callbacks = []

    def subscribe(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def notify(self):
        for callback in self.callbacks:
            callback()

    # Лагранж
    def is_lagrange_enabled(self):
        return self.lagrange_enabled

    def set_lagrange_enabled(self, state):
        self.lagrange_enabled = state
        self.notify()

    # Ньютон (разд)
    def is_newton_div_enabled(self):
        return self.newton_div_enabled

    def set_newton_div_enabled(self, state):
        self.newton_div_enabled = state
        self.notify()

    # Ньютон (кон)
    def is_newton_fin_enabled(self):
        return self.newton_fin_enabled

    def set_newton_fin_enabled(self, state):
        self.newton_fin_enabled = state
        self.notify()

    # Стирлинг
    def is_stirling_enabled(self):
        return self.stirling_enabled

    def set_stirling_enabled(self, state):
        self.stirling_enabled = state
        self.notify()

    # Бессель
    def is_bessel_enabled(self):
        return self.bessel_enabled

    def set_bessel_enabled(self, state):
        self.bessel_enabled = state
        self.notify()


# Глобальный экземпляр состояния
methods_state = MethodsState()