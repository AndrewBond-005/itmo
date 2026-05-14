from tkinter import ttk
import tkinter as tk
from views.control.buttons.exit import ExitButton
from views.control.buttons.draw_mode import DrawModeButton
from views.control.buttons.auto_update import AutoUpdateButton
from views.control.buttons.compute import ComputeButton
from views.control.buttons.import_btn import ImportButton
from views.control.buttons.export_btn import ExportButton
from views.control.buttons.help_btn import HelpButton
from views.control.methods_panel import MethodsPanel
from views.control.inputs import XInput, FuncInput, AInput, BInput, NInput
from views.generate import GenerateButton
from views.control.messages.area import MessageArea


class ControlContainer(ttk.Frame):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, **kwargs)
        self.root_window = root_window

        # СНАЧАЛА создаём область сообщений
        self.message_area = MessageArea(self, height=3)
        self.message_area.pack(fill=tk.X, pady=(0, 2))

        # Разделитель
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5)

        # Верхняя строка: импорт, экспорт, помощь, выход
        top_line = ttk.Frame(self)
        top_line.pack(fill=tk.X, pady=(0, 5))

        self.import_btn = ImportButton(top_line, self.message_area)
        self.import_btn.pack(side=tk.LEFT, padx=2)

        # ExportButton будет создан ПОЗЖЕ, когда будет methods_panel
        self.export_btn = None
        self.help_btn = HelpButton(top_line)
        self.help_btn.pack(side=tk.LEFT, padx=2)

        exit_btn = ExitButton(top_line, self.root_window)
        exit_btn.pack(side=tk.LEFT, padx=2)

        # Разделитель
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5)

        # Строка 1: поле функции
        self.func_input = FuncInput(self)
        self.func_input.pack(fill=tk.X, pady=1)

        # Строка 2: a, b, n и кнопка генерации
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

        # Строка 4: режим рисования и автообновление
        options_line = ttk.Frame(self)
        options_line.pack(fill=tk.X, pady=2)

        self.draw_mode_btn = DrawModeButton(options_line)
        self.draw_mode_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.auto_update_btn = AutoUpdateButton(options_line)
        self.auto_update_btn.pack(side=tk.LEFT)

        # Разделитель
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5)

        # Панель методов (вертикальная с полями вывода)
        self.methods_panel = MethodsPanel(self)
        self.methods_panel.pack(fill=tk.X, pady=5)

        # ТЕПЕРЬ создаём ExportButton с methods_panel
        if self.export_btn is None:
            self.export_btn = ExportButton(top_line, self.message_area, self.methods_panel)
            self.export_btn.pack(side=tk.LEFT, padx=2, before=self.help_btn)

        # Передаём methods_panel в compute_btn
        self.compute_btn.set_methods_panel(self.methods_panel)

        # Растягивающийся фрейм
        ttk.Frame(self).pack(expand=True, fill=tk.BOTH)

    def get_draw_mode_button(self):
        return self.draw_mode_btn

    def get_x_input(self):
        return self.x_input

    def get_compute_button(self):
        return self.compute_btn

    def get_methods_panel(self):
        return self.methods_panel

    def set_message_height(self, height):
        self.message_area.set_height(height)