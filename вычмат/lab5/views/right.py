from tkinter import ttk
from views.plot.canvas import PlotCanvas


class RightPanel(ttk.Frame):
    def __init__(self, parent, control_container, **kwargs):  # ИЗМЕНИТЬ параметр
        super().__init__(parent, **kwargs)
        # Получаем кнопку режима рисования из контейнера управления
        draw_mode_button = control_container.get_draw_mode_button()
        # Создаём график с передачей кнопки режима рисования
        self.plot_canvas = PlotCanvas(self, draw_mode_button)