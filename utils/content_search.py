import os
import docx
import logging
from PyPDF2 import PdfReader
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentSearcher:
    """
    Класс для поиска строки в текстовых файлах (.txt), документах Word (.docx)
    и PDF-файлах в указанной директории.
    """
    def __init__(self, directory):
        """
        Инициализирует объект ContentSearcher.

        Параметры:
        -----------
        directory : str
            Путь к директории, в которой будет происходить поиск.
        """
        self.directory = directory

    def search(self, search_string):
        """
        Выполняет поиск заданной строки в файлах указанной директории.

        Параметры:
        -----------
        search_string : str
            Строка для поиска в содержимом файлов.

        Возвращает:
        -----------
        list
            Список файлов, в которых была найдена строка.
        """
        results = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                filepath = os.path.join(root, file)
                if file.endswith('.txt'):
                    if self.search_in_txt(filepath, search_string):
                        results.append(filepath)
                elif file.endswith('.docx'):
                    if self.search_in_docx(filepath, search_string):
                        results.append(filepath)
                elif file.endswith('.pdf'):
                    if self.search_in_pdf(filepath, search_string):
                        results.append(filepath)
        return results

    def search_in_txt(self, filepath, search_string):
        """
        Поиск строки в текстовом файле (.txt).

        Параметры:
        -----------
        filepath : str
            Путь к текстовому файлу.
        search_string : str
            Строка для поиска.

        Возвращает:
        -----------
        bool
            True, если строка найдена, иначе False.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                if search_string.lower() in content.lower():
                    logger.info(f"Found in {filepath}")
                    return True
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
        return False

    def search_in_docx(self, filepath, search_string):
        """
        Поиск строки в документе Word (.docx).

        Параметры:
        -----------
        filepath : str
            Путь к документу Word.
        search_string : str
            Строка для поиска.

        Возвращает:
        -----------
        bool
            True, если строка найдена, иначе False.
        """
        try:
            doc = docx.Document(filepath)
            for paragraph in doc.paragraphs:
                if search_string.lower() in paragraph.text.lower():
                    logger.info(f"Found in {filepath}")
                    return True
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
        return False

    def search_in_pdf(self, filepath, search_string):
        """
        Поиск строки в PDF-файле.

        Параметры:
        -----------
        filepath : str
            Путь к PDF-файлу.
        search_string : str
            Строка для поиска.

        Возвращает:
        -----------
        bool
            True, если строка найдена, иначе False.
        """
        try:
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    if search_string.lower() in page.extract_text().lower():
                        logger.info(f"Found in {filepath}")
                        return True
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
        return False
