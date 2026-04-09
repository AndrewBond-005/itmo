# Константы режима добавления точек

import tkinter as tk
from tkinter import ttk
BUTTON_POINT_MODE_TEXT = "Поставить точки"
BUTTON_POINT_MODE_ACTIVE_COLOR = "#006697"
BUTTON_POINT_MODE_INACTIVE_COLOR = "#a1a4a1"
BUTTON_PADDING = 5

# Настройки границы кнопки режима точек
BUTTON_POINT_BORDER_WIDTH = 2
BUTTON_POINT_ACTIVE_BORDER_COLOR = "#00ff00"
BUTTON_POINT_INACTIVE_BORDER_COLOR = "#333333"
BUTTON_POINT_RELIEF = tk.RIDGE




class PointModeButton:
    """Класс для кнопки режима добавления точек."""

    def __init__(self, parent, graph, table):
        self.parent = parent
        self.graph = graph
        self.table = table
        self.active = False

        self._create_button()

    def _create_button(self):
        """Создаёт кнопку режима точек."""
        self.btn = tk.Button(
            self.parent,
            text=BUTTON_POINT_MODE_TEXT,
            bg=BUTTON_POINT_MODE_INACTIVE_COLOR,
            fg="black",
            command=self._toggle,
            relief=BUTTON_POINT_RELIEF,
            bd=BUTTON_POINT_BORDER_WIDTH,
            padx=10,
            pady=2,
            highlightbackground=BUTTON_POINT_INACTIVE_BORDER_COLOR,
            highlightcolor=BUTTON_POINT_INACTIVE_BORDER_COLOR,
            highlightthickness=BUTTON_POINT_BORDER_WIDTH,
            activebackground=BUTTON_POINT_MODE_ACTIVE_COLOR,
            activeforeground="black"
        )
        self.btn.pack(pady=BUTTON_PADDING)

    def _toggle(self):
        """Переключает режим добавления точек."""
        self.active = not self.active

        if self.active:
            self.btn.configure(
                bg=BUTTON_POINT_MODE_ACTIVE_COLOR,
                highlightbackground=BUTTON_POINT_ACTIVE_BORDER_COLOR,
                highlightcolor=BUTTON_POINT_ACTIVE_BORDER_COLOR,
                activebackground=BUTTON_POINT_MODE_ACTIVE_COLOR
            )
            self.graph.enable_point_mode(self.table)
        else:
            self.btn.configure(
                bg=BUTTON_POINT_MODE_INACTIVE_COLOR,
                highlightbackground=BUTTON_POINT_INACTIVE_BORDER_COLOR,
                highlightcolor=BUTTON_POINT_INACTIVE_BORDER_COLOR,
                activebackground=BUTTON_POINT_MODE_ACTIVE_COLOR
            )
            self.graph.disable_point_mode()


def setup_point_mode_button(parent, graph, table):
    """Создаёт и возвращает кнопку режима добавления точек."""
    return PointModeButton(parent, graph, table)