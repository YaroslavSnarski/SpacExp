import tkinter as tk
from tkinter import messagebox, filedialog
#from utils.statistics_view import StatisticsView

class MenuCreator:
    def __init__(self, app):
        menubar = tk.Menu(app.root)
        app.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть CSV файл", command=app.open_csv)
        file_menu.add_command(label="Выход", command=app.root.quit)

        actions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Действия программы", menu=actions_menu)
        
        stats_menu = tk.Menu(actions_menu, tearoff=0)
        actions_menu.add_cascade(label="Действия со статистикой", menu=stats_menu)
        stats_menu.add_command(label="Аналитика по расширениям", command=app.show_extensions)
        stats_menu.add_command(label="Топ-10 файлов по размеру", command=app.show_top_files)
        stats_menu.add_command(label="Показать график топ-10 файлов", command=app.statistics_view.show_top_files_chart)
        stats_menu.add_command(label="Каталожный поиск", command=app.search_files)
        stats_menu.add_command(label="Поиск по содержимому", command=app.search_content)

        program_menu = tk.Menu(actions_menu, tearoff=0)
        actions_menu.add_cascade(label="Управление программой", menu=program_menu)
        program_menu.add_command(label="Выбор папки", command=app.select_folder)
        program_menu.add_command(label="Индексация содержимого", command=app.run_indexing)
        program_menu.add_command(label="Сведения о последней индексации", command=app.show_last_index_info)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="О программе", menu=about_menu)
#        about_menu.add_command(label="Справка", command=lambda: tk.messagebox.showinfo("О программе", "Версия 0.1"))
        about_menu.add_command(label="Справка", command=self.show_help)


    def show_help(self):
        messagebox.showinfo("О программе", "Программа для анализа каталога файлов. Версия 0.1. Автор: Yaroslav Snarski")
