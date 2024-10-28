import tkinter as tk
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import os
import sys


class FileSearch:
    def __init__(self, root, output_file):
        self.root = root  # Сохраняем root как атрибут экземпляра
        self.output_file = output_file
        self.create_search_window(root)

    def create_search_window(self, root):
        search_window = tk.Toplevel(root)
        search_window.title("Поиск файлов")
        
        # Поля для ввода
        # Метки и поля ввода для фильтров
        tk.Label(search_window, text="Название файла:").grid(row=0, column=0)
        tk.Label(search_window, text="Минимальный размер (в байтах):").grid(row=1, column=0)
        tk.Label(search_window, text="Максимальный размер (в байтах):").grid(row=2, column=0)
        tk.Label(search_window, text="Дата создания (формат YYYY-MM-DD):").grid(row=3, column=0)
        tk.Label(search_window, text="Дата модификации (формат YYYY-MM-DD):").grid(row=4, column=0)
        
        # Поля ввода
        file_name = tk.Entry(search_window)
        min_size = tk.Entry(search_window)
        max_size = tk.Entry(search_window)
        creation_date = tk.Entry(search_window)
        modification_date = tk.Entry(search_window)
        
        # Размещение полей ввода
        file_name.grid(row=0, column=1)
        min_size.grid(row=1, column=1)
        max_size.grid(row=2, column=1)
        creation_date.grid(row=3, column=1)
        modification_date.grid(row=4, column=1)

        # Кнопка запуска поиска
        tk.Button(
            search_window, 
            text="Поиск", 
            command=lambda: self.execute_search(
                file_name.get(), 
                min_size.get(), 
                max_size.get(), 
                creation_date.get(), 
                modification_date.get()
            )
        ).grid(row=5, column=1)

    def execute_search(self, name, min_size, max_size, creation_date, modification_date):
        if not os.path.exists(self.output_file):
            messagebox.showwarning("Внимание", "Нет данных для поиска. Сначала выполните индексацию.")
            return
        
        df = pd.read_csv(self.output_file)

        # Фильтрация по названию
        if name:
            df = df[df['file_name'].fillna('').str.contains(name, case=False)]
        
        # Фильтрация по размеру файла
        if min_size:
            df = df[df['file_size'] >= int(min_size)]
        if max_size:
            df = df[df['file_size'] <= int(max_size)]
        
        # Фильтрация по дате создания
        if creation_date:
            try:
                creation_date_dt = datetime.strptime(creation_date, '%Y-%m-%d')
                df = df[df['creation_time'] >= creation_date_dt.strftime('%Y-%m-%d')]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для создания. Используйте YYYY-MM-DD.")
        
        # Фильтрация по дате модификации
        if modification_date:
            try:
                modification_date_dt = datetime.strptime(modification_date, '%Y-%m-%d')
                df = df[df['modification_time'] >= modification_date_dt.strftime('%Y-%m-%d')]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для модификации. Используйте YYYY-MM-DD.")
        
        # Отображение результатов
        top = tk.Toplevel(self.root)
        top.title("Результаты каталожного поиска")
        text = tk.Text(top)
        text.pack(fill="both", expand=True)

        # Выводим данные для каждого найденного файла
        if not df.empty:
            for _, row in df.iterrows():
                text.insert("end", f"{row['file_name']} - {row['file_size']} bytes - {row['creation_time']} - {row['modification_time']}\n")
        else:
            text.insert("end", "Нет результатов, соответствующих критериям поиска.\n")

