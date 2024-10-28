import sys
import logging
import os
import time
import mimetypes
from tkinter import messagebox
from SpacExp.file_manager import FileManager
from tkinter import messagebox
import pandas as pd

# Add the project root directory to the Python path
#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.insert(0, project_root)
process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')


class FileHandler:
    def __init__(self, directory, output_file, progress, status_label):
        self.directory = directory
        # Set the output file path to always save in the project root
        self.output_file = output_file # os.path.join(project_root, output_file)
        self.progress = progress
        self.status_label = status_label

    def index_files(self):
        self.progress["value"] = 0
        manager = FileManager(self.directory, self.output_file)
        data = []
        files = list(manager.get_files())
        total_files = len(files)

        for i, filepath in enumerate(files, 1):
            mime_type, _ = mimetypes.guess_type(filepath)
            handler = manager.get_handler(mime_type)
#            if handler:
#                data.append(handler.process(filepath))
            if handler:
                file_data = handler.process(filepath)
            else:
                # Используем стандартный обработчик для получения общей информации
                file_data = manager.default_handler.get_generic_info(filepath)
                process_logger.warning(f"Unsupported file type. Processed with default handler: {filepath}")
            
            if file_data:
                data.append(file_data)  # Добавляем данные в итоговый список


            self.progress["value"] = (i / total_files) * 100
            self.status_label.config(text=f"Обработано {i} из {total_files} файлов")
            self.status_label.update_idletasks()  # Обновляем интерфейс после изменения текста
            self.progress.update_idletasks()      # Обновляем интерфейс после изменения прогресса

        manager.save_results(data)
        self.status_label.config(text=f"Индексация завершена. Результаты сохранены в {self.output_file}")

    def show_last_index_info(self):
        if os.path.exists(self.output_file):
            last_mod_time = os.path.getmtime(self.output_file)
            minutes_ago = (time.time() - last_mod_time) / 60
            messagebox.showinfo("Последняя индексация", f"Индексация была произведена {int(minutes_ago)} минут назад.")
