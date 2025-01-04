import tkinter as tk
import pandas as pd
import os
import sys
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.gui_humanizer import humanize_file_size

class StatisticsView:
    """
    Класс для отображения статистики на основе данных из CSV файла.

    Предоставляет функциональность для отображения статистики по расширениям файлов,
    списка топ-10 файлов по размеру и графиков на основе этих данных.
    """
    def __init__(self, root, output_file):
        """
        Инициализирует объект StatisticsView.

        Параметры:
        ----------
        root : tkinter.Tk или tkinter.Toplevel
            Основное окно Tkinter.
        output_file : str
            Путь к CSV файлу с результатами индексации.
        """
        self.root = root
        self.output_file = output_file


    def show_extensions(self):
        """
        Отображает статистику по расширениям файлов.

        Считывает данные из CSV файла и показывает количество файлов каждого расширения
        в отдельном окне Tkinter.
        """
        if not os.path.exists(self.output_file) or os.path.getsize(self.output_file) == 0:
            messagebox.showwarning("Внимание", "Файл данных пуст или не существует.")
            return
        try:
            # Чтение CSV файла
            df = pd.read_csv(self.output_file)
            extension_counts = df['extension'].value_counts()

            top = tk.Toplevel(self.root)
            text = tk.Text(top)
            text.pack(fill="both", expand=True)
            text.insert("1.0", "Разбивка по расширениям:\n")
            for ext, count in extension_counts.items():
                text.insert("end", f"{ext}: {count}\n")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Ошибка", "Файл не содержит данных для анализа.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке данных: {e}")

    def show_top_files(self):
        """
        Отображает список топ-10 файлов по размеру.

        Считывает данные из CSV файла, сортирует их по размеру и показывает
        список из 10 самых крупных файлов в отдельном окне Tkinter.
        """
        if not os.path.exists(self.output_file) or os.path.getsize(self.output_file) == 0:
            messagebox.showwarning("Внимание", "Файл данных пуст или не существует.")
            return
        try:
        # Read and process CSV
            df = pd.read_csv(self.output_file).sort_values(by="file_size", ascending=False).head(10)

            top = tk.Toplevel(self.root)
            text = tk.Text(top)
            text.pack(fill="both", expand=True)
            text.insert("1.0", "Топ 10 файлов по размеру:\n")
            for _, row in df.iterrows():
                readable_size = humanize_file_size(row['file_size'])
                text.insert("end", f"{row['file_name']} - {readable_size}\n")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Ошибка", "Файл не содержит данных для анализа.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке данных: {e}")


    def show_top_files_chart(self):
        """
        Строит и отображает график топ-10 файлов по размеру.

        Считывает данные из CSV файла, сортирует их по размеру, строит
        горизонтальный столбчатый график и отображает его в новом окне Tkinter.
        """
        if not os.path.exists(self.output_file) or os.path.getsize(self.output_file) == 0:
            messagebox.showwarning("Внимание", "Файл данных пуст или не существует.")
            return
        try:
            # Чтение и обработка CSV
            df = pd.read_csv(self.output_file).sort_values(by="file_size", ascending=False).head(10)
            # Преобразование размера файла в мегабайты
            df['file_size_mb'] = df['file_size'] / (1024 * 1024)


            # Построение графика
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(df['file_name'], df['file_size_mb'], color='skyblue')
            ax.set_xlabel('Размер файла (мб.)')
            ax.set_title('Топ 10 файлов по размеру')
            
            # Сохранение графика в файл
            chart_file = os.path.join(os.path.dirname(self.output_file), 'top_files_chart.png')
            plt.savefig(chart_file, bbox_inches='tight')
            plt.close(fig)

            # Отображение графика в Tkinter
            self.display_chart(chart_file)

        except pd.errors.EmptyDataError:
            messagebox.showerror("Ошибка", "Файл не содержит данных для анализа.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке данных: {e}")

    def display_chart(self, chart_file):
        """
        Отображает сохранённый график в новом окне Tkinter.

        Параметры:
        ----------
        chart_file : str
            Путь к файлу изображения с графиком.
        """
        top = tk.Toplevel(self.root)
        top.title("График топ-10 файлов по размеру")

        img = tk.PhotoImage(file=chart_file)
        label = tk.Label(top, image=img)
        label.image = img  # Keep a reference
        label.pack()

