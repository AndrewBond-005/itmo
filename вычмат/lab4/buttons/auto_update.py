# Константы автообновления

import tkinter as tk
from tkinter import ttk
BUTTON_AUTO_UPDATE_TEXT = "🔄 Автообновление"
BUTTON_AUTO_UPDATE_ACTIVE_COLOR = "#006697"
BUTTON_AUTO_UPDATE_INACTIVE_COLOR = "#a1a4a1"
BUTTON_PADDING = 5

# Настройки границы кнопки
BUTTON_BORDER_WIDTH = 2
BUTTON_ACTIVE_BORDER_COLOR = "#00ff00"
BUTTON_INACTIVE_BORDER_COLOR = "#3333FF"
BUTTON_RELIEF = tk.RIDGE




class AutoUpdateButton:
    """Класс для кнопки автообновления с состоянием."""

    def __init__(self, parent, table, graph, results_text, results_table, calc_callback):
        self.parent = parent
        self.table = table
        self.graph = graph
        self.results_text = results_text
        self.results_table = results_table
        self.calc_callback = calc_callback
        self.active = False

        self._create_button()

    def _create_button(self):
        """Создаёт кнопку автообновления."""
        self.btn = tk.Button(
            self.parent,
            text=BUTTON_AUTO_UPDATE_TEXT,
            bg=BUTTON_AUTO_UPDATE_INACTIVE_COLOR,
            fg="black",
            command=self._toggle,
            relief=BUTTON_RELIEF,
            bd=BUTTON_BORDER_WIDTH,
            padx=10,
            pady=2,
            highlightbackground=BUTTON_INACTIVE_BORDER_COLOR,
            highlightcolor=BUTTON_INACTIVE_BORDER_COLOR,
            highlightthickness=BUTTON_BORDER_WIDTH
        )
        self.btn.pack(pady=BUTTON_PADDING)

    def _toggle(self):
        """Переключает режим автообновления."""
        self.active = not self.active

        if self.active:
            self.btn.configure(
                bg=BUTTON_AUTO_UPDATE_ACTIVE_COLOR,
                highlightbackground=BUTTON_ACTIVE_BORDER_COLOR,
                highlightcolor=BUTTON_ACTIVE_BORDER_COLOR
            )
        else:
            self.btn.configure(
                bg=BUTTON_AUTO_UPDATE_INACTIVE_COLOR,
                highlightbackground=BUTTON_INACTIVE_BORDER_COLOR,
                highlightcolor=BUTTON_INACTIVE_BORDER_COLOR
            )

    def is_active(self):
        """Возвращает состояние автообновления."""
        return self.active


def setup_auto_update_button(parent, table, graph, results_text, results_table, calc_callback):
    """Создаёт и возвращает кнопку автообновления."""
    return AutoUpdateButton(parent, table, graph, results_text, results_table, calc_callback)