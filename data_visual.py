import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datatest
from datetime import datetime
import os
import numpy as np

CATEGORICAL_COLS = ['anaemia', 'diabetes', 'high bp']
ALL_COLS = datatest.df.columns.tolist()

# Список цветовых схем
COLORMAPS = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges',
    'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd',
    'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu',
    'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg',
    'spring', 'summer', 'autumn', 'winter'
]

# Маркер
MARKER = 'o'

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация данных - Расширенная")
        self.root.geometry("900x750")

        # Переменные для выбранных колонок и цветовой схемы
        self.x_col = tk.StringVar(value=ALL_COLS[0] if ALL_COLS else "")
        self.y_col = tk.StringVar(value=ALL_COLS[1] if len(ALL_COLS) > 1 else ALL_COLS[0])
        self.cmap_name = tk.StringVar(value='GnBu')  # для фамилии на 'С'

        # Списки кнопок
        self.x_buttons = []
        self.y_buttons = []

        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        #  Верхняя панель: выбор цветовой схемы
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(top_frame, text="Цветовая схема (colormap):").pack(side=tk.LEFT, padx=5)
        cmap_menu = ttk.Combobox(top_frame, textvariable=self.cmap_name,
                                 values=COLORMAPS, state='readonly', width=15)
        cmap_menu.pack(side=tk.LEFT, padx=5)
        cmap_menu.bind('<<ComboboxSelected>>', lambda e: self.update_plot())

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        #  Левая панель (кнопки Y)
        left_frame = ttk.Frame(main_frame, width=120)
        left_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        left_frame.grid_propagate(False)

        ttk.Label(left_frame, text="Ось Y", font=('Arial', 10, 'bold')).pack(pady=5)

        for col in ALL_COLS:
            btn = tk.Button(left_frame, text=col, width=15,
                            command=lambda c=col: self.select_y(c))
            btn.pack(pady=2)
            self.y_buttons.append(btn)

        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Нижняя панель
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

        ttk.Label(bottom_frame, text="Ось X", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

        for col in ALL_COLS:
            btn = tk.Button(bottom_frame, text=col, width=12,
                            command=lambda c=col: self.select_x(c))
            btn.pack(side=tk.LEFT, padx=2)
            self.x_buttons.append(btn)

        # Кнопка сохранения
        save_btn = tk.Button(bottom_frame, text="Сохранить график", command=self.save_plot,
                             bg='lightgreen', width=15)
        save_btn.pack(side=tk.RIGHT, padx=10)

        # Выделяем начальные кнопки
        self.highlight_buttons()

    def select_x(self, col):
        self.x_col.set(col)
        self.highlight_buttons()
        self.update_plot()

    def select_y(self, col):
        self.y_col.set(col)
        self.highlight_buttons()
        self.update_plot()

    def highlight_buttons(self):
        for btn in self.x_buttons:
            if btn['text'] == self.x_col.get():
                btn.config(bg='lightblue', relief=tk.SUNKEN)
            else:
                btn.config(bg='SystemButtonFace', relief=tk.RAISED)

        for btn in self.y_buttons:
            if btn['text'] == self.y_col.get():
                btn.config(bg='lightblue', relief=tk.SUNKEN)
            else:
                btn.config(bg='SystemButtonFace', relief=tk.RAISED)

    def determine_plot_type(self, x_col, y_col):
        x_is_cat = x_col in CATEGORICAL_COLS
        y_is_cat = y_col in CATEGORICAL_COLS

        if x_col == y_col:
            if x_is_cat:
                return 'pie'
            else:
                return 'histogram'
        else:
            if x_is_cat and not y_is_cat:
                return 'bar'
            elif not x_is_cat and y_is_cat:
                return 'boxplot'
            else:
                return 'scatter'

    def update_plot(self):
        x_col = self.x_col.get()
        y_col = self.y_col.get()
        cmap = self.cmap_name.get()

        self.ax.clear()

        df = datatest.df
        x_data = df[x_col]
        y_data = df[y_col]

        plot_type = self.determine_plot_type(x_col, y_col)

        if plot_type == 'scatter':
            self.ax.scatter(x_data, y_data, marker=MARKER,
                            c=x_data, cmap=cmap, alpha=0.7, edgecolors='k')
            self.ax.set_xlabel(x_col)
            self.ax.set_ylabel(y_col)
            self.ax.set_title(f'Scatter: {y_col} vs {x_col}')

        elif plot_type == 'histogram':
            self.ax.hist(x_data, bins=10, color=plt.get_cmap(cmap)(0.5), edgecolor='black')
            self.ax.set_xlabel(x_col)
            self.ax.set_ylabel('Частота')
            self.ax.set_title(f'Гистограмма для {x_col}')

        elif plot_type == 'pie':
            counts = x_data.value_counts()
            colors = [plt.get_cmap(cmap)(i / len(counts)) for i in range(len(counts))]
            self.ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=colors,
                        startangle=90, wedgeprops={'edgecolor': 'black'})
            self.ax.set_title(f'Круговая диаграмма для {x_col}')
            self.ax.axis('equal')

        elif plot_type == 'bar':
            counts = x_data.value_counts().sort_index()
            colors = [plt.get_cmap(cmap)(i / len(counts)) for i in range(len(counts))]
            self.ax.bar(counts.index, counts.values, color=colors, edgecolor='black')
            self.ax.set_xlabel(x_col)
            self.ax.set_ylabel('Количество записей')
            self.ax.set_title(f'Столбчатая диаграмма: {x_col}')

        elif plot_type == 'boxplot':
            cats = sorted(df[y_col].unique())
            data_by_cat = [df[df[y_col] == cat][x_col].dropna() for cat in cats]
            self.ax.boxplot(data_by_cat, tick_labels=cats, patch_artist=True,
                            boxprops=dict(facecolor=plt.get_cmap(cmap)(0.5)))
            self.ax.set_xlabel(y_col)
            self.ax.set_ylabel(x_col)
            self.ax.set_title(f'Коробочная диаграмма: {x_col} по {y_col}')

        self.canvas.draw()

    def save_plot(self):
        now = datetime.now()
        filename = f"graph{now.hour:02d}_{now.minute:02d}_{now.second:02d}.png"
        filepath = os.path.join(os.getcwd(), filename)
        self.figure.savefig(filepath, dpi=100, bbox_inches='tight')
        messagebox.showinfo("Сохранение", f"График сохранён как:\n{filepath}")

if __name__ == '__main__':
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()