import tkinter as tk
from tkinter import filedialog


def import_from_file(message_area):
    """
    Открывает диалог выбора файла и читает точки

    Returns:
        tuple: (x_list, y_list) или (None, None) при ошибке или отмене
    """
    file_path = filedialog.askopenfilename(
        title="Выберите файл с узлами",
        filetypes=[("Текстовые файлы", "*.txt"), ("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
    )

    if not file_path:
        return None, None

    x_list = []
    y_list = []
    line_num = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue

                # Разделяем пробелами, табуляцией или запятой
                parts = line.replace(',', ' ').split()
                if len(parts) < 2:
                    message_area.add_message(f"Строка {line_num}: пропущена (не два числа)", "warning")
                    continue

                try:
                    x = float(parts[0].replace(',', '.'))
                    y = float(parts[1].replace(',', '.'))
                    x_list.append(x)
                    y_list.append(y)
                except ValueError:
                    message_area.add_message(f"Строка {line_num}: пропущена (нечисловые значения)", "warning")
                    continue

        if not x_list:
            message_area.add_message("В файле не найдено корректных строк", "error")
            return None, None

        message_area.add_message(f"Прочитано {len(x_list)} точек из файла", "info")
        return x_list, y_list

    except Exception as e:
        message_area.add_message(f"Ошибка чтения файла: {e}", "error")
        return None, None