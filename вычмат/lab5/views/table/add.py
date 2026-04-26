from tkinter import ttk

class AddRowButton(ttk.Button):
    def __init__(self, parent, core_module, table_widget, **kwargs):
        super().__init__(parent, text="+ Добавить строку", command=self._add_row, **kwargs)
        self.core = core_module
        self.table_widget = table_widget

    def _add_row(self):
        self.core.add_point(None, None)
        if self.table_widget:
            self.table_widget.after(100, self.table_widget.scroll_to_bottom)