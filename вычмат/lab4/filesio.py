# Константы импорта/экспорта
IMPORT_FILE_TYPES = [("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
EXPORT_FILE_TYPES = [("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
DEFAULT_ENCODING = "utf-8"

import tkinter as tk
from tkinter import filedialog, messagebox
from utils import parse_number


class FileIO:
    """Класс для импорта/экспорта данных."""

    @staticmethod
    def import_data(table, max_points, warning_callback):
        """Импортирует данные из файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл для импорта",
            filetypes=IMPORT_FILE_TYPES
        )

        if not filename:
            return

        try:
            with open(filename, 'r', encoding=DEFAULT_ENCODING) as f:
                lines = f.readlines()

            points = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if len(parts) >= 2:
                    x = parse_number(parts[0])
                    y = parse_number(parts[1])
                    if x is not None and y is not None:
                        points.append((x, y))

            if len(points) > max_points:
                warning_callback(f"Слишком много точек (максимум {max_points})")
                points = points[:max_points]

            # Очищаем таблицу
            table.clear_phi_epsilon()
            for entry in table.entries:
                entry['x_entry'].delete(0, tk.END)
                entry['y_entry'].delete(0, tk.END)

            # Заполняем данными
            for i, (x, y) in enumerate(points):
                if i < len(table.entries):
                    table.entries[i]['x_entry'].insert(0, str(x))
                    table.entries[i]['y_entry'].insert(0, str(y))

            table._on_data_changed()

        except Exception as e:
            warning_callback(f"Ошибка импорта: {str(e)}")

    @staticmethod
    def export_data(table, results_text, results_table):
        """Экспортирует данные в файл."""
        filename = filedialog.asksaveasfilename(
            title="Сохранить как",
            filetypes=EXPORT_FILE_TYPES,
            defaultextension=".txt"
        )

        if not filename:
            return

        try:
            with open(filename, 'w', encoding=DEFAULT_ENCODING) as f:
                # Таблица
                f.write("Таблица:\n")
                f.write("№\tx\ty\tφ(x)\tε\n")

                for i, entry in enumerate(table.entries, 1):
                    x_val = entry['x_entry'].get().strip()
                    y_val = entry['y_entry'].get().strip()
                    phi_val = entry['phi_label'].cget("text")
                    eps_val = entry['eps_label'].cget("text")

                    if x_val or y_val:
                        f.write(f"{i}\t{x_val}\t{y_val}\t{phi_val}\t{eps_val}\n")

                f.write("\n")

                # Лучшая аппроксимация
                results = results_text.get(1.0, tk.END).strip()
                if results:
                    f.write(results)
                    f.write("\n\n")

                # Все аппроксимации
                f.write("Все аппроксимации:\n")
                headers = ["Тип", "a", "b", "c", "d", "S", "δ", "R²", "r"]
                f.write("\t".join(headers) + "\n")

                for row_labels in results_table.labels:
                    values = [label.cget("text") for label in row_labels]
                    if any(values):  # Только непустые строки
                        f.write("\t".join(values) + "\n")

            messagebox.showinfo("Экспорт", "Данные успешно сохранены!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка экспорта: {str(e)}")