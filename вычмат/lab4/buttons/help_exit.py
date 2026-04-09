# Константы кнопок
BUTTON_HELP_TEXT = "❓Помощь"
BUTTON_EXIT_TEXT = "Выход"
BUTTON_PADDING = 5

HELP_TEXT = """Как работать с программой:

1. Ввод данных:
   - Клик по ячейке x или y
   - Введите число (точка или запятая)
   - Enter или клик вне ячейки - сохранение

2. Добавление точек на график:
   - Нажмите кнопку "Режим точек"
   - ЛКМ на график - добавить точку
   - ПКМ на график - удалить последнюю точку

3. Управление графиком:
   - 🏠 - вернуться к начальному виду
   - 🔍 - выделить область для увеличения
   - ✋ - перемещать график

4. Вычисление:
   - Нажмите "Вычислить" или включите автообновление
   - При автообновлении расчёт происходит автоматически

5. Импорт/Экспорт:
   - Импорт: текстовый файл с парами x y через пробел
   - Экспорт: сохраняет таблицу и результаты

6. Переключение режима:
   - 8-12 точек - минимально 8, максимально 12
   - 4-15 точек - минимально 4, максимально 15"""

import tkinter as tk
from tkinter import ttk, messagebox


def setup_help_exit(parent, root):
    """Создаёт кнопки помощи и выхода."""
    frame = tk.Frame(parent)
    frame.pack(pady=BUTTON_PADDING)

    help_btn = tk.Button(
        frame,
        text=BUTTON_HELP_TEXT,
        bg="#f0f0f0",
        fg="black",
        command=lambda: messagebox.showinfo("Помощь", HELP_TEXT),
        relief=tk.RAISED,
        bd=2,
        padx=10,
        pady=2
    )
    help_btn.pack(side=tk.LEFT, padx=5)

    exit_btn = tk.Button(
        frame,
        text=BUTTON_EXIT_TEXT,
        bg="#ff1600",
        fg="black",
        command=root.quit,
        relief=tk.RAISED,
        bd=2,
        padx=10,
        pady=2
    )
    exit_btn.pack(side=tk.LEFT, padx=5)

    return frame