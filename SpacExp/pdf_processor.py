# pdf_processor.py

import time
import logging
from PyPDF2 import PdfReader
from datetime import datetime
from .base_processor import FileProcessor
import re
import time
import PyPDF2 
process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')

class PDFProcessor(FileProcessor):
    def process(self, filepath):
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
    def __init__(self, file_path=None):
        super().__init__()

    def process(self, file_path):
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
