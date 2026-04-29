import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import data.core as core
from utils.const import CLICK_EPSILON, SCROLL_STEP, COLOR_LAGRANGE, COLOR_NEWTON_DIV, COLOR_NEWTON_FIN, LINE_WIDTH, \
    LINE_STYLE
from views.plot.methods_state import methods_state
from views.plot import lines


class PlotCanvas(tk.Frame):
    def __init__(self, parent, draw_mode_button, x_range=(-5, 15), y_range=(-5, 15)):
        super().__init__(parent)
        self.parent = parent
        self.draw_mode_button = draw_mode_button
        self.x_range = x_range
        self.y_range = y_range
        self.point_mode = False
        self.table = None
        self.x_input = None
        self.compute_button = None

        # Создаём фрейм для тулбара
        self.toolbar_frame = tk.Frame(self)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Создаём фигуру
        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.axes = self.figure.add_subplot(111)

        # Настройка осей
        self.axes.set_xlim(self.x_range[0], self.x_range[1])
        self.axes.set_ylim(self.y_range[0], self.y_range[1])
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.axes.set_title("Узлы интерполяции")
        self.axes.grid(True, linestyle='--', alpha=0.7)
        self.axes.axhline(y=0, color='black', linewidth=1.5)
        self.axes.axvline(x=0, color='black', linewidth=1.5)

        # Создаём холст
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Добавляем тулбар
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

        # Подключаем события
        self.canvas.mpl_connect('button_press_event', self._on_click)
        self.canvas.mpl_connect('scroll_event', self._on_scroll)

        # Подписки
        core.subscribe(self.refresh)
        methods_state.subscribe(self.refresh)

        # Первая отрисовка
        self.refresh()

    def enable_point_mode(self, table):
        self.point_mode = True
        self.table = table

    def disable_point_mode(self):
        self.point_mode = False
        self.table = None

    def set_x_input(self, x_input):
        """Устанавливает ссылку на поле ввода x для СКМ"""
        self.x_input = x_input

    def set_compute_button(self, compute_button):
        """Устанавливает ссылку на кнопку вычисления для СКМ"""
        self.compute_button = compute_button

    def _on_click(self, event):
        if not self.draw_mode_button.is_active():
            return
        if event.inaxes != self.axes:
            return

        # Проверка клика по тулбару
        try:
            toolbar_widget = self.toolbar_frame
            widget_under_cursor = toolbar_widget.winfo_containing(event.x, event.y)
            if widget_under_cursor is not None:
                parent = widget_under_cursor
                while parent is not None:
                    if parent == toolbar_widget:
                        return
                    parent = parent.master
        except:
            pass

        if event.button == 1:  # ЛКМ - добавление точки
            self._add_point(event.xdata, event.ydata)
        elif event.button == 3:  # ПКМ - удаление ближайшей точки
            self._delete_nearest(event.xdata, event.ydata)
        elif event.button == 2:  # СКМ - выбор абсциссы
            x_click = event.xdata
            print(f"СКМ: выбрана абсцисса {x_click:.6f}")

            # Устанавливаем значение в поле ввода x
            if self.x_input:
                self.x_input.set_value(x_click)

            # Автоматически вызываем вычисление
            if self.compute_button:
                self.compute_button._compute()

    def _on_scroll(self, event):
        if not self.draw_mode_button.is_active():
            return
        if event.inaxes != self.axes:
            return

        idx, dist = self._find_nearest(event.xdata, event.ydata)
        if idx != -1 and dist < CLICK_EPSILON:
            current_y = core.get_y()[idx]
            if current_y is not None:
                delta = SCROLL_STEP if event.step > 0 else -SCROLL_STEP
                core.update_y(idx, current_y + delta)

    def _add_point(self, x, y):
        x_list = core.get_x()
        y_list = core.get_y()

        # Ищем пустую или неполную строку
        for i in range(len(x_list)):
            if x_list[i] is None or y_list[i] is None:
                core.update_x(i, x)
                core.update_y(i, y)
                return

        # Все строки полные - добавляем новую
        core.add_point(x, y)

    def _delete_nearest(self, x, y):
        idx, dist = self._find_nearest(x, y)
        if idx != -1 and dist < CLICK_EPSILON:
            core.delete_point(idx)

    def _find_nearest(self, x, y):
        x_list = core.get_x()
        y_list = core.get_y()
        min_dist = float('inf')
        min_idx = -1

        for i in range(len(x_list)):
            if x_list[i] is None or y_list[i] is None:
                continue
            dist = ((x_list[i] - x) ** 2 + (y_list[i] - y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                min_idx = i

        return min_idx, min_dist

    def _is_method_active(self, method_name):
        """Проверяет, активен ли метод"""
        if method_name == "lagrange":
            return methods_state.is_lagrange_enabled()
        elif method_name == "newton_div":
            return methods_state.is_newton_div_enabled()
        elif method_name == "newton_fin":
            return methods_state.is_newton_fin_enabled()
        return False

    def _get_method_color(self, method_name):
        """Возвращает цвет для метода"""
        if method_name == "lagrange":
            return COLOR_LAGRANGE
        elif method_name == "newton_div":
            return COLOR_NEWTON_DIV
        elif method_name == "newton_fin":
            return COLOR_NEWTON_FIN
        return "black"

    def _draw_computed_points(self):
        """Рисует вычисленные точки"""
        x = core.get_compute_x()
        if x is None:
            return

        values = core.get_computed_values()
        if not values:
            return

        for method_name, y in values.items():
            if y is None:
                continue
            if not self._is_method_active(method_name):
                continue
            color = self._get_method_color(method_name)
            self.axes.plot(x, y, marker='*', color=color, markersize=12,
                           linestyle='none', zorder=6)

    def refresh(self):
        """Перерисовка графика"""
        # Сохраняем границы
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        # Очищаем оси
        self.axes.clear()

        # Восстанавливаем базовые элементы
        self.axes.set_xlim(xlim)
        self.axes.set_ylim(ylim)
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("y")
        self.axes.set_title("Узлы интерполяции")
        self.axes.grid(True, linestyle='--', alpha=0.7)
        self.axes.axhline(y=0, color='black', linewidth=1.5)
        self.axes.axvline(x=0, color='black', linewidth=1.5)

        # Рисуем линии интерполяции ТОЛЬКО если включено автообновление
        if core.get_auto_update():
            x_sorted, y_sorted = lines.get_sorted_valid_nodes(core)
            if len(x_sorted) >= 2:
                x_grid = lines.build_grid(x_sorted)

                if methods_state.is_lagrange_enabled():
                    y_grid = lines.compute_lagrange_line(x_grid, x_sorted, y_sorted)
                    if y_grid:
                        self.axes.plot(x_grid, y_grid, color=COLOR_LAGRANGE,
                                       linewidth=LINE_WIDTH, label="Лагранж")

                if methods_state.is_newton_div_enabled():
                    y_grid = lines.compute_newton_div_line(x_grid, x_sorted, y_sorted)
                    if y_grid:
                        self.axes.plot(x_grid, y_grid, color=COLOR_NEWTON_DIV,
                                       linewidth=LINE_WIDTH, label="Ньютон (разд)")

                if methods_state.is_newton_fin_enabled():
                    y_grid = lines.compute_newton_fin_line(x_grid, x_sorted, y_sorted)
                    if y_grid:
                        self.axes.plot(x_grid, y_grid, color=COLOR_NEWTON_FIN,
                                       linewidth=LINE_WIDTH, label="Ньютон (кон)")

                self.axes.legend(loc='upper left')

        # Рисуем точки (всегда)
        points_x, points_y = [], []
        for x, y in zip(core.get_x(), core.get_y()):
            if x is not None and y is not None:
                points_x.append(x)
                points_y.append(y)

        if points_x:
            self.axes.scatter(points_x, points_y, color='blue', s=40, zorder=5)

        # Рисуем вычисленные точки
        self._draw_computed_points()

        # Обновляем холст
        self.canvas.draw()

        # Возвращаем фокус на график
        self.canvas.get_tk_widget().focus_set()