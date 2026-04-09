# Константы графика
from utils import parse_number, format_number

COLOR_POINTS = "red"
POINT_SIZE = 50
COLOR_LINE = "blue"
COLOR_AXIS = "black"
COLOR_GRID = "lightgray"
LINE_WIDTH = 2
FIXED_X_MIN = -5
FIXED_X_MAX = 15
FIXED_Y_MIN = -5
FIXED_Y_MAX = 15
FIGURE_SIZE = (6, 5)
DPI = 100

# Константы режима добавления точек
POINT_ADD_COLOR = "red"
POINT_ADD_SIZE = 60

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GraphWidget(tk.Frame):
    """Виджет для отображения графика matplotlib с панелью навигации."""

    def _on_scroll(self, event):
        """Обработчик прокрутки колёсика мыши - изменяет Y ближайшей точки."""
        if not self.point_mode or self.table is None:
            return

        # Проверяем что курсор в области осей
        if event.inaxes != self.axes:
            return

        # Получаем координаты курсора
        x_cursor, y_cursor = event.xdata, event.ydata

        # Получаем все валидные точки
        data = self.table.get_valid_data()
        if not data:
            return

        # Находим ближайшую точку к курсору
        min_dist = float('inf')
        nearest_row = None

        for item in data:
            dist = ((item['x'] - x_cursor) ** 2 + (item['y'] - y_cursor) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest_row = item['row']

        if nearest_row is not None:
            # Определяем направление и величину изменения
            delta = 0.1 if event.button == 'up' else -0.1

            # Изменяем Y ближайшей точки
            y_widget = self.table.grid_slaves(row=nearest_row, column=2)[0]
            if isinstance(y_widget, tk.Entry):
                current_y = parse_number(y_widget.get())
                if current_y is not None:
                    new_y = current_y + delta
                    y_widget.delete(0, tk.END)
                    y_widget.insert(0, format_number(new_y, 3))
                    self.table._on_data_changed()

    def __init__(self, parent):
        super().__init__(parent)
        self.points_plotted = False
        self.line_plotted = False
        self.point_mode = False
        self.table = None
        self._create_graph()
        self.canvas.mpl_connect('scroll_event', self._on_scroll)


    def _create_graph(self):
        """Создание фигуры, холста и панели навигации matplotlib."""
        # Создаём фигуру
        self.figure = Figure(figsize=FIGURE_SIZE, dpi=DPI)
        self.axes = self.figure.add_subplot(111)

        # Настройка осей и сетки
        self.axes.grid(True, color=COLOR_GRID, linestyle='-', linewidth=0.5)
        self.axes.axhline(y=0, color=COLOR_AXIS, linewidth=1)
        self.axes.axvline(x=0, color=COLOR_AXIS, linewidth=1)
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")

        # Фиксируем соотношение сторон
        self.axes.set_aspect('equal', adjustable='box')

        # Установка фиксированных начальных границ
        self.axes.set_xlim(FIXED_X_MIN, FIXED_X_MAX)
        self.axes.set_ylim(FIXED_Y_MIN, FIXED_Y_MAX)

        # Создаём фрейм для панели инструментов
        self.toolbar_frame = tk.Frame(self)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Создаём холст
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Добавляем панель навигации matplotlib
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

        self.figure.tight_layout()

    def enable_point_mode(self, table):
        """Включает режим добавления точек кликом на график."""
        self.point_mode = True
        self.table = table
        # Привязываем обработчики кликов
        self.click_cid = self.canvas.mpl_connect('button_press_event', self._on_click)

    def disable_point_mode(self):
        """Выключает режим добавления точек."""
        self.point_mode = False
        self.table = None
        # Отвязываем обработчики
        if hasattr(self, 'click_cid'):
            self.canvas.mpl_disconnect(self.click_cid)

    def _on_click(self, event):
        """Обработчик клика по графику."""
        if not self.point_mode or self.table is None:
            return

        # Проверяем что клик был в области осей
        if event.inaxes != self.axes:
            return

        # Игнорируем клики если курсор над тулбаром
        toolbar_widget = self.toolbar_frame
        try:
            widget_under_cursor = toolbar_widget.winfo_containing(event.x, event.y)
            if widget_under_cursor is not None:
                # Проверяем, является ли виджет частью тулбара
                parent = widget_under_cursor
                while parent is not None:
                    if parent == toolbar_widget:
                        return
                    parent = parent.master
        except:
            pass

        x, y = event.xdata, event.ydata

        # ЛКМ (button 1) - добавить точку
        if event.button == 1:
            self.table.add_point(x, y)
        # ПКМ (button 3) - удалить последнюю точку
        elif event.button == 3:
            self.table.remove_last_point()
        elif event.button == 2:
            self._remove_nearest_point(x, y)
    def plot_points_only(self, x_values, y_values):
        """Рисует только точки, очищая предыдущий график."""
        # Сохраняем текущие границы перед очисткой
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        # Очищаем график
        self.axes.clear()

        # Восстанавливаем сетку и оси
        self.axes.grid(True, color=COLOR_GRID, linestyle='-', linewidth=0.5)
        self.axes.axhline(y=0, color=COLOR_AXIS, linewidth=1)
        self.axes.axvline(x=0, color=COLOR_AXIS, linewidth=1)
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")

        # Восстанавливаем фиксированное соотношение сторон
        self.axes.set_aspect('equal', adjustable='box')

        # Восстанавливаем границы
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

        # Рисуем точки если они есть
        if x_values and y_values:
            self.axes.scatter(x_values, y_values, color=COLOR_POINTS, s=POINT_SIZE, zorder=5)
            self.points_plotted = True
        else:
            self.points_plotted = False
            self.line_plotted = False

        self.canvas.draw()

    def plot_points(self, x_values, y_values):
        """Рисует красные кружочки точек."""
        if not x_values or not y_values:
            return

        self.axes.scatter(x_values, y_values, color=COLOR_POINTS, s=POINT_SIZE, zorder=5)
        self.points_plotted = True
        self.canvas.draw()

    def plot_function(self, x_range, y_values, color=COLOR_LINE):
        """Рисует линию функции, не меняя границы."""
        if not x_range or not y_values:
            return

        self.axes.plot(x_range, y_values, color=color, linewidth=LINE_WIDTH, zorder=4)
        self.line_plotted = True
        self.canvas.draw()

    def clear(self):
        """Очищает график, оставляя сетку и оси."""
        # Сохраняем текущие границы
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        self.axes.clear()

        # Восстанавливаем сетку и оси
        self.axes.grid(True, color=COLOR_GRID, linestyle='-', linewidth=0.5)
        self.axes.axhline(y=0, color=COLOR_AXIS, linewidth=1)
        self.axes.axvline(x=0, color=COLOR_AXIS, linewidth=1)
        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")

        # Восстанавливаем фиксированное соотношение сторон
        self.axes.set_aspect('equal', adjustable='box')

        # Восстанавливаем границы
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)

        self.points_plotted = False
        self.line_plotted = False

    def reset_view(self):
        """Возвращает к фиксированным начальным границам."""
        self.axes.set_xlim(FIXED_X_MIN, FIXED_X_MAX)
        self.axes.set_ylim(FIXED_Y_MIN, FIXED_Y_MAX)
        self.axes.set_aspect('equal', adjustable='box')
        self.canvas.draw()

    def _remove_nearest_point(self, x, y):
        """Удаляет точку, ближайшую к координатам (x, y)."""
        data = self.table.get_valid_data()
        if not data:
            return

        # Находим ближайшую точку
        min_dist = float('inf')
        nearest_row = None

        for item in data:
            dist = ((item['x'] - x) ** 2 + (item['y'] - y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest_row = item['row']

        if nearest_row is not None:
            # Удаляем данные из найденной строки
            x_widget = self.table.grid_slaves(row=nearest_row, column=1)[0]
            y_widget = self.table.grid_slaves(row=nearest_row, column=2)[0]
            phi_widget = self.table.grid_slaves(row=nearest_row, column=3)[0]
            eps_widget = self.table.grid_slaves(row=nearest_row, column=4)[0]

            if isinstance(x_widget, tk.Entry):
                x_widget.delete(0, tk.END)
            if isinstance(y_widget, tk.Entry):
                y_widget.delete(0, tk.END)
            if isinstance(phi_widget, tk.Label):
                phi_widget.configure(text="")
            if isinstance(eps_widget, tk.Label):
                eps_widget.configure(text="")

            self.table._on_data_changed()
