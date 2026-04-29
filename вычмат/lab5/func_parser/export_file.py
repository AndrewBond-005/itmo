import tkinter as tk
from tkinter import filedialog
import data.core as core


def export_to_file(message_area):
    """
    Открывает диалог сохранения файла и сохраняет текущие узлы

    Returns:
        bool: True при успехе, False при ошибке
    """
    x_list = core.get_x()
    y_list = core.get_y()

    # Собираем только валидные точки
    points = []
    for x, y in zip(x_list, y_list):
        if x is not None and y is not None:
            points.append((x, y))

    if not points:
        message_area.add_message("Нет данных для экспорта (нет введённых точек)", "warning")
        return False

    file_path = filedialog.asksaveasfilename(
        title="Сохранить узлы в файл",
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt"), ("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
    )

    if not file_path:
        return False

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for x, y in points:
                f.write(f"{x:.3f} {y:.3f}\n")

        message_area.add_message(f"Экспортировано {len(points)} точек в файл {file_path}", "info")
        return True

    except Exception as e:
        message_area.add_message(f"Ошибка сохранения файла: {e}", "error")
        return False