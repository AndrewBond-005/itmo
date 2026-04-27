from tkinter import ttk
from views.control.buttons.exit import ExitButton
from views.control.buttons.draw_mode import DrawModeButton  # ДОБАВИТЬ эту строку


class ControlContainer(ttk.Frame):
    def __init__(self, parent, root_window, **kwargs):
        super().__init__(parent, **kwargs)
        self.root_window = root_window

        # ДОБАВИТЬ кнопку режима рисования
        self.draw_mode_btn = DrawModeButton(self)
        self.draw_mode_btn.pack(pady=10, padx=10, anchor="center")

        # Существующая кнопка выхода
        exit_btn = ExitButton(self, self.root_window)
        exit_btn.pack(pady=10, padx=10, anchor="center")

        ttk.Frame(self).pack(expand=True)

    def get_draw_mode_button(self):  # ДОБАВИТЬ этот метод
        """Возвращает кнопку режима рисования для передачи в график"""
        return self.draw_mode_btn