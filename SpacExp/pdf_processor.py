# pdf_processor.py
import time, os
import logging
from PyPDF2 import PdfReader
from datetime import datetime
from .base_processor import FileProcessor
import re
import PyPDF2 
from .logging_config import setup_logging

# логгирование
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
process_logger, error_logger = setup_logging(project_root)

class PDFProcessor(FileProcessor):
    """
    Класс для обработки PDF-файлов.

    Наследуется:
        FileProcessor: Базовый класс для обработки файлов.

    Методы:
        process(filepath): Извлекает информацию из PDF-файла, включая метаданные и количество страниц.
        parse_pdf_date(date_str): Парсит дату в формате PDF в читаемый формат.
    """
    def process(self, filepath):
        """
        Обрабатывает PDF-файл и извлекает его параметры, такие как количество страниц и метаданные.

        Args:
            filepath (str): Путь к PDF-файлу.

        Returns:
            dict: Словарь с информацией о PDF-файле, включая:
                - num_pages (int): Количество страниц.
                - pdf_author (str): Автор документа.
                - pdf_title (str): Название документа.
                - pdf_creation_date (str): Дата создания документа.
                - pdf_modification_date (str): Дата изменения документа.
                - Любые общие параметры из метода `get_generic_info`.

            В случае ошибки возвращает словарь с ключом "error" и описанием ошибки.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            reader = PdfReader(filepath)
            num_pages = len(reader.pages)
            pdf_info = reader.metadata

            file_info.update({
                "num_pages": num_pages,
                "pdf_author": pdf_info.get('/Author', self.default_author),
                "pdf_title": pdf_info.get('/Title', 'N/A'),
                "pdf_creation_date": self.parse_pdf_date(pdf_info.get('/CreationDate', 'D:00010101000000Z')),
                "pdf_modification_date": self.parse_pdf_date(pdf_info.get('/ModDate', 'D:00010101000000Z')),
            })

            elapsed_time = time.time() - start_time
            process_logger.info(f"PDF processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing PDF {filepath}: {e}")
            return {"error": str(e)}

    def parse_pdf_date(self, date_str):
        """
        Парсит дату в формате PDF в читаемый формат (YYYY-MM-DD HH:MM:SS).

        Args:
            date_str (str): Дата в формате PDF, например, 'D:YYYYMMDDHHMMSS'.

        Returns:
            str: Парсенная дата в читаемом формате. Если парсинг невозможен, возвращается "Unknown Date".
        """
        if date_str.startswith('D:'):
            # Remove 'D:' prefix and split timezone offset, if any
            date_str = date_str[2:]
            date_main_part = re.split(r'[\+\-]', date_str)[0]  # Splits and keeps only the main date

            try:
                parsed_date = datetime.strptime(date_main_part, '%Y%m%d%H%M%S')
                return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                error_logger.error(f"Date parsing error for {date_str}")
                return "Unknown Date"
        return date_str

class PDFProcessorWeb(FileProcessor):
    """
    Класс для обработки PDF-файлов в веб-приложении.

    Наследуется:
        FileProcessor: Базовый класс для обработки файлов.

    Методы:
        process(file_path): Извлекает информацию из PDF-файла для использования в веб-приложении.
    """
    def __init__(self, file_path=None):
        """
        Инициализирует процессор PDF-файлов для веб-приложений.

        Args:
            file_path (str, optional): Путь к файлу. По умолчанию None.
        """
        super().__init__()

    def process(self, file_path):
        """
        Обрабатывает PDF-файл, извлекая информацию о количестве страниц и типе файла.

        Args:
            file_path (str): Путь к PDF-файлу.

        Returns:
            dict: Словарь с информацией о PDF-файле, включая:
                - type (str): Тип файла (всегда "pdf").
                - page_count (int): Количество страниц.
            
            В случае ошибки возвращает словарь с ключом "error" и описанием ошибки.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(file_path)
            
            pdf_file = PyPDF2.PdfReader(file_path)
            page_count = len(pdf_file.pages)  # страницы

            file_info.update({
                "type": "pdf",  # тип файла
                "page_count": page_count,
                # any meta-data
            })

            elapsed_time = time.time() - start_time
            logging.info(f"PDF processed: {file_path} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            logging.error(f"Error processing PDF {file_path}: {e}")
            return {"type": "pdf", "error": str(e)}  # setting error type
