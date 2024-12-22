import os, sys
import mimetypes
import time
import logging
import pandas as pd
import math
from datetime import datetime
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .docx_processor import DOCXProcessor#, DOCProcessor
from .excel_processor import ExcelProcessor
from .audio_processor import AudioProcessor
from .video_processor import VideoProcessor
from .base_processor import FileProcessor
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'SpacExpWeb'))))
from api.models import FileRecord
import pythoncom

# importing web-versions of all the classes

from .pdf_processor import PDFProcessorWeb
from .image_processor import ImageProcessorWeb
from .docx_processor import DOCXProcessorWeb
from .audio_processor import AudioProcessorWeb
from .excel_processor import ExcelProcessorWeb 
from .video_processor import VideoProcessorWeb  

# initialising COM
pythoncom.CoInitialize()

process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')


class FileManager:
    def __init__(self, directory, output_file):
        self.directory = directory
        self.output_file = output_file
        self.default_handler = FileProcessor()
        self.handlers = {
            'application/pdf': PDFProcessor(),
            'image': ImageProcessor(),
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DOCXProcessor(),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelProcessor(),
            'application/msword': DOCXProcessor(),
            'audio': AudioProcessor(),
            'video': VideoProcessor(),
        }

    def run(self):
        try:
            start_time = time.time()
            data = []

            for filepath in self.get_files():
                try:
                    mime_type, _ = mimetypes.guess_type(filepath)
                    handler = self.get_handler(mime_type)
                    if handler:
                        file_data = handler.process(filepath)
                    else:
                        file_data = self.default_handler.get_generic_info(filepath)
                
                    if file_data:
                        data.append(file_data)
                except Exception as e:
                    error_logger.error(f"Error processing {filepath}: {e}")
        
            self.save_results(data)
            total_time = time.time() - start_time
            process_logger.info(f"Total processing time: {total_time:.2f} seconds")
        except Exception as e:
            error_logger.error(f"Error in FileManager run: {str(e)}")
            raise

    def get_files(self):
        """Итерирует файлы в указанной директории."""
        for root, _, files in os.walk(self.directory):
            for file in files:
                yield os.path.join(root, file)

    def get_handler(self, mime_type):
        """Возвращает обработчик для MIME-типа."""
        if not mime_type:
            return None
        for key, handler in self.handlers.items():
            if mime_type.startswith(key):
                return handler
        return None

    def import_csv_to_db(self, csv_file_path):
        """Импортирует CSV данные в базу данных."""
        if FileRecord.objects.exists():
            FileRecord.objects.all().delete()

        data = pd.read_csv(csv_file_path)
        for _, row in data.iterrows():
            try:
                file_size = row['file_size'] if not math.isnan(row['file_size']) else 0
                width = self.safe_float(row.get('width'))
                height = self.safe_float(row.get('height'))
                page_count = self.safe_float(row.get('page_count'))
                creation_time = self.parse_datetime(row.get('creation_time'))
                modification_time = self.parse_datetime(row.get('modification_time'))

                FileRecord.objects.create(
                    file_path=row['file_path'],
                    file_name=row['file_name'],
                    file_size=file_size,
                    creation_time=creation_time or datetime.now(),
                    modification_time=modification_time or datetime.now(),
                    extension=row['extension'],
                    width=width,
                    height=height,
                    page_count=page_count,
                )
            except Exception as e:
                error_logger.error(f"Error importing row: {row} - {e}")

        process_logger.info("CSV data imported to the database.")

    def parse_datetime(self, value):
        """Преобразует строку в формат datetime."""
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                error_logger.error(f"Invalid datetime format: {value}")
        return None

    def safe_float(self, value):
        """Безопасно преобразует значение в float."""
        try:
            return float(value) if not math.isnan(value) else None
        except (ValueError, TypeError):
            return None

    def save_results(self, data):
        """Сохраняет результаты в CSV файл."""
        process_logger.info(f"Total files processed: {len(data)}")
        if data:
            df = pd.DataFrame(data)
            df.to_csv(self.output_file, index=False)
            self.import_csv_to_db(self.output_file)
            process_logger.info(f"Results saved to {self.output_file}")

    def get_results(self):
        """Возвращает результаты обработки в виде словаря."""
        return pd.read_csv(self.output_file).to_dict(orient='records')


class FileManagerWeb:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def process_files(self):
        results = []
        for root, _, files in os.walk(self.folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                extension = os.path.splitext(file_name)[1].lower()
                processor = None

                # Обработка PDF
                if extension == ".pdf":
                    processor = PDFProcessorWeb()
                # Обработка изображений
                elif extension in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
                    processor = ImageProcessorWeb()  
                # Обработка документов Word
                elif extension in [".doc", ".docx"]:
                    processor = DOCXProcessorWeb()  
                # Обработка аудио
                elif extension in [".mp3", ".wav", ".flac", ".aac", ".ogg"]:
                    processor = AudioProcessorWeb()  
                # Обработка excel
                elif extension in [".xls", ".xlsx"]:
                    processor = ExcelProcessorWeb()  
                # Обработка видео
                elif extension in [".mp4", ".avi", ".mov", ".mkv", ".flv"]:
                    processor = VideoProcessorWeb()  

                if processor:
                    # передаем `file_path` в `process` метод для всех типов файлов
                    result = processor.process(file_path)

                    # общие данные о файле
                    result.update({
                        "file_name": file_name,
                        "file_size": os.path.getsize(file_path),
                        "creation_time": datetime.fromtimestamp(os.path.getctime(file_path)),
                        "modification_time": datetime.fromtimestamp(os.path.getmtime(file_path)),
                        "type": self.get_file_type(file_path)  # Добавляем тип файла
                    })
                    results.append(result)
                else:
                    results.append({"file_name": file_name, "file_size": os.path.getsize(file_path), "type": "unknown"})

        return results

    def get_file_type(self, file_path):
        """Возвращает тип файла, например, 'audio', 'image', 'document' и т.д."""
        extension = os.path.splitext(file_path)[1].lower()
        if extension in [".mp3", ".wav", ".flac", ".aac", ".ogg"]:
            return "audio"
        elif extension in [".pdf"]:
            return "pdf"
        elif extension in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
            return "image"
        elif extension in [".doc", ".docx"]:
            return "document"
        elif extension in [".xls", ".xlsx"]:
            return "excel"  
        elif extension in [".mp4", ".avi", ".mov", ".mkv", ".flv"]:
            return "video"  
        # другие типы файлов
        return "unknown"
