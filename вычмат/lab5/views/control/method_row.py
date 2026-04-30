import tkinter as tk
from tkinter import ttk
from views.plot.methods_state import methods_state


class MethodRow(ttk.Frame):
    """Один ряд в панели методов: чекбокс + поле вывода"""

    def __init__(self, parent, method_name, method_color, compute_func=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.method_name = method_name
        self.compute_func = compute_func
        self.current_value = None

        # Маппинг имён методов на функции в methods_state
        self.state_methods = {
            "Лагранж": "lagrange",
            "Ньютон (разд)": "newton_div",
            "Ньютон (кон)": "newton_fin",
            "Стирлинг": "stirling",
            "Бессель": "bessel"
        }

        state_key = self.state_methods.get(method_name, method_name.lower())

        # Получаем начальное состояние из methods_state
        initial_state = False
        if hasattr(methods_state, f"is_{state_key}_enabled"):
            initial_state = getattr(methods_state, f"is_{state_key}_enabled")()

        self.enabled = tk.BooleanVar(value=initial_state)

        self.pack(fill=tk.X, pady=2)

        # Чекбокс (слева)
        self.checkbox = ttk.Checkbutton(
            self,
            text=method_name,
            variable=self.enabled,
            command=self._on_toggle
        )
        self.checkbox.pack(side=tk.LEFT, padx=5)

        # Стрелка
        ttk.Label(self, text="→", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

        # Нередактируемое поле вывода (справа)
        self.value_var = tk.StringVar(value="—")
        self.value_entry = ttk.Entry(
            self,
            textvariable=self.value_var,
            state="readonly",
            width=12,
            justify=tk.RIGHT,
            font=("Courier", 9)
        )
        self.value_entry.pack(side=tk.LEFT, padx=5)
        self.value_entry.configure(foreground=method_color)

    def _on_toggle(self):
        """При изменении состояния чекбокса обновляем methods_state"""
        state_key = self.state_methods.get(self.method_name, self.method_name.lower())

        if hasattr(methods_state, f"set_{state_key}_enabled"):
            setter = getattr(methods_state, f"set_{state_key}_enabled")
            setter(self.enabled.get())

        # notify уже вызывается внутри setter'ов methods_state
        # core.notify() будет вызван через methods_state.notify()

    def is_enabled(self):
        return self.enabled.get()

    def update_value(self, value):
        self.current_value = value
        if value is None:
            self.value_var.set("—")
        else:
            self.value_var.set(f"{value:.6f}")

    def get_value(self):
        return self.current_value