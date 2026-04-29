import tkinter as tk
from tkinter import ttk
import data.core as core
from views.diffs.finite import format_finite_table
from views.diffs.divided import format_divided_table
from views.plot import lines


class DiffsContainer(ttk.LabelFrame):  # Используем LabelFrame для рамки
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Таблицы разностей", relief="groove", borderwidth=2, **kwargs)

        # Фиксированная высота контейнера
        self.configure(height=300)
        self.pack_propagate(False)  # Запрещаем автоматическое изменение размера

        # Создаём вкладки
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Вкладка конечных разностей
        self.finite_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.finite_frame, text="Конечные разности")
        self._create_text_widget(self.finite_frame, "finite_text")

        # Вкладка разделённых разностей
        self.divided_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.divided_frame, text="Разделённые разности")
        self._create_text_widget(self.divided_frame, "divided_text")

        # Подписка на изменения
        core.subscribe(self.refresh)

        # Первая отрисовка
        self.refresh()

    def _create_text_widget(self, parent, name):
        """Создаёт текстовый виджет с прокруткой и рамкой"""
        # Фрейм с рамкой
        frame = ttk.Frame(parent, relief="sunken", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Текстовый виджет с моноширинным шрифтом
        text_widget = tk.Text(frame, wrap=tk.NONE, font=("Courier New", 10),
                              bg="white", relief="flat", borderwidth=0)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Горизонтальная прокрутка
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=text_widget.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.configure(xscrollcommand=h_scrollbar.set)

        # Вертикальная прокрутка
        v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=v_scrollbar.set)

        setattr(self, name, text_widget)

    def refresh(self):
        """Обновляет таблицы разностей"""
        # Проверяем автообновление
        if not core.get_auto_update():
            return

        # Получаем отсортированные узлы
        x_sorted, y_sorted = lines.get_sorted_valid_nodes(core)

        # Обновляем таблицу конечных разностей
        finite_text = format_finite_table(x_sorted, y_sorted)
        self._update_text_widget(self.finite_text, finite_text)

        # Обновляем таблицу разделённых разностей
        divided_text = format_divided_table(x_sorted, y_sorted)
        self._update_text_widget(self.divided_text, divided_text)

    def _update_text_widget(self, text_widget, content):
        """Обновляет содержимое текстового виджета"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)