import os
import mimetypes
import time
import logging
import pandas as pd
import math
from datetime import datetime

from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .docx_processor import DOCXProcessor, DOCProcessor
from .excel_processor import ExcelProcessor
from .audio_processor import AudioProcessor
from .video_processor import VideoProcessor
from .base_processor import FileProcessor
import csv  # Импортируем модуль csv для работы с CSV файлами
from spacexapp.models import FileAnalysis  # Импорт модели для базы данных


process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')


class FileManager:
    def __init__(self, directory, output_file):
        self.directory = directory
        self.output_file = output_file

        # Создаем базовый обработчик, который будет использоваться для неизвестных типов файлов
        self.default_handler = FileProcessor()

        self.handlers = {
            'application/pdf': PDFProcessor(),
            'image': ImageProcessor(),
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DOCXProcessor(),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelProcessor(),
            'application/msword': DOCProcessor(),  # Обработчик для .doc файлов
            'audio': AudioProcessor(),
            'video': VideoProcessor()
        }

    def run(self):
        start_time = time.time()
        data = []

        for filepath in self.get_files():
            mime_type, _ = mimetypes.guess_type(filepath)
            handler = self.get_handler(mime_type)
            if handler:
                file_data = handler.process(filepath)
            else:
                # Используем стандартный обработчик для получения общей информации
                file_data = self.default_handler.get_generic_info(filepath)
                process_logger.warning(f"Unsupported file type. Processed with default handler: {filepath}")
        
            if file_data:
                data.append(file_data)  # Добавляем данные в итоговый список
        self.save_results(data)
        total_time = time.time() - start_time
        process_logger.info(f"Total processing time: {total_time:.2f} seconds")

    def get_files(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                yield os.path.join(root, file)

    def get_handler(self, mime_type):
        for key in self.handlers.keys():
            if mime_type and mime_type.startswith(key):
                return self.handlers[key]
        return None




    def import_csv_to_db(self, csv_file_path):
    # Проверяем, есть ли в базе данные
        if FileAnalysis.objects.exists():  # Если таблица не пуста
            FileAnalysis.objects.all().delete()  # Удаляем все старые записи
    
    # Чтение данных из CSV файла
        data = pd.read_csv(csv_file_path)
    
    # Итерируем по строкам и добавляем записи в базу данных
        for _, row in data.iterrows():
        # Преобразуем значения в безопасные для БД
            file_size = row['file_size'] if not math.isnan(row['file_size']) else 0
            image_width = row.get('image_width') if not math.isnan(row.get('image_width', float('nan'))) else None
            image_height = row.get('image_height') if not math.isnan(row.get('image_height', float('nan'))) else None
            num_pages = row.get('num_pages') if not math.isnan(row.get('num_pages', float('nan'))) else None

        # Преобразуем время на основе наличия данных
            creation_time = self.parse_datetime(row.get('creation_time'))
            modification_time = self.parse_datetime(row.get('modification_time'))

        # Если creation_time или modification_time отсутствуют или некорректны, устанавливаем текущую дату
            if not creation_time:
                creation_time = datetime.now()
            if not modification_time:
                modification_time = datetime.now()

        # Создаем запись в базе данных
            FileAnalysis.objects.create(
                file_path=row['file_path'],
                file_name=row['file_name'],
                file_size=file_size,  # заменяем nan на 0
                creation_time=creation_time,
                modification_time=modification_time,
                extension=row['extension'],
                image_width=image_width,
                image_height=image_height,
                num_pages=num_pages
        )
        process_logger.info("Old data removed (if any) and new data imported into the database.")

    def parse_datetime(self, value):
        """Преобразует строку в формат datetime. Если значение некорректное или пустое, возвращает None."""
        if isinstance(value, str):  # Проверяем, является ли значением строкой
            try:
                return datetime.fromisoformat(value)  # Преобразуем в datetime, если строка в корректном формате
            except ValueError:
                error_logger.error(f"Invalid datetime format: {value}")
                return None  # Возвращаем None в случае ошибки
        return None  # Если не строка, возвращаем None

    def save_results(self, data):
        # Логируем количество файлов для проверки
        process_logger.info(f"Total files processed: {len(data)}")
        if len(data) > 0:
            process_logger.info(f"Sample data: {data[0]}")  # Логируем данные первого файла
            df = pd.DataFrame(data)
            df.to_csv(self.output_file, index=False)
            process_logger.info(f"Results saved to {self.output_file}")
            # Вызов метода import_csv_to_db через self
            self.import_csv_to_db(self.output_file)

    def get_results(self):
        # Читаем результаты из CSV (если вы сохраняете их в CSV)
        return pd.read_csv(self.output_file).to_dict(orient='records')
