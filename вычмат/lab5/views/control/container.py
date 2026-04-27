from tkinter import ttk
from views.control.buttons.exit import ExitButton
from views.control.buttons.draw_mode import DrawModeButton
from views.control.buttons.method_lagrange import LagrangeButton
from views.control.buttons.method_newton_div import NewtonDivButton
from views.control.buttons.method_newton_fin import NewtonFinButton


class ControlContainer(ttk.Frame):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, **kwargs)
        self.root_window = root_window

        # Рамка для методов интерполяции
        methods_frame = ttk.LabelFrame(self, text="Методы интерполяции", relief="groove")
        methods_frame.pack(pady=10, padx=10, fill="x")

        # Кнопки методов
        self.lagrange_btn = LagrangeButton(methods_frame)
        self.lagrange_btn.pack(pady=5, padx=10, anchor="w")

        self.newton_div_btn = NewtonDivButton(methods_frame)
        self.newton_div_btn.pack(pady=5, padx=10, anchor="w")

        self.newton_fin_btn = NewtonFinButton(methods_frame)
        self.newton_fin_btn.pack(pady=5, padx=10, anchor="w")

        # Кнопка режима рисования
        self.draw_mode_btn = DrawModeButton(self)
        self.draw_mode_btn.pack(pady=10, padx=10, anchor="center")

        # Кнопка выхода
        exit_btn = ExitButton(self, self.root_window)
        exit_btn.pack(pady=10, padx=10, anchor="center")

        ttk.Frame(self).pack(expand=True)

    def get_draw_mode_button(self):
        """Возвращает кнопку режима рисования для передачи в график"""
        return self.draw_mode_btn