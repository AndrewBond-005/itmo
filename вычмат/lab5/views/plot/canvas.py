import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data.core as core
from utils.const import CLICK_EPSILON, SCROLL_STEP


class PlotCanvas:
    def __init__(self, parent, draw_mode_button, x_range=(-5, 15), y_range=(-5, 15)):
        self.parent = parent
        self.draw_mode_button = draw_mode_button
        self.x_range = x_range
        self.y_range = y_range

        print("[PlotCanvas] Инициализация...")

        # Создание фигуры и осей
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Создание холста
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Настройка осей
        self._setup_axes()

        # Подключение событий мыши
        self._connect_events()

        # Подписка на изменения в core
        core.subscribe(self.refresh)

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
        print(f"[PlotCanvas] События подключены: click_id={self.cid_click}, scroll_id={self.cid_scroll}")

    def _on_click(self, event):
        """Обработчик нажатий кнопок мыши"""
        print(f"[PlotCanvas] _on_click вызван: button={event.button}, x={event.xdata}, y={event.ydata}")

        # Проверяем, включён ли режим рисования
        if not self.draw_mode_button.is_active():
            print("[PlotCanvas] Режим рисования ВЫКЛЮЧЁН - игнорируем клик")
            return

        # Проверяем, что клик внутри области графика
        if event.inaxes != self.ax:
            print(f"[PlotCanvas] Клик вне области графика: inaxes={event.inaxes}")
            return

        x_click = event.xdata
        y_click = event.ydata
        print(f"[PlotCanvas] Клик внутри графика: x={x_click:.3f}, y={y_click:.3f}")

        if event.button == 1:  # ЛКМ - добавление точки
            print("[PlotCanvas] ЛКМ: добавление точки")
            self._add_point(x_click, y_click)
        elif event.button == 3:  # ПКМ - удаление ближайшего узла
            print("[PlotCanvas] ПКМ: удаление ближайшего узла")
            self._delete_nearest(x_click, y_click)
        elif event.button == 2:  # СКМ - выбор абсциссы
            print("[PlotCanvas] СКМ: выбор абсциссы")
            self._select_x(x_click)
        else:
            print(f"[PlotCanvas] Неизвестная кнопка: {event.button}")

    def _on_scroll(self, event):
        """Обработчик колёсика мыши"""
        print(
            f"[PlotCanvas] _on_scroll вызван: button={event.button}, x={event.xdata}, y={event.ydata}, step={event.step}")

        # Проверяем, включён ли режим рисования
        if not self.draw_mode_button.is_active():
            print("[PlotCanvas] Режим рисования ВЫКЛЮЧЁН - игнорируем скролл")
            return

        # Проверяем, что курсор внутри области графика
        if event.inaxes != self.ax:
            print(f"[PlotCanvas] Скролл вне области графика: inaxes={event.inaxes}")
            return

        x_cursor = event.xdata
        y_cursor = event.ydata
        print(f"[PlotCanvas] Скролл внутри графика: x={x_cursor:.3f}, y={y_cursor:.3f}")

        # Находим ближайший узел
        idx, dist = self._find_nearest(x_cursor, y_cursor)

        if idx != -1 and dist < CLICK_EPSILON:
            x_list = core.get_x()
            y_list = core.get_y()
            current_y = y_list[idx]
            print(f"[PlotCanvas] Найден узел #{idx}: x={x_list[idx]:.3f}, y={current_y:.3f}, dist={dist:.4f}")

            if current_y is not None:
                if event.button == 'up':  # Колёсико вверх
                    new_y = current_y + SCROLL_STEP
                    print(f"[PlotCanvas] Колёсико вверх: y={current_y:.3f} -> {new_y:.3f}")
                elif event.button == 'down':  # Колёсико вниз
                    new_y = current_y - SCROLL_STEP
                    print(f"[PlotCanvas] Колёсико вниз: y={current_y:.3f} -> {new_y:.3f}")
                else:
                    print(f"[PlotCanvas] Неизвестное направление скролла: {event.button}")
                    return

                # Обновляем значение Y
                core.update_y(idx, new_y)
        else:
            if idx == -1:
                print("[PlotCanvas] Узлов поблизости не найдено")
            else:
                print(f"[PlotCanvas] Узел слишком далеко: dist={dist:.4f} > epsilon={CLICK_EPSILON}")

    def _add_point(self, x, y):
        """Добавляет новую точку, находя подходящее место"""
        print(f"[PlotCanvas] Добавление точки: ({x:.3f}, {y:.3f})")

        x_list = core.get_x()
        y_list = core.get_y()

        # Ищем подходящее место для вставки
        found_index = -1

        for i in range(len(x_list)):
            x_val = x_list[i]
            y_val = y_list[i]

            # Проверяем, можно ли использовать эту строку
            if x_val is None and y_val is None:
                # Пустая строка - идеально
                found_index = i
                print(f"[PlotCanvas] Найдена пустая строка #{i}, используем её")
                break
            elif x_val is None and y_val is not None:
                # Есть только y, можно заменить
                found_index = i
                print(f"[PlotCanvas] Найдена строка #{i} с частичными данными (y={y_val:.3f}), используем её")
                break
            elif x_val is not None and y_val is None:
                # Есть только x, можно заменить
                found_index = i
                print(f"[PlotCanvas] Найдена строка #{i} с частичными данными (x={x_val:.3f}), используем её")
                break

        if found_index != -1:
            # Обновляем существующую строку
            print(f"[PlotCanvas] Обновление строки #{found_index}: ({x:.3f}, {y:.3f})")
            core.update_x(found_index, x)
            core.update_y(found_index, y)
        else:
            # Все строки полные, добавляем новую
            print("[PlotCanvas] Свободных строк нет, добавляем новую")
            core.add_point(x, y)

        print(f"[PlotCanvas] Точка добавлена, всего строк: {len(core.get_x())}")

    def _delete_nearest(self, x_click, y_click):
        """Удаляет ближайший узел, если он достаточно близко"""
        idx, dist = self._find_nearest(x_click, y_click)
        print(f"[PlotCanvas] Ближайший узел: idx={idx}, dist={dist:.4f}")

        if idx != -1 and dist < CLICK_EPSILON:
            x_list = core.get_x()
            y_list = core.get_y()
            print(f"[PlotCanvas] Удаление узла #{idx}: ({x_list[idx]:.3f}, {y_list[idx]:.3f})")
            core.delete_point(idx)
            print(f"[PlotCanvas] Узел удалён, осталось строк: {len(core.get_x())}")
        else:
            if idx == -1:
                print("[PlotCanvas] Узлов поблизости не найдено")
            else:
                print(f"[PlotCanvas] Узел слишком далеко для удаления: dist={dist:.4f} > epsilon={CLICK_EPSILON}")

    def _select_x(self, x_click):
        """Выбирает абсциссу для будущего вычисления"""
        print(f"[PlotCanvas] Выбрана абсцисса: {x_click:.3f}")
        # Здесь позже будет заполнение поля ввода

    def _find_nearest(self, x_click, y_click):
        """Находит индекс ближайшего узла и евклидово расстояние"""
        x_list = core.get_x()
        y_list = core.get_y()

        min_dist_sq = float('inf')
        min_idx = -1

        for i in range(len(x_list)):
            if x_list[i] is None or y_list[i] is None:
                print(f"[PlotCanvas] Точка #{i}: пропущена (None)")
                continue

            dx = x_list[i] - x_click
            dy = y_list[i] - y_click
            dist_sq = dx * dx + dy * dy
            dist = dist_sq ** 0.5

            print(f"[PlotCanvas] Точка #{i}: ({x_list[i]:.3f}, {y_list[i]:.3f}), расстояние={dist:.4f}")

            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                min_idx = i

        if min_idx != -1:
            min_dist = min_dist_sq ** 0.5
            print(f"[PlotCanvas] Ближайшая точка: #{min_idx}, расстояние={min_dist:.4f}")
            return min_idx, min_dist
        print("[PlotCanvas] Ближайших точек не найдено")
        return -1, float('inf')

    def refresh(self):
        """Обновляет график на основе данных из core"""
        print("[PlotCanvas] refresh() вызван")
        # Очищаем оси
        self.ax.clear()

        # Заново устанавливаем фиксированные границы и подписи
        self._setup_axes()

        # Получаем данные из core
        x_list = core.get_x()
        y_list = core.get_y()
        print(f"[PlotCanvas] Данные из core: X={x_list}, Y={y_list}")

        # Собираем только те точки, где оба значения не None
        points_x = []
        points_y = []

        for i, (x, y) in enumerate(zip(x_list, y_list)):
            if x is not None and y is not None:
                points_x.append(x)
                points_y.append(y)
                print(f"[PlotCanvas] Точка #{i}: ({x:.3f}, {y:.3f}) - будет отображена")
            else:
                print(f"[PlotCanvas] Точка #{i}: ({x}, {y}) - НЕ отображена (None значение)")

        # Рисуем точки (синие кружочки, без линии)
        if points_x:
            print(f"[PlotCanvas] Рисуем {len(points_x)} точек")
            self.ax.scatter(points_x, points_y, color='blue', marker='o', s=50, zorder=5)
        else:
            print("[PlotCanvas] Нет точек для отображения")

        # Перерисовываем холст
        self.canvas.draw()
        print("[PlotCanvas] refresh() завершён")