import os
import mimetypes
import time
import pandas as pd
from datetime import datetime

# importing app classes
from .base_processor import FileProcessor
from .pdf_processor import PDFProcessor, PDFProcessorWeb
from .image_processor import ImageProcessor, ImageProcessorWeb
from .docx_processor import DOCXProcessor, DOCXProcessorWeb
from .excel_processor import ExcelProcessor, ExcelProcessorWeb
from .audio_processor import AudioProcessor, AudioProcessorWeb
from .video_processor import VideoProcessor, VideoProcessorWeb
from .logging_config import setup_logging
process_logger, error_logger = setup_logging(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class BaseFileManager:
    """Базовый класс для управления файлами."""
    def __init__(self, directory=None):
        self.default_handler = FileProcessor()
        self.directory = directory

    def get_files(self, directory=None):
        """
        Генерирует список файлов в указанной директории.
        
        :return: Путь к каждому файлу в директории.
        """
        if directory is None:
            directory = self.directory
        if not directory:
            raise ValueError("Directory path is not specified.")
        for root, _, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)

    def save_results(self, data, output_file="output_analysis.csv"):
        """
        Сохраняет результаты обработки файлов в CSV файл.

        :param data: Список с результатами обработки файлов.
        """
        process_logger.info(f"Total files processed: {len(data)}")
        if data:
            # Создаём директорию для файла, если она не существует
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            df = pd.DataFrame(data)
            df.to_csv(output_file, index=False)
            process_logger.info(f"Results saved to {output_file}")


class FileManager(BaseFileManager):
    """
    Класс для обработки файлов в указанной директории.
    Для каждого файла определяется MIME-тип, и в зависимости от типа выбирается соответствующий обработчик.
    Результаты обработки сохраняются в CSV файл.
    """
    def __init__(self, directory, output_file):
        super().__init__()
        self.directory = directory
        self.output_file = output_file
        self.handlers = {
            'application/pdf': PDFProcessor(),
            'image': ImageProcessor(),
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DOCXProcessor(),
            'application/vnd.openxmlformats-officedocument.themeManager+xml' : DOCXProcessor(),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelProcessor(),
            'application/msword': DOCXProcessor(),
            'audio': AudioProcessor(),
            'video': VideoProcessor(),
        }

    def run(self):
        """
        Запускает процесс обработки файлов в указанной директории.
        Результаты обработки сохраняются в CSV файл.
        """
        try:
            start_time = time.time()
            data = []

            for filepath in self.get_files(self.directory):
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

        # Преобразуем путь к output_file относительно директории проекта
            if not os.path.isabs(self.output_file):
                self.output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.output_file)

        # Создаем директорию, если она не существует
            output_dir = os.path.dirname(self.output_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            try:
                self.save_results(data, self.output_file)
            except Exception as e:
                error_logger.error(f"Error saving results to {self.output_file}: {e}")
                raise

            total_time = time.time() - start_time
            process_logger.info(f"Total processing time: {total_time:.2f} seconds")

        except Exception as e:
            error_logger.error(f"Error in FileManager run: {str(e)}")
            raise

    def get_handler(self, mime_type):
        """Возвращает обработчик для MIME-типа."""
        if not mime_type:
            return None
        for key, handler in self.handlers.items():
            if mime_type.startswith(key):
                return handler
        return None




class FileManagerWeb(BaseFileManager):
    """
    Класс для обработки файлов в веб-среде.
    Для каждого файла определяется расширение, и в зависимости от расширения выбирается соответствующий обработчик.
    Результаты обработки возвращаются в виде списка словарей.
    """
    def __init__(self, folder_path):
        """
        Инициализирует FileManagerWeb.
        
        :param folder_path: Путь к папке, содержащей файлы для обработки.
        """
        super().__init__()
        self.folder_path = folder_path

    def process_files(self):
        """
        Обрабатывает файлы в указанной папке.
        
        :return: Список словарей с результатами обработки файлов.
        """
        results = []
        for filepath in self.get_files(self.folder_path):
            file_name = os.path.basename(filepath)
            extension = os.path.splitext(file_name)[1].lower()

            # детектим обработчик по расширению файла
            processor = self.get_processor(extension)
            if processor:
                result = processor.process(filepath)
            else:
                result = {"file_name": file_name, "type": "unknown"}

            # общая информация о файле
            result.update({
                "file_name": file_name,
                "file_size": os.path.getsize(filepath),
                "creation_time": datetime.fromtimestamp(os.path.getctime(filepath)),
                "modification_time": datetime.fromtimestamp(os.path.getmtime(filepath)),
                "type": self.get_file_type(extension),
            })
            results.append(result)
        return results

    def get_processor(self, extension):
        """Возвращает обработчик для расширения файла."""
        match extension:
            case ".pdf":
                return PDFProcessorWeb()
            case ".png" | ".jpg" | ".jpeg" | ".bmp" | ".gif":
                return ImageProcessorWeb()
            case ".doc" | ".docx":
                return DOCXProcessorWeb()
            case ".xls" | ".xlsx":
                return ExcelProcessorWeb()
            case ".mp3" | ".wav" | ".flac" | ".aac" | ".ogg":
                return AudioProcessorWeb()
            case ".mp4" | ".avi" | ".mov" | ".mkv" | ".flv":
                return VideoProcessorWeb()
            case _:
                return None

    def get_file_type(self, extension):
        """
        Определяет тип файла на основе его расширения.
        
        :param file_path: Путь к файлу.
        :return: Тип файла.
        """
        match extension:
            case ".mp3" | ".wav" | ".flac" | ".aac" | ".ogg":
                return "audio"
            case ".pdf":
                return "pdf"
            case ".png" | ".jpg" | ".jpeg" | ".bmp" | ".gif":
                return "image"
            case ".doc" | ".docx":
                return "document"
            case ".xls" | ".xlsx":
                return "excel"
            case ".mp4" | ".avi" | ".mov" | ".mkv" | ".flv":
                return "video"
            case _:
                return "unknown"
