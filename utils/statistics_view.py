import tkinter as tk
import pandas as pd
import os
import sys
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatisticsView:
    def __init__(self, root, output_file):
        self.root = root
        self.output_file = output_file

    def show_extensions(self):
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
                text.insert("end", f"{row['file_name']} - {row['file_size']} bytes\n")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Ошибка", "Файл не содержит данных для анализа.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке данных: {e}")


    def show_top_files_chart(self):
        if not os.path.exists(self.output_file) or os.path.getsize(self.output_file) == 0:
            messagebox.showwarning("Внимание", "Файл данных пуст или не существует.")
            return
        try:
            # Чтение и обработка CSV
            df = pd.read_csv(self.output_file).sort_values(by="file_size", ascending=False).head(10)

            # Построение графика
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(df['file_name'], df['file_size'], color='skyblue')
            ax.set_xlabel('Размер файла (bytes)')
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
        top = tk.Toplevel(self.root)
        top.title("График топ-10 файлов по размеру")

        img = tk.PhotoImage(file=chart_file)
        label = tk.Label(top, image=img)
        label.image = img  # Keep a reference
        label.pack()
