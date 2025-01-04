import os
from datetime import datetime
from .logging_config import setup_logging
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
process_logger, error_logger = setup_logging(project_root)

class FileProcessor:
    """
    Класс для обработки файлов. Предоставляет базовые методы для получения информации о файле.

    Аргументы:
        default_author (str): Имя автора по умолчанию. Используется для тегирования файлов, если автор не указан.
    """
    def __init__(self, default_author="Unknown Author"):
        """
        Инициализирует объект FileProcessor с указанным именем автора по умолчанию.

        Аргументы:
            default_author (str): Имя автора, используемое по умолчанию для файлов.
        """
        self.default_author = default_author

    def get_generic_info(self, filepath):
        """
        Извлекает общую информацию о файле: размер, время создания, время последней модификации и расширение.

        Аргументы:
            filepath (str): Путь к файлу, для которого требуется получить информацию.

        Возвращает:
            dict: Словарь с информацией о файле, включая:
                  - 'file_path': Путь к файлу.
                  - 'file_name': Имя файла.
                  - 'file_size': Размер файла в байтах.
                  - 'creation_time': Время создания файла.
                  - 'modification_time': Время последней модификации файла.
                  - 'extension': Расширение файла.
                  
            Если возникает ошибка при доступе к файлу, возвращается None, и ошибка записывается в лог.
        """
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
