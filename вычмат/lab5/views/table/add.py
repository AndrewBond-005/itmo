from tkinter import ttk

class AddRowButton(ttk.Button):
    def __init__(self, parent, core_module, table_widget, **kwargs):
        super().__init__(parent, text="+ Добавить строку", command=self._add_row, **kwargs)
        self.core = core_module
        self.table_widget = table_widget

    def _add_row(self):
        # Принудительно добавляем строку в core
        current_x = self.core.get_x()
        current_y = self.core.get_y()
        self.core.add_point(None, None)
        # Прокручиваем вниз
        if self.table_widget:
            self.table_widget.after(100, self.table_widget.scroll_to_bottom)