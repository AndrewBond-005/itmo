# Константы кнопок
BUTTON_IMPORT_TEXT = "📂 Импорт"
BUTTON_EXPORT_TEXT = "💾 Экспорт"
BUTTON_PADDING = 5

import tkinter as tk
from tkinter import ttk
from filesio import FileIO


def setup_import_export_buttons(parent, table, results_text, results_table, get_max_points, warning_callback):
    """Создаёт кнопки импорта и экспорта."""
    frame = tk.Frame(parent)
    frame.pack(pady=BUTTON_PADDING)

    import_btn = tk.Button(
        frame,
        text=BUTTON_IMPORT_TEXT,
        bg="#f0f0f0",
        fg="black",
        command=lambda: FileIO.import_data(table, get_max_points(), warning_callback),
        relief=tk.RAISED,
        bd=2,
        padx=10,
        pady=2
    )
    import_btn.pack(side=tk.LEFT, padx=5)

    export_btn = tk.Button(
        frame,
        text=BUTTON_EXPORT_TEXT,
        bg="#f0f0f0",
        fg="black",
        command=lambda: FileIO.export_data(table, results_text, results_table),
        relief=tk.RAISED,
        bd=2,
        padx=10,
        pady=2
    )
    export_btn.pack(side=tk.LEFT, padx=5)

    return frame