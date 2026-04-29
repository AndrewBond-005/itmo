from tkinter import ttk
import tkinter as tk
from views.control.buttons.exit import ExitButton
from views.control.buttons.draw_mode import DrawModeButton
from views.control.buttons.method_lagrange import LagrangeButton
from views.control.buttons.method_newton_div import NewtonDivButton
from views.control.buttons.method_newton_fin import NewtonFinButton
from views.control.buttons.auto_update import AutoUpdateButton
from views.control.buttons.compute import ComputeButton
from views.control.inputs import XInput, FuncInput, AInput, BInput, NInput
from views.generate import GenerateButton
from views.control.messages.area import MessageArea


class ControlContainer(ttk.Frame):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, **kwargs)
        self.root_window = root_window

        # Область сообщений (с возможностью скрыть, установив height=0)
        self.message_area = MessageArea(self, height=3)
        self.message_area.pack(fill=tk.X, pady=(0, 2))

        # Строка 1: поле функции
        self.func_input = FuncInput(self)
        self.func_input.pack(fill=tk.X, pady=1)

        # Строка 2: a, b, n и кнопка генерации в одной строке
        gen_line = ttk.Frame(self)
        gen_line.pack(fill=tk.X, pady=1)

        self.a_input = AInput(gen_line)
        self.a_input.pack(side=tk.LEFT, padx=(0, 2))

        self.b_input = BInput(gen_line)
        self.b_input.pack(side=tk.LEFT, padx=2)

        self.n_input = NInput(gen_line)
        self.n_input.pack(side=tk.LEFT, padx=2)

        self.generate_btn = GenerateButton(gen_line, self.func_input, self.a_input,
                                           self.b_input, self.n_input, self.message_area)
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        # Строка 3: поле x и кнопка вычисления
        compute_line = ttk.Frame(self)
        compute_line.pack(fill=tk.X, pady=1)

        self.x_input = XInput(compute_line)
        self.x_input.pack(side=tk.LEFT, padx=(0, 5))

        self.compute_btn = ComputeButton(compute_line, self.x_input, self.message_area)
        self.compute_btn.pack(side=tk.LEFT)

        # Строка 4: режим рисования и автообновление в одной строке
        options_line = ttk.Frame(self)
        options_line.pack(fill=tk.X, pady=2)

        self.draw_mode_btn = DrawModeButton(options_line)
        self.draw_mode_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.auto_update_btn = AutoUpdateButton(options_line)
        self.auto_update_btn.pack(side=tk.LEFT)

        # Методы интерполяции - компактно в одну строку
        methods_label = ttk.Label(self, text="Методы:", font=("Arial", 9))
        methods_label.pack(anchor="w", pady=(3, 0))

        methods_line = ttk.Frame(self)
        methods_line.pack(fill=tk.X, pady=1)

        self.lagrange_btn = LagrangeButton(methods_line)
        self.lagrange_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.newton_div_btn = NewtonDivButton(methods_line)
        self.newton_div_btn.pack(side=tk.LEFT, padx=5)

        self.newton_fin_btn = NewtonFinButton(methods_line)
        self.newton_fin_btn.pack(side=tk.LEFT, padx=5)

        # Растягивающийся фрейм внизу (чтобы кнопка выхода была внизу)
        ttk.Frame(self).pack(expand=True, fill=tk.BOTH)

        # Кнопка выхода внизу
        exit_btn = ExitButton(self, self.root_window)
        exit_btn.pack(pady=2)

        # <---- ВОТ ЭТИ ДВЕ СТРОКИ ДОБАВЬ В КОНЕЦ ----->
        self.pack_propagate(False)  # Запрещаем автоматическое сжатие
        self.pack(fill=tk.BOTH, expand=True)  # Принудительно растягиваем

    def get_draw_mode_button(self):
        return self.draw_mode_btn

    def get_x_input(self):
        return self.x_input

    def get_compute_button(self):
        return self.compute_btn

    def set_message_height(self, height):
        """Позволяет настроить высоту области сообщений"""
        self.message_area.set_height(height)