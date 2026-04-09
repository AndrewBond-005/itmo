# Константы режимов
MODE_8_12_TEXT = "Режим 8-12 точек"
MODE_4_15_TEXT = "Режим 4-15 точек"
MODE_8_12_MIN = 8
MODE_8_12_MAX = 12
MODE_4_15_MIN = 4
MODE_4_15_MAX = 15
BUTTON_PADDING = 5

import tkinter as tk
from tkinter import ttk


class ModeToggleButton:
    """Класс для кнопки переключения режима."""

    def __init__(self, parent, table, warning_callback):
        self.parent = parent
        self.table = table
        self.warning_callback = warning_callback
        self.mode_8_12 = True  # True = 8-12, False = 4-15

        self._create_button()

    def _create_button(self):
        """Создаёт кнопку переключения режима."""
        self.btn = tk.Button(
            self.parent,
            text=MODE_8_12_TEXT,
            bg="#f0f0f0",
            fg="black",
            command=self._toggle,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=2
        )
        self.btn.pack(side=tk.RIGHT, padx=5, pady=BUTTON_PADDING)

        self.label = tk.Label(
            self.parent,
            text=f"Текущий режим: 8-12 точек",
            font=('Arial', 9)
        )
        self.label.pack(side=tk.RIGHT, padx=5)

    def _toggle(self):
        """Переключает режим."""
        self.mode_8_12 = not self.mode_8_12

        if self.mode_8_12:
            self.btn.configure(text=MODE_8_12_TEXT)
            self.label.configure(text="Текущий режим: 8-12 точек")
            self.table.set_row_count(12)
        else:
            self.btn.configure(text=MODE_4_15_TEXT)
            self.label.configure(text="Текущий режим: 4-15 точек")
            self.table.set_row_count(15)

    def get_min_points(self):
        """Возвращает минимальное количество точек для текущего режима."""
        return MODE_8_12_MIN if self.mode_8_12 else MODE_4_15_MIN

    def get_max_points(self):
        """Возвращает максимальное количество точек для текущего режима."""
        return MODE_8_12_MAX if self.mode_8_12 else MODE_4_15_MAX


def setup_mode_toggle(parent, table, warning_callback):
    """Создаёт и возвращает кнопку переключения режима."""
    return ModeToggleButton(parent, table, warning_callback)