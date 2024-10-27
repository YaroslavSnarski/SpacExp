import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from SpacExp.file_manager import FileManager
from utils.statistics import extension_stats, top_files, summary_stats
import os
import mimetypes
import time
from datetime import datetime

class FileAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Analyzer")
        self.root.geometry("800x600")

        self.directory = ""
        self.output_file = "output_analysis.csv"
        self.manager = None

        # Меню
        self.create_menu()

        # Прогресс-бар и статус-бар
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        self.status_label = tk.Label(root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть CSV файл", command=self.open_csv)
        file_menu.add_command(label="Выход", command=self.root.quit)

        actions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Действия программы", menu=actions_menu)
        
        stats_menu = tk.Menu(actions_menu, tearoff=0)
        actions_menu.add_cascade(label="Действия со статистикой", menu=stats_menu)
        stats_menu.add_command(label="Аналитика по расширениям", command=self.show_extensions)
        stats_menu.add_command(label="Топ-10 файлов по размеру", command=self.show_top_files)
        stats_menu.add_command(label="Каталожный поиск", command=self.search_files)  # Добавленная кнопка поиска

        program_menu = tk.Menu(actions_menu, tearoff=0)
        actions_menu.add_cascade(label="Управление программой", menu=program_menu)
        program_menu.add_command(label="Переиндексация", command=self.run_indexing)
        program_menu.add_command(label="Выбор папки", command=self.select_folder)
        program_menu.add_command(label="Сведения о последней индексации", command=self.show_last_index_info)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="О программе", menu=about_menu)
        about_menu.add_command(label="Справка", command=self.show_help)

    def open_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                # Загружаем CSV файл
                df = pd.read_csv(filepath)
                
                # Проверяем, что в CSV есть все необходимые колонки
                required_columns = {"file_path", "file_name", "file_size", "creation_time", "modification_time", "extension"}
                if required_columns.issubset(df.columns):
                    # Обновляем активный CSV файл
                    self.output_file = filepath
                    messagebox.showinfo("Файл открыт", f"Выбран файл индексации: {os.path.basename(filepath)}")
                    self.status_label.config(text=f"Активный файл индексации: {os.path.basename(filepath)}")
                else:
                    messagebox.showwarning("Ошибка", "Выбранный файл не соответствует формату индексации.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть CSV файл: {e}")

    def show_extensions(self):
        # Проверяем, что существует файл для анализа
        if not os.path.exists(self.output_file):
            messagebox.showwarning("Внимание", "Нет данных для анализа. Сначала выполните индексацию.")
            return

        df = pd.read_csv(self.output_file)
        extension_counts = df['extension'].value_counts()

        top = tk.Toplevel(self.root)
        top.title("Разбивка по расширениям")
        text = tk.Text(top)
        text.pack(fill="both", expand=True)
        text.insert("1.0", "Разбивка по расширениям:\n")
        for ext, count in extension_counts.items():
            text.insert("end", f"{ext}: {count}\n")

    def show_top_files(self):
        # Проверяем, что существует файл для анализа
        if not os.path.exists(self.output_file):
            messagebox.showwarning("Внимание", "Нет данных для анализа. Сначала выполните индексацию.")
            return

        df = pd.read_csv(self.output_file)
        df = df.sort_values(by="file_size", ascending=False).head(10)

        top = tk.Toplevel(self.root)
        top.title("Топ 10 файлов по размеру")
        text = tk.Text(top)
        text.pack(fill="both", expand=True)
        text.insert("1.0", "Топ 10 файлов по размеру:\n")
        for _, row in df.iterrows():
            text.insert("end", f"{row['file_name']} - {row['file_size']} bytes\n")

    def select_folder(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.status_label.config(text=f"Выбрана папка: {self.directory}")

    def run_indexing(self):
        if not self.directory:
            messagebox.showwarning("Внимание", "Выберите папку для анализа.")
            return

        self.status_label.config(text="Индексация файлов...")
        self.progress["value"] = 0
        self.root.update_idletasks()

        self.manager = FileManager(self.directory, self.output_file)
        data = []

        files = list(self.manager.get_files())
        total_files = len(files)
        for i, filepath in enumerate(files, 1):
            mime_type, _ = mimetypes.guess_type(filepath)
            handler = self.manager.get_handler(mime_type)
            if handler:
                file_data = handler.process(filepath)
                data.append(file_data)
            self.progress["value"] = (i / total_files) * 100
            self.status_label.config(text=f"Обработано {i} из {total_files} файлов")
            self.root.update_idletasks()

        self.manager.save_results(data)
        self.status_label.config(text=f"Индексация завершена. Результаты сохранены в {self.output_file}")
        messagebox.showinfo("Завершено", "Индексация успешно завершена.")

    def show_last_index_info(self):
        if not os.path.exists(self.output_file):
            messagebox.showinfo("Информация", "Файл индексации не найден.")
            return

        last_mod_time = os.path.getmtime(self.output_file)
        minutes_ago = (time.time() - last_mod_time) / 60
        messagebox.showinfo("Последняя индексация", f"Индексация была произведена {int(minutes_ago)} минут назад.")

    def show_extensions(self):
        if not os.path.exists(self.output_file):
            messagebox.showwarning("Внимание", "Нет данных для анализа. Сначала выполните индексацию.")
            return

        df = pd.read_csv(self.output_file)
        extension_counts = df['extension'].value_counts()

        top = tk.Toplevel(self.root)
        top.title("Разбивка по расширениям")
        text = tk.Text(top)
        text.pack(fill="both", expand=True)
        text.insert("1.0", "Разбивка по расширениям:\n")
        for ext, count in extension_counts.items():
            text.insert("end", f"{ext}: {count}\n")

    def show_top_files(self):
        if not os.path.exists(self.output_file):
            messagebox.showwarning("Внимание", "Нет данных для анализа. Сначала выполните индексацию.")
            return

        df = pd.read_csv(self.output_file)
        df = df.sort_values(by="file_size", ascending=False).head(10)

        top = tk.Toplevel(self.root)
        top.title("Топ 10 файлов по размеру")
        text = tk.Text(top)
        text.pack(fill="both", expand=True)
        text.insert("1.0", "Топ 10 файлов по размеру:\n")
        for _, row in df.iterrows():
            text.insert("end", f"{row['file_name']} - {row['file_size']} bytes\n")

    def show_help(self):
        messagebox.showinfo("О программе", "Программа для анализа файлов. Версия 1.0. Автор: ...")

    def search_files(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Поиск файлов (каталожный поиск)")
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = FileAnalyzerApp(root)
    root.mainloop()
