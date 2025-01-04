import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
from utils.file_handler import FileHandler
from utils.menu import MenuCreator
from utils.search import FileSearch
from utils.statistics_view import StatisticsView
from utils.content_search import ContentSearcher
import os
import sys
from datetime import datetime

# adding the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

class FileAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Analyzer")
        self.root.geometry("800x600")
        self.directory = ""
        self.output_file = os.path.join(project_root, "output_analysis.csv")  # Specifying the full path here to save csv properly!
        
        # Прогресс-бар и статус-бар
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        self.status_label = tk.Label(root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
         # Создание экземпляра StatisticsView
        self.statistics_view = StatisticsView(self.root, self.output_file)
       
        # Создание меню
        MenuCreator(self)

    def open_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            self.output_file = filepath
            messagebox.showinfo("Файл открыт", f"Выбран файл индексации: {os.path.basename(filepath)}")
            self.status_label.config(text=f"Активный файл индексации: {os.path.basename(filepath)}")

    def select_folder(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.status_label.config(text=f"Выбрана папка: {self.directory}")

    def run_indexing(self):
        if not self.directory:
            messagebox.showwarning("Внимание", "Выберите папку для анализа.")
            return

        handler = FileHandler(self.directory, self.output_file, self.progress, self.status_label)
        handler.index_files()

    def show_last_index_info(self):
        handler = FileHandler(self.directory, self.output_file, self.progress, self.status_label)
        handler.show_last_index_info()

    def search_files(self):
        FileSearch(self.root, self.output_file)

    def show_extensions(self):
        StatisticsView(self.root, self.output_file).show_extensions()

    def show_top_files(self):
        StatisticsView(self.root, self.output_file).show_top_files()

    def search_content(self):
        if not self.directory:
            messagebox.showwarning("Внимание", "Выберите папку для анализа.")
            return

        search_string = simpledialog.askstring("Поиск", "Введите строку для поиска:")
        if search_string:
            searcher = ContentSearcher(self.directory)
            results = searcher.search(search_string)
            if results:
                messagebox.showinfo("Результаты поиска", "\n".join(results))
            else:
                messagebox.showinfo("Результаты поиска", "Ничего не найдено.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileAnalyzerApp(root)
    root.mainloop()
