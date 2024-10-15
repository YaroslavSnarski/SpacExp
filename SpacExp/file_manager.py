import os
import mimetypes
import time
import logging
import pandas as pd
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .docx_processor import DOCXProcessor
from .excel_processor import ExcelProcessor
from .audio_processor import AudioProcessor
from .video_processor import VideoProcessor

process_logger = logging.getLogger('process')
error_logger = logging.getLogger('error')

class FileManager:
    def __init__(self, directory, output_file):
        self.directory = directory
        self.output_file = output_file

        self.handlers = {
            'application/pdf': PDFProcessor(),
            'image': ImageProcessor(),
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DOCXProcessor(),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelProcessor(),
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
                data.append(file_data)
            else:
                process_logger.warning(f"Unsupported file type: {filepath}")

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

    def save_results(self, data):
        df = pd.DataFrame(data)
        df.to_csv(self.output_file, index=False)
        process_logger.info(f"Results saved to {self.output_file}")