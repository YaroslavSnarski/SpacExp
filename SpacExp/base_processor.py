import pandas as pd
pd.set_option('display.max_columns', None)

from docx import Document
from win32com.client import Dispatch
from PIL import Image, ExifTags
import os
import logging
from datetime import datetime
import mimetypes
import csv
from datetime import datetime
import time
from PyPDF2 import PdfFileReader  # external library for PDFs
from PyPDF2 import PdfReader
from PIL import Image  # external library for images
import cv2
import docx  # external library for DOCX
from docx import Document
import openpyxl  # external library for Excel
import mutagen  # external library for audio files
import moviepy.editor as mp  # external library for video files
from mutagen import File as MutagenFile

# Для логирования создадим два лог-файла: 
# - один для ошибок (error.log),
# - другой для успешных операций (process.log).
# Логи будут хранить информацию об ошибках и успешных операциях с файлами.


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("process_goldstandard.log"),
        logging.FileHandler("error_goldstandard.log"),
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

        return {
            "file_path": filepath,
            "file_name": os.path.basename(filepath),
            "file_size": stats.st_size,
            "creation_time": creation_time,
            "modification_time": modification_time
        }
