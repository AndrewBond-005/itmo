import tkinter as tk
from tkinter import ttk


class MethodRow(ttk.Frame):
    """Один ряд в панели методов: чекбокс + поле вывода"""

    def __init__(self, parent, method_name, method_color, compute_func=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.method_name = method_name
        self.compute_func = compute_func
        self.enabled = tk.BooleanVar(value=True)
        self.current_value = None

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

        # Цвет текста поля (опционально)
        self.value_entry.configure(foreground=method_color)

    def _on_toggle(self):
        """При изменении состояния чекбокса"""
        from data import core
        core.notify()

    def is_enabled(self):
        return self.enabled.get()

    def update_value(self, value):
        """Обновляет отображаемое значение"""
        self.current_value = value
        if value is None:
            self.value_var.set("—")
        else:
            self.value_var.set(f"{value:.6f}")

    def get_value(self):
        return self.current_value