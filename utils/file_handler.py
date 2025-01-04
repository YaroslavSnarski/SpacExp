import sys
import logging
import os
import time
import mimetypes
from tkinter import messagebox
from SpacExp.file_manager import FileManager
from tkinter import messagebox
import pandas as pd

from SpacExp.logging_config import setup_logging
process_logger, error_logger = setup_logging(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class FileHandler:
    """
    Класс для обработки и индексации файлов в указанной директории.

    Предоставляет функциональность для индексирования файлов с помощью 
    обработчиков, сохранения результатов индексации и отображения информации 
    о последней индексации.
    """
    def __init__(self, directory, output_file, progress, status_label):
        """
        Инициализация обработчика файлов.

        Параметры:
        ----------
        directory : str
            Путь к директории, в которой будут индексироваться файлы.
        output_file : str
            Имя выходного файла, в котором будут сохранены результаты индексации.
        progress : tkinter.Progressbar
            Виджет для отображения прогресса обработки.
        status_label : tkinter.Label
            Метка для отображения статуса индексации.
        """
        self.directory = directory
        # setting the output file path to always save in the project root
        self.output_file = output_file
        self.progress = progress
        self.status_label = status_label

    def index_files(self):
        """
        Индексирует файлы в указанной директории.

        Этот метод перебирает файлы в директории, определяет их MIME-тип 
        и обрабатывает их с помощью подходящего обработчика. Результаты сохраняются
        в выходной файл. Также обновляет прогресс и статус обработки в интерфейсе.
        """
        self.progress["value"] = 0
        manager = FileManager(self.directory, self.output_file)
        data = []
        files = list(manager.get_files())
        total_files = len(files)

        for i, filepath in enumerate(files, 1):
            mime_type, _ = mimetypes.guess_type(filepath)
            handler = manager.get_handler(mime_type)
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
            self.status_label.update_idletasks()  # адпейт интерфейса после изменения текста
            self.progress.update_idletasks()      # адпейт интерфейса после изменения прогресса

        manager.save_results(data)
        self.status_label.config(text=f"Индексация завершена. Результаты сохранены в {self.output_file}")

    def show_last_index_info(self):
        """
        Показывает информацию о времени последней индексации.

        Если файл с результатами индексации существует, выводит окно сообщения
        с указанием, сколько минут назад была выполнена последняя индексация.
        """
        if os.path.exists(self.output_file):
            last_mod_time = os.path.getmtime(self.output_file)
            minutes_ago = (time.time() - last_mod_time) / 60
            messagebox.showinfo("Последняя индексация", f"Индексация была произведена {int(minutes_ago)} минут назад.")
