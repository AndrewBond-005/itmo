# Константы управления графиком
BUTTON_ZOOM_IN_TEXT = "➕"
BUTTON_ZOOM_OUT_TEXT = "➖"
BUTTON_PAN_LEFT_TEXT = "⬅️"
BUTTON_PAN_RIGHT_TEXT = "➡️"
BUTTON_PAN_UP_TEXT = "⬆️"
BUTTON_PAN_DOWN_TEXT = "⬇️"
BUTTON_RESET_TEXT = "🔄 Сброс"
BUTTON_WIDTH = 3
BUTTON_PADDING = 2

import tkinter as tk
from tkinter import ttk


def setup_graph_controls(parent, graph):
    """
    Создаёт панель кнопок управления графиком.
    Возвращает frame с кнопками.
    """
    control_frame = tk.Frame(parent)

    # Первая строка: Зум
    zoom_frame = tk.Frame(control_frame)
    zoom_frame.pack(pady=BUTTON_PADDING)

    tk.Label(zoom_frame, text="Зум:").pack(side=tk.LEFT, padx=5)

    zoom_in_btn = tk.Button(
        zoom_frame,
        text=BUTTON_ZOOM_IN_TEXT,
        width=BUTTON_WIDTH,
        command=graph.zoom_in
    )
    zoom_in_btn.pack(side=tk.LEFT, padx=2)

    zoom_out_btn = tk.Button(
        zoom_frame,
        text=BUTTON_ZOOM_OUT_TEXT,
        width=BUTTON_WIDTH,
        command=graph.zoom_out
    )
    zoom_out_btn.pack(side=tk.LEFT, padx=2)

    # Вторая строка: Панорама
    pan_frame = tk.Frame(control_frame)
    pan_frame.pack(pady=BUTTON_PADDING)

    tk.Label(pan_frame, text="Сдвиг:").pack(side=tk.LEFT, padx=5)

    pan_left_btn = tk.Button(
        pan_frame,
        text=BUTTON_PAN_LEFT_TEXT,
        width=BUTTON_WIDTH,
        command=graph.pan_left
    )
    pan_left_btn.pack(side=tk.LEFT, padx=2)

    pan_right_btn = tk.Button(
        pan_frame,
        text=BUTTON_PAN_RIGHT_TEXT,
        width=BUTTON_WIDTH,
        command=graph.pan_right
    )
    pan_right_btn.pack(side=tk.LEFT, padx=2)

    pan_up_btn = tk.Button(
        pan_frame,
        text=BUTTON_PAN_UP_TEXT,
        width=BUTTON_WIDTH,
        command=graph.pan_up
    )
    pan_up_btn.pack(side=tk.LEFT, padx=2)

    pan_down_btn = tk.Button(
        pan_frame,
        text=BUTTON_PAN_DOWN_TEXT,
        width=BUTTON_WIDTH,
        command=graph.pan_down
    )
    pan_down_btn.pack(side=tk.LEFT, padx=2)

    # Третья строка: Сброс
    reset_frame = tk.Frame(control_frame)
    reset_frame.pack(pady=BUTTON_PADDING)

    reset_btn = tk.Button(
        reset_frame,
        text=BUTTON_RESET_TEXT,
        command=graph.reset_view
    )
    reset_btn.pack()

    return control_frame