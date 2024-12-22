import pandas as pd
from docx import Document
from win32com.client import Dispatch
from PIL import Image, ExifTags
import os
import logging
from datetime import datetime
from docx import Document
from mutagen import File as MutagenFile
import sys
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
log_file = os.path.join(project_root, 'file_analyzer.log')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler() 
    ]
)

# Логгер для ошибок
error_logger = logging.getLogger('error')
error_logger.setLevel(logging.ERROR)

# Логгер для процесса
process_logger = logging.getLogger('process')
process_logger.setLevel(logging.INFO)

class FileProcessor:
    def __init__(self, default_author="Unknown Author"):
        self.default_author = default_author

    def get_generic_info(self, filepath):
        stats = os.stat(filepath)
        creation_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        extension = os.path.splitext(filepath)[1][1:]
        try:
            return {
            "file_path": filepath,
            "file_name": os.path.basename(filepath),
            "file_size": stats.st_size,
            "creation_time": creation_time,
            "modification_time": modification_time,
            "extension": extension
            }
        except Exception as e:
            # logging errors if no access to file
            error_logger.error(f"Failed to get info for file {filepath}: {e}")
            return None  # skipping errors
