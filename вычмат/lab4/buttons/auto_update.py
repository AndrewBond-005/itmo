# Константы автообновления
BUTTON_AUTO_UPDATE_TEXT = "🔄 Автообновление"
BUTTON_AUTO_UPDATE_ACTIVE_COLOR = "green"
BUTTON_AUTO_UPDATE_INACTIVE_COLOR = "gray"
BUTTON_PADDING = 5

import tkinter as tk
from tkinter import ttk


class AutoUpdateButton:
    """Класс для кнопки автообновления с состоянием."""

    def __init__(self, parent, table, graph, results_text, calc_callback):
        self.parent = parent
        self.table = table
        self.graph = graph
        self.results_text = results_text
        self.calc_callback = calc_callback
        self.active = False

        self._create_button()

    def _create_button(self):
        """Создаёт кнопку автообновления."""
        self.btn = tk.Button(
            self.parent,
            text=BUTTON_AUTO_UPDATE_TEXT,
            bg=BUTTON_AUTO_UPDATE_INACTIVE_COLOR,
            command=self._toggle,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=2
        )
        self.btn.pack(pady=BUTTON_PADDING)

    def _toggle(self):
        """Переключает режим автообновления."""
        self.active = not self.active

        if self.active:
            self.btn.configure(bg=BUTTON_AUTO_UPDATE_ACTIVE_COLOR)
            # Проверяем текущие данные
            self._check_and_update()
        else:
            self.btn.configure(bg=BUTTON_AUTO_UPDATE_INACTIVE_COLOR)

    def is_active(self):
        """Возвращает состояние автообновления."""
        return self.active

    def _check_and_update(self):
        """Проверяет количество точек и вызывает пересчёт."""
        if self.active:  # Проверяем только если активно
            if self.table.get_valid_count() >= 4:
                self.calc_callback()
            else:
                # Просто обновляем текст результатов
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Недостаточно точек для автообновления\n(нужно ≥4)", "warning")
                self.results_text.tag_config("warning", foreground="orange")


def setup_auto_update_button(parent, table, graph, results_text, calc_callback):
    """Создаёт и возвращает кнопку автообновления."""
    return AutoUpdateButton(parent, table, graph, results_text, calc_callback)