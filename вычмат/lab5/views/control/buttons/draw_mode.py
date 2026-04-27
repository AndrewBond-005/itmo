from tkinter import ttk


class DrawModeButton(ttk.Button):
    def __init__(self, parent, **kwargs):
        self.mode_on = False
        super().__init__(parent, text="✎ Режим рисования", command=self._toggle, **kwargs)
        self._update_style()

    def _toggle(self):
        self.mode_on = not self.mode_on
        self._update_style()

    def _update_style(self):
        if self.mode_on:
            self.configure(text="✓ Режим рисования (вкл)")
        else:
            self.configure(text="✎ Режим рисования (выкл)")

    def is_active(self):
        return self.mode_on