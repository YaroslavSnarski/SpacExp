from .base_processor import FileProcessor
from win32com.client import Dispatch
import logging
import os
import pythoncom
import win32com.client
import time
from docx import Document 

process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')

class DOCXProcessor(FileProcessor):
    def __init__(self, default_author="Unknown Author"):
        super().__init__(default_author=default_author)

    def process(self, filepath):
        """Обрабатывает файл DOCX или DOC и возвращает информацию."""
        return self.get_document_info(filepath)

    def get_doc_info_with_com(self, filepath):
        """Использует COM для извлечения метаданных и подсчёта страниц."""
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            error_logger.error(f"File not found: {filepath}")
            return None

        pythoncom.CoInitialize()
        word = None
        try:
            word = Dispatch("Word.Application")
            doc = word.Documents.Open(filepath, ReadOnly=True)
            properties = {
                "author": doc.BuiltInDocumentProperties("Author").Value,
                "title": doc.BuiltInDocumentProperties("Title").Value,
                "page_count": doc.ComputeStatistics(2),  # wdStatisticPages
            }
            process_logger.info(f"Extracted COM properties for {filepath}")
            doc.Close(False)
            return properties
        except Exception as e:
            error_logger.error(f"COM processing failed for {filepath}: {e}")
            return None
        finally:
            if word:
                word.Quit()
            pythoncom.CoUninitialize()

    def get_docx_page_count(self, filepath):
        """Оценивает количество страниц в DOCX файле через COM."""
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            error_logger.error(f"File not found: {filepath}")
            return None

        pythoncom.CoInitialize()
        word = None
        try:
            word = Dispatch("Word.Application")
            doc = word.Documents.Open(filepath, ReadOnly=True)
            page_count = doc.ComputeStatistics(2)  # wdStatisticPages
            process_logger.info(f"Calculated page count for {filepath}: {page_count}")
            doc.Close(False)
            return page_count
        except Exception as e:
            error_logger.error(f"Failed to estimate pages for DOCX file {filepath}: {e}")
            return None
        finally:
            if word:
                word.Quit()
            pythoncom.CoUninitialize()

    def get_docx_info(self, filepath):
        """Извлекает информацию из DOCX файлов."""
        process_logger.info(f"Processing DOCX file: {filepath}")
        page_count = self.get_docx_page_count(filepath)
        return {
            "author": self.default_author,  # Метаданные авторства не поддерживаются напрямую
            "title": "Unknown Title",  # Извлечение заголовка можно добавить при необходимости
            "page_count": page_count,
        }

    def get_doc_info(self, filepath):
        """Извлекает информацию из DOC файлов."""
        process_logger.info(f"Processing DOC file: {filepath}")
        return self.get_doc_info_with_com(filepath)

    def get_document_info(self, filepath):
        """Основной метод для обработки DOCX и DOC файлов."""
        file_info = self.get_generic_info(filepath)
        if file_info is None:
            return None

        extension = file_info.get("extension")
        if extension == "docx":
            doc_info = self.get_docx_info(filepath)
        elif extension == "doc":
            doc_info = self.get_doc_info(filepath)
        else:
            error_logger.error(f"Unsupported file type: {filepath}")
            return None

        if doc_info:
            file_info.update(doc_info)
            process_logger.info(f"Successfully processed: {filepath}")
        else:
            error_logger.error(f"Failed to process: {filepath}")

        return file_info

class DOCXProcessorWeb(FileProcessor):
    def __init__(self, file_path=None):
        super().__init__()
        # Инициализация для DOCXProcessorWeb (если нужно)

    def process(self, file_path):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(file_path)
            
            extension = file_path.split('.')[-1].lower()

            # Обработка .doc и .docx файлов через win32com
            if extension == "doc" or extension == "docx":
                page_count = self.count_word_pages(file_path)
            else:
                raise ValueError(f"Unsupported file extension: {extension}")

            file_info.update({
                "type": "document",  # Указываем тип файла
                "page_count": page_count,
            })

            elapsed_time = time.time() - start_time
            logging.info(f"DOCX processed: {file_path} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            logging.error(f"Error processing DOCX {file_path}: {e}")
            return {"type": "document", "error": str(e)}  # Устанавливаем тип даже при ошибке

    def count_word_pages(self, file_path):
        """Функция для подсчета страниц в .doc и .docx файле с помощью win32com."""
        try:
            pythoncom.CoInitialize()
            word_app = win32com.client.Dispatch("Word.Application")
            word_app.Visible = False  # Отключаем отображение приложения Word
            try:
                # Открытие файла в режиме только для чтения
                doc = word_app.Documents.Open(file_path, ReadOnly=True)
                page_count = doc.ComputeStatistics(2)  # wdStatisticPages = 2
                doc.Close()
            finally:
                word_app.Quit()
                pythoncom.CoUninitialize()
            return page_count
        except Exception as e:
            logging.error(f"Error counting Word pages for file {file_path}: {e}")
            return None
