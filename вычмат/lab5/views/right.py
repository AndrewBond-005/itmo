from tkinter import ttk

class RightPanel(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        frame = ttk.Frame(self, relief="groove", borderwidth=2)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Label(frame, text="Здесь будет график", font=("Arial", 16)).pack(expand=True)