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