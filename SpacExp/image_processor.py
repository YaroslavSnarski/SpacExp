from PIL import Image, ExifTags
from .base_processor import FileProcessor
import time, os
from .logging_config import setup_logging

# логгирование
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
process_logger, error_logger = setup_logging(project_root)

class ImageProcessor(FileProcessor):
    """
    Класс для обработки изображений.

    Наследуется:
        FileProcessor: Базовый класс для обработки файлов.

    Методы:
        process(filepath): Извлекает информацию о размере изображения, DPI, метаданных EXIF.
    """
    def __init__(self):
        """
        Инициализирует объект ImageProcessor с набором всех уникальных ключей EXIF, 
        которые встречаются во время обработки.
        """
        self.all_exif_keys = set()
    def process(self, filepath):
        """
        Обрабатывает изображение и извлекает параметры, такие как размер, DPI и EXIF-данные.

        Args:
            filepath (str): Путь к изображению.

        Returns:
            dict: Словарь с информацией об изображении, включая:
                - image_width (int): Ширина изображения.
                - image_height (int): Высота изображения.
                - dpi_x (float или None): DPI по горизонтали.
                - dpi_y (float или None): DPI по вертикали.
                - exif_data (dict): Словарь с сырыми EXIF-данными.
                - exif_* (различные ключи EXIF): Индивидуальные данные EXIF.

            В случае ошибки возвращает словарь с ключом "error" и описанием ошибки.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            with Image.open(filepath) as img:
                width, height = img.size
                dpi = img.info.get('dpi', (None, None))
                exif_data = img.getexif()
                exif = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()} if exif_data else {}

                file_info.update({
                    "image_width": width,
                    "image_height": height,
                    "dpi_x": dpi[0],
                    "dpi_y": dpi[1],
                    "exif_data": exif,
                })

                # tracking all unique exif keys encountered
                self.all_exif_keys.update(exif.keys())

                # adding each exif key-value pair to file_info, or None if key is missing
                for key in self.all_exif_keys:
                    file_info[f"exif_{key}"] = exif.get(key, None)

            elapsed_time = time.time() - start_time
            process_logger.info(f"Image processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing image {filepath}: {e}")
            return {"error": str(e)}

class ImageProcessorWeb(FileProcessor):
    """
    Класс для обработки изображений в веб-приложении.

    Наследуется:
        FileProcessor: Базовый класс для обработки файлов.

    Методы:
        process(file_path): Извлекает информацию о размере изображения и типе файла.
    """
    def __init__(self):
        """
        Инициализация объекта ImageProcessorWeb.
        """
        super().__init__()

    def process(self, file_path):
        """
        Обрабатывает изображение, извлекая его параметры, такие как ширина и высота.

        Args:
            file_path (str): Путь к изображению.

        Returns:
            dict: Словарь с информацией об изображении, включая:
                - type (str): Тип файла (всегда "image").
                - width (int): Ширина изображения.
                - height (int): Высота изображения.

            В случае ошибки возвращает словарь с ключом "error" и описанием ошибки.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(file_path)
            
            # processing images
            with Image.open(file_path) as img:
                width, height = img.size  # size of an image

            file_info.update({
                "type": "image",  # type specified
                "width": width,
                "height": height,
                # additional meta-data if needed in future
            })

            elapsed_time = time.time() - start_time
            process_logger.info(f"Image processed: {file_path} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing image {file_path}: {e}")
            return {"type": "image", "error": str(e)}  # setting the type despite an error
