# Константы режима добавления точек
BUTTON_POINT_MODE_TEXT = "📍 Режим точек"
BUTTON_POINT_MODE_ACTIVE_COLOR = "blue"
BUTTON_POINT_MODE_INACTIVE_COLOR = "gray"
BUTTON_PADDING = 5

import tkinter as tk
from tkinter import ttk


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
        self.style = ttk.Style()
        self.style.configure("PointMode.TButton", background=BUTTON_POINT_MODE_INACTIVE_COLOR)

        self.btn = ttk.Button(
            self.parent,
            text=BUTTON_POINT_MODE_TEXT,
            style="PointMode.TButton",
            command=self._toggle
        )
        self.btn.pack(pady=BUTTON_PADDING)

    def _toggle(self):
        """Переключает режим добавления точек."""
        self.active = not self.active

        if self.active:
            self.style.configure("PointMode.TButton", background=BUTTON_POINT_MODE_ACTIVE_COLOR)
            self.graph.enable_point_mode(self.table)
        else:
            self.style.configure("PointMode.TButton", background=BUTTON_POINT_MODE_INACTIVE_COLOR)
            self.graph.disable_point_mode()


def setup_point_mode_button(parent, graph, table):
    """Создаёт и возвращает кнопку режима добавления точек."""
    return PointModeButton(parent, graph, table)