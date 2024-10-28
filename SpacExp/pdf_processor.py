
# pdf_processor.py

import time
import logging
from PyPDF2 import PdfReader
from datetime import datetime
from .base_processor import FileProcessor
import re

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

#    def parse_pdf_date(self, date_str):
#        if date_str.startswith('D:'):
#            date_str = date_str[2:].split('+')[0].replace("Z", "")
#            return datetime.strptime(date_str, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
#        return date_str

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
