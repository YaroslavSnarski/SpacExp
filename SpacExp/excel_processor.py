import openpyxl
from .base_processor import FileProcessor
import logging
import time
import xlrd

error_logger = logging.getLogger('error')
process_logger = logging.getLogger('process')

class ExcelProcessor(FileProcessor):
    def process(self, filepath):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            workbook = openpyxl.load_workbook(filepath)
            file_info.update({"num_sheets": len(workbook.sheetnames)})

            elapsed_time = time.time() - start_time
            process_logger.info(f"Excel processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing Excel {filepath}: {e}")
            return {"error": str(e)}

class ExcelProcessorWeb(FileProcessor):
    def process(self, filepath):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)
            extension = filepath.split('.')[-1].lower()

            if extension == "xls":
                # Обработка .xls файлов с помощью xlrd
                workbook = xlrd.open_workbook(filepath)
                sheet_names = workbook.sheet_names()
            elif extension == "xlsx":
                # Обработка .xlsx файлов с помощью openpyxl
                workbook = openpyxl.load_workbook(filepath)
                sheet_names = workbook.sheetnames
            else:
                raise ValueError("Unsupported Excel file format")

            file_info.update({
                "num_sheets": len(sheet_names),
                "sheet_names": sheet_names  # adding sheets names to results
            })

            elapsed_time = time.time() - start_time
            process_logger.info(f"Excel processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing Excel {filepath}: {e}")
            return {"error": str(e)}
