import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import data.core as core
from utils.const import CLICK_EPSILON, SCROLL_STEP, COLOR_LAGRANGE, COLOR_NEWTON_DIV, COLOR_NEWTON_FIN, LINE_WIDTH, \
    LINE_STYLE
from views.plot.methods_state import methods_state
from views.plot import lines


class PlotCanvas:
    def __init__(self, parent, draw_mode_button, x_range=(-5, 15), y_range=(-5, 15)):
        self.parent = parent
        self.draw_mode_button = draw_mode_button
        self.x_range = x_range
        self.y_range = y_range

        print("[PlotCanvas] Инициализация...")

        # Создаём контейнер для графика и тулбара
        self.plot_container = tk.Frame(parent)
        self.plot_container.pack(fill=tk.BOTH, expand=True)

        # Создание фигуры и осей
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Создание холста
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_container)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Добавляем панель инструментов для навигации
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_container)
        self.toolbar.update()

        # Настройка осей
        self._setup_axes()

        # Подключение событий мыши для рисования
        self._connect_events()

        # Подписка на изменения в core
        core.subscribe(self.refresh)

        # Подписка на изменения состояния методов
        methods_state.subscribe(self.refresh)

        # Начальная отрисовка
        self.refresh()

        print("[PlotCanvas] Инициализация завершена")

    def _setup_axes(self):
        """Устанавливает фиксированные границы осей и подписи"""
        self.ax.set_xlim(self.x_range[0], self.x_range[1])
        self.ax.set_ylim(self.y_range[0], self.y_range[1])
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Узлы интерполяции")
        self.ax.grid(True, linestyle='--', alpha=0.7)

        # Добавляем чёрные оси (линии x=0 и y=0)
        self.ax.axhline(y=0, color='black', linewidth=1.5)
        self.ax.axvline(x=0, color='black', linewidth=1.5)

    def _connect_events(self):
        """Подключает обработчики событий мыши"""
        print("[PlotCanvas] Подключение событий мыши...")
        self.cid_click = self.figure.canvas.mpl_connect('button_press_event', self._on_click)
        self.cid_scroll = self.figure.canvas.mpl_connect('scroll_event', self._on_scroll)
        print(f"[PlotCanvas] События подключены")

    def _on_click(self, event):
        """Обработчик нажатий кнопок мыши"""
        # Если режим рисования выключен - не обрабатываем
        if not self.draw_mode_button.is_active():
            return

        # Проверяем, что клик внутри области графика
        if event.inaxes != self.ax:
            return

        x_click = event.xdata
        y_click = event.ydata

        if event.button == 1:  # ЛКМ - добавление точки
            self._add_point(x_click, y_click)
        elif event.button == 3:  # ПКМ - удаление ближайшего узла
            self._delete_nearest(x_click, y_click)
        elif event.button == 2:  # СКМ - выбор абсциссы
            self._select_x(x_click)

    def _on_scroll(self, event):
        """Обработчик колёсика мыши"""
        # Если режим рисования выключен - не обрабатываем
        if not self.draw_mode_button.is_active():
            return

        # Проверяем, что курсор внутри области графика
        if event.inaxes != self.ax:
            return

        x_cursor = event.xdata
        y_cursor = event.ydata

        # Находим ближайший узел
        idx, dist = self._find_nearest(x_cursor, y_cursor)

        if idx != -1 and dist < CLICK_EPSILON:
            x_list = core.get_x()
            y_list = core.get_y()
            current_y = y_list[idx]

            if current_y is not None:
                if event.step > 0:  # Колёсико вверх
                    new_y = current_y + SCROLL_STEP
                elif event.step < 0:  # Колёсико вниз
                    new_y = current_y - SCROLL_STEP
                else:
                    return

                # Обновляем значение Y
                core.update_y(idx, new_y)

    def _add_point(self, x, y):
        """Добавляет новую точку, находя подходящее место"""
        x_list = core.get_x()
        y_list = core.get_y()

        # Ищем подходящее место для вставки
        found_index = -1

        for i in range(len(x_list)):
            x_val = x_list[i]
            y_val = y_list[i]

            # Проверяем, можно ли использовать эту строку (не полную)
            if x_val is None and y_val is None:
                found_index = i
                break
            elif x_val is None and y_val is not None:
                found_index = i
                break
            elif x_val is not None and y_val is None:
                found_index = i
                break

        if found_index != -1:
            # Обновляем существующую строку
            core.update_x(found_index, x)
            core.update_y(found_index, y)
        else:
            # Все строки полные, добавляем новую
            core.add_point(x, y)

    def _delete_nearest(self, x_click, y_click):
        """Удаляет ближайший узел, если он достаточно близко"""
        idx, dist = self._find_nearest(x_click, y_click)

        if idx != -1 and dist < CLICK_EPSILON:
            core.delete_point(idx)

    def _select_x(self, x_click):
        """Выбирает абсциссу для будущего вычисления"""
        print(f"[PlotCanvas] Выбрана абсцисса: {x_click:.3f}")

    def _find_nearest(self, x_click, y_click):
        """Находит индекс ближайшего узла и евклидово расстояние"""
        x_list = core.get_x()
        y_list = core.get_y()

        min_dist_sq = float('inf')
        min_idx = -1

        for i in range(len(x_list)):
            if x_list[i] is None or y_list[i] is None:
                continue

            dx = x_list[i] - x_click
            dy = y_list[i] - y_click
            dist_sq = dx * dx + dy * dy

            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                min_idx = i

        if min_idx != -1:
            return min_idx, min_dist_sq ** 0.5
        return -1, float('inf')

    def _draw_interpolation_lines(self):
        """Рисует линии интерполяции для активных методов"""
        # Получаем отсортированные валидные узлы
        x_sorted, y_sorted = lines.get_sorted_valid_nodes(core)

        # Если узлов меньше 2, линии не рисуем
        if len(x_sorted) < 2:
            return

        # Создаём сетку для построения линий
        x_grid = lines.build_grid(x_sorted)

        if not x_grid:
            return

        # Лагранж (синий)
        if methods_state.is_lagrange_enabled():
            y_grid = lines.compute_lagrange_line(x_grid, x_sorted, y_sorted)
            if y_grid:
                self.ax.plot(x_grid, y_grid, color=COLOR_LAGRANGE,
                             linewidth=LINE_WIDTH, linestyle=LINE_STYLE,
                             label="Лагранж", zorder=2)

        # Ньютон (разделённые разности) - зелёный
        if methods_state.is_newton_div_enabled():
            y_grid = lines.compute_newton_div_line(x_grid, x_sorted, y_sorted)
            if y_grid:
                self.ax.plot(x_grid, y_grid, color=COLOR_NEWTON_DIV,
                             linewidth=LINE_WIDTH, linestyle=LINE_STYLE,
                             label="Ньютон (разд)", zorder=2)

        # Ньютон (конечные разности) - оранжевый
        if methods_state.is_newton_fin_enabled():
            y_grid = lines.compute_newton_fin_line(x_grid, x_sorted, y_sorted)
            if y_grid:
                self.ax.plot(x_grid, y_grid, color=COLOR_NEWTON_FIN,
                             linewidth=LINE_WIDTH, linestyle=LINE_STYLE,
                             label="Ньютон (кон)", zorder=2)

        # Добавляем легенду, если есть хотя бы одна линия
        if (methods_state.is_lagrange_enabled() or
                methods_state.is_newton_div_enabled() or
                methods_state.is_newton_fin_enabled()):
            self.ax.legend(loc='upper left')

    def refresh(self):
        """Обновляет график на основе данных из core"""
        # Очищаем оси
        self.ax.clear()

        # Заново устанавливаем фиксированные границы и подписи
        self._setup_axes()

        # Рисуем линии интерполяции
        self._draw_interpolation_lines()

        # Получаем данные из core
        x_list = core.get_x()
        y_list = core.get_y()

        # Собираем только те точки, где оба значения не None
        points_x = []
        points_y = []

        for i, (x, y) in enumerate(zip(x_list, y_list)):
            if x is not None and y is not None:
                points_x.append(x)
                points_y.append(y)

        # Рисуем точки
        if points_x:
            self.ax.scatter(points_x, points_y, color='blue', marker='o', s=40, zorder=5)

        # Перерисовываем холст
        self.canvas.draw()