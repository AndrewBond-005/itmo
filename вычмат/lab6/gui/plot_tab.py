"""
Вкладка с графиками
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from config import COLORS, PLOT_COLORS


class PlotTab(tk.Frame):
    """Вкладка с графиками"""

    def __init__(self, parent, colors, var_show_exact):
        super().__init__(parent, bg=colors["bg"])
        self.colors = colors
        self.var_show_exact = var_show_exact
        self._build()

    def _build(self):
        self.fig = Figure(figsize=(9, 6), facecolor=self.colors["plot_bg"])
        self.ax = self.fig.add_subplot(111)
        self._style_ax(self.ax)

        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_plot.get_tk_widget().pack(fill="both", expand=True)

        toolbar_frame = tk.Frame(self, bg=self.colors["bg"])
        toolbar_frame.pack(fill="x")
        toolbar = NavigationToolbar2Tk(self.canvas_plot, toolbar_frame)
        toolbar.config(bg=self.colors["bg"])
        toolbar.update()

    def _style_ax(self, ax):
        ax.set_facecolor(self.colors["plot_bg"])
        ax.tick_params(colors=self.colors["text_dim"], labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(self.colors["plot_axes"])
        ax.xaxis.label.set_color(self.colors["text"])
        ax.yaxis.label.set_color(self.colors["text"])
        ax.title.set_color(self.colors["text"])
        ax.grid(True, color=self.colors["plot_grid"], linestyle="--", linewidth=0.7, alpha=0.7)

    def clear(self):
        self.ax.clear()
        self._style_ax(self.ax)
        self.canvas_plot.draw()

    def draw(self, results, xs_exact, ys_exact, ode_label):
        self.ax.clear()
        self._style_ax(self.ax)

        if self.var_show_exact.get():
            self.ax.plot(xs_exact, ys_exact,
                         color=self.colors["exact"], linewidth=2.5,
                         label="Точное решение", zorder=5)

        styles = {"Эйлер": ("-", 1.6), "Рунге-Кутта 4": ("-", 1.6), "Адамс": ("-", 2.0)}

        for name, (xs, ys) in results.items():
            lstyle, lw = styles.get(name, ("-", 1.5))
            self.ax.plot(
                xs, ys,
                color=PLOT_COLORS.get(name, "#ffffff"),
                linestyle=lstyle, linewidth=lw,
                marker='',
                label=name, alpha=0.9, zorder=4
            )

        self.ax.set_title(f"Решение ОДУ: {ode_label}",
                          color=self.colors["text"], fontsize=11, pad=12)
        self.ax.set_xlabel("x", fontsize=10)
        self.ax.set_ylabel("y", fontsize=10)

        if self.ax.get_legend_handles_labels()[0]:
            self.ax.legend(
                facecolor=self.colors["card"],
                edgecolor=self.colors["border"],
                labelcolor=self.colors["text"],
                fontsize=9, loc="best"
            )

        self.fig.tight_layout()
        self.canvas_plot.draw()