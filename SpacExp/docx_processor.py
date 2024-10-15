from docx import Document
from .base_processor import FileProcessor
import logging
import time
import pythoncom
from win32com.client import Dispatch

error_logger = logging.getLogger('error')
process_logger = logging.getLogger('process')

class DOCXProcessor(FileProcessor):
    def process(self, filepath):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            doc = Document(filepath)
            core_props = doc.core_properties
            num_pages = self.get_docx_page_count(filepath)

            file_info.update({
                "docx_author": core_props.author or self.default_author,
                "docx_title": core_props.title or 'N/A',
                "docx_page_count": num_pages,
            })

            elapsed_time = time.time() - start_time
            process_logger.info(f"DOCX processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing DOCX {filepath}: {e}")
            return {"error": str(e)}

    def get_docx_page_count(self, filepath):
        try:
            pythoncom.CoInitialize()
            word = Dispatch("Word.Application")
            doc = word.Documents.Open(filepath)
            num_pages = doc.ComputeStatistics(2)
            doc.Close(False)
            word.Quit()
            pythoncom.CoUninitialize()
            return num_pages
        except Exception as e:
            error_logger.error(f"Error getting DOCX page count {filepath}: {e}")
            return "N/A"
