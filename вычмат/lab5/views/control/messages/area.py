import tkinter as tk
from tkinter import ttk


class MessageArea(ttk.Frame):
    def __init__(self, parent, height=3, **kwargs):
        super().__init__(parent, **kwargs)
        self.height = height

        # Текстовое поле с возможностью скролла
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(frame, wrap=tk.WORD, height=height, font=("Courier", 8))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=scrollbar.set)

        # Настройка тегов для цветов
        self.text.tag_config("error", foreground="red")
        self.text.tag_config("warning", foreground="orange")
        self.text.tag_config("info", foreground="green")

        self.clear()

    def set_height(self, height):
        """Изменяет высоту текстового поля"""
        self.height = height
        self.text.configure(height=height)

    def add_message(self, message, msg_type="info"):
        """Добавляет сообщение с цветом"""
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, message + "\n", msg_type)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def clear(self):
        """Очищает все сообщения"""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, "Готов\n", "info")
        self.text.config(state=tk.DISABLED)

    def hide(self):
        """Скрывает область сообщений"""
        self.pack_forget()

    def show(self):
        """Показывает область сообщений"""
        self.pack(fill=tk.X, pady=(0, 2))