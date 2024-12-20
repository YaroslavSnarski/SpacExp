import os
import mimetypes
import time
import logging
import pandas as pd
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .docx_processor import DOCXProcessor, DOCProcessor
from .excel_processor import ExcelProcessor
from .audio_processor import AudioProcessor
from .video_processor import VideoProcessor
from .base_processor import FileProcessor
#from spacexapp.views import import_csv_to_db  # Импортируем функцию из views
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

#    def save_results(self, data):
#        df = pd.DataFrame(data)
#        df.to_csv(self.output_file, index=False)
#        process_logger.info(f"Results saved to {self.output_file}")

    def import_csv_to_db(csv_file_path):
        data = pd.read_csv(csv_file_path)
        for _, row in data.iterrows():
            FileAnalysis.objects.create(
                file_path=row['file_path'],
                file_name=row['file_name'],
                file_size=row['file_size'],
                creation_time=row['creation_time'],
                modification_time=row['modification_time'],
                extension=row['extension'],
                width=row.get('width'),
                height=row.get('height'),
                page_count=row.get('page_count')
        )

#    def save_results(self, data):
#    	# Логируем количество файлов для проверки
#        process_logger.info(f"Total files processed: {len(data)}")
#        if len(data) > 0:
#            process_logger.info(f"Sample data: {data[0]}")  # Логируем данные первого файла
#            df = pd.DataFrame(data)
#            df.to_csv(self.output_file, index=False)
#            process_logger.info(f"Results saved to {self.output_file}")
#            import_csv_to_db(self.output_file) # Импортируем данные из CSV в базу данных


    def get_results(self):
        # Читаем результаты из CSV (если вы сохраняете их в CSV)
        return pd.read_csv(self.output_file).to_dict(orient='records')
