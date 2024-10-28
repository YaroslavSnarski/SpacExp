# Импортируем базовый процессор и необходимые библиотеки
from .base_processor import FileProcessor
from docx import Document
from win32com.client import Dispatch
import logging
import os

process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')

class DOCXProcessor(FileProcessor):
    def __init__(self, default_author="Unknown Author"):
        super().__init__(default_author=default_author)

    def process(self, filepath):
        """Основной метод для обработки файла и получения его информации."""
        return self.get_document_info(filepath)

    def get_doc_info_with_com(self, filepath):
        """Используем COM для получения точной информации о количестве страниц."""
        try:
            # Преобразуем путь в абсолютный формат
            filepath = os.path.abspath(filepath)
            # Проверка, что файл существует
            if not os.path.exists(filepath):
                error_logger.error(f"File not found: {filepath}")
                return None
            word = Dispatch("Word.Application")
            doc = word.Documents.Open(filepath)
            properties = {
                "author": doc.BuiltInDocumentProperties("Author").Value,
                "title": doc.BuiltInDocumentProperties("Title").Value,
                "page_count": doc.ComputeStatistics(2)  # 2 = wdStatisticPages
            }
            doc.Close(False)
            word.Quit()
            return properties
        except Exception as e:
            error_logger.error(f"Failed to get info for {filepath} using COM: {e}")
            return None

    def get_docx_info(self, filepath):
        """Метод для получения информации из .docx файлов."""
        return self.get_doc_info_with_com(filepath)

    def get_doc_info(self, filepath):
        """Метод для получения информации из .doc файлов через COM-интерфейс."""
        return self.get_doc_info_with_com(filepath)

    def get_document_info(self, filepath):
        """Основной метод для обработки файлов .docx и .doc."""
        file_info = self.get_generic_info(filepath)
        if file_info is None:
            return None

        extension = file_info.get("extension")
        if extension in ["docx", "doc"]:
            doc_info = self.get_doc_info_with_com(filepath)
        else:
            error_logger.error(f"Unsupported file type for DOCXProcessor: {filepath}")
            return None

        if doc_info is not None:
            file_info.update(doc_info)
            process_logger.info(f"Successfully processed {filepath}")
        else:
            error_logger.error(f"Failed to extract info for {filepath}")
        
        return file_info


class DOCProcessor(FileProcessor):
    def __init__(self, default_author="Unknown Author"):
        super().__init__(default_author=default_author)

    def process(self, filepath):
        """Основной метод для обработки файла и получения его информации."""
        return self.get_document_info(filepath)

    def get_doc_info(self, filepath):
        """Метод для получения информации из .doc файлов через COM-интерфейс."""
        try:
            word = Dispatch("Word.Application")
            doc = word.Documents.Open(filepath)
            properties = {
                "author": doc.BuiltInDocumentProperties("Author").Value,
                "title": doc.BuiltInDocumentProperties("Title").Value,
                "page_count": doc.ComputeStatistics(2)  # 2 = wdStatisticPages
            }
            doc.Close(False)
            word.Quit()
            return properties
        except Exception as e:
            error_logger.error(f"Failed to get DOC info for {filepath}: {e}")
            return None

    def get_document_info(self, filepath):
        """Основной метод для обработки файлов .docx и .doc."""
        file_info = self.get_generic_info(filepath)
        if file_info is None:
            return None

        if file_info.get("extension") == "doc":
            doc_info = self.get_doc_info(filepath)
            if doc_info is not None:
                file_info.update(doc_info)
                process_logger.info(f"Successfully processed {filepath}")
            else:
                error_logger.error(f"Failed to extract info for {filepath}")
            return file_info
        else:
            error_logger.error(f"Unsupported file type for DOCProcessor: {filepath}")
            return None
