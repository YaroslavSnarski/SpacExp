import cv2
from .base_processor import FileProcessor
import time, os
from .logging_config import setup_logging

# логгирование
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
process_logger, error_logger = setup_logging(project_root)

class VideoProcessor(FileProcessor):
    """
    Класс для обработки видеофайлов.

    Наследуется:
        FileProcessor: Базовый класс для обработки файлов.

    Методы:
        process(filepath): Обрабатывает видеофайл, извлекая его основные параметры.
    """
    def process(self, filepath):
        """
        Обрабатывает видеофайл и извлекает его параметры: длительность, количество кадров, частота кадров и размеры.

        Args:
            filepath (str): Путь к видеофайлу.

        Returns:
            dict: Словарь с информацией о видеофайле, включая:
                - video_frame_count (int): Количество кадров.
                - video_fps (float): Частота кадров.
                - video_duration (float): Длительность видео в секундах.
                - video_width (int): Ширина видео в пикселях.
                - video_height (int): Высота видео в пикселях.
                - Любые общие параметры из метода `get_generic_info`.

            В случае ошибки возвращает словарь с ключом "error" и описанием ошибки.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            video = cv2.VideoCapture(filepath)
            duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = video.get(cv2.CAP_PROP_FPS)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            file_info.update({
                "video_frame_count": frame_count,
                "video_fps": fps,
                "video_duration": duration,
                "video_width": width,
                "video_height": height,
            })

            elapsed_time = time.time() - start_time
            process_logger.info(f"Video processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing video {filepath}: {e}")
            return {"error": str(e)}



class VideoProcessorWeb(FileProcessor):
    """
    Класс для обработки видеофайлов в веб-приложении.

    Наследуется:
        FileProcessor: Базовый класс для обработки файлов.

    Методы:
        process(filepath): Обрабатывает видеофайл, извлекая его основные параметры.
    """
    def process(self, filepath):
        """
        Обрабатывает видеофайл и извлекает его параметры: длительность, количество кадров, частота кадров и размеры.

        Args:
            filepath (str): Путь к видеофайлу.

        Returns:
            dict: Словарь с информацией о видеофайле, включая:
                - video_frame_count (int): Количество кадров.
                - video_fps (float): Частота кадров.
                - video_duration (float): Длительность видео в секундах.
                - video_width (int): Ширина видео в пикселях.
                - video_height (int): Высота видео в пикселях.
                - Любые общие параметры из метода `get_generic_info`.

            В случае ошибки возвращает словарь с ключом "error" и описанием ошибки.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            video = cv2.VideoCapture(filepath)
            duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = video.get(cv2.CAP_PROP_FPS)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            file_info.update({
                "video_frame_count": frame_count,
                "video_fps": fps,
                "video_duration": duration,
                "video_width": width,
                "video_height": height,
            })

            elapsed_time = time.time() - start_time
            process_logger.info(f"Video processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing video {filepath}: {e}")
            return {"error": str(e)}
