from tkinter import ttk
from views.plot.canvas import PlotCanvas


class RightPanel(ttk.Frame):
    def __init__(self, parent, control_container, **kwargs):
        super().__init__(parent, **kwargs)

        # Получаем кнопку режима рисования
        draw_mode_button = control_container.get_draw_mode_button()

        # Создаём график
        self.plot_canvas = PlotCanvas(self, draw_mode_button)
        self.plot_canvas.pack(fill="both", expand=True)

        # Передаём ссылки на виджеты для СКМ
        self.plot_canvas.set_x_input(control_container.get_x_input())
        self.plot_canvas.set_compute_button(control_container.get_compute_button())

        # Передаём methods_panel в compute_button
        compute_btn = control_container.get_compute_button()
        compute_btn.set_methods_panel(control_container.get_methods_panel())