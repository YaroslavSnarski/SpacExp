# audio_processor.py
import time
import os
from mutagen import File as MutagenFile 
from .base_processor import FileProcessor
from .logging_config import setup_logging

# Настраиваем логгирование
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
process_logger, error_logger = setup_logging(project_root)

class BaseAudioProcessor(FileProcessor):
    """
    Класс для обработки аудиофайлов, извлечения метаданных: продолжительность, теги, битрейт и частота дискретизации.

    Наследует класс FileProcessor и реализует метод process для обработки аудиофайлов.
    """
    def __init__(self):
        """
        Инициализация экземпляра AudioProcessor и создание множества для отслеживания уникальных ключей тегов.
        """
        # множество для отслеживания всех уникальных ключей тегов
        self.all_tag_keys = set()

    def process_audio_file(self, filepath, is_web=False):
        """
        Обрабатывает указанный аудиофайл, извлекая метаданные: продолжительность, теги, битрейт и частоту дискретизации.

        Аргументы:
            filepath (str): Путь к аудиофайлу, который необходимо обработать.

        Возвращает:
            dict: Словарь, содержащий метаданные аудиофайла, включая:
                  - 'audio_duration': Продолжительность аудиофайла.
                  - 'audio_tags': Словарь с тегами аудиофайла.
                  - 'audio_bitrate': Битрейт аудиофайла.
                  - 'audio_sample_rate': Частота дискретизации аудиофайла.
                  - Другие общие данные о файле, полученные из родительского класса.

                  Если возникает ошибка, возвращается словарь с сообщением об ошибке.
        """
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            # Mutagen для получения информации об аудио
            audio = MutagenFile(filepath)
            duration = audio.info.length if audio and audio.info else "N/A"
            tags = audio.tags if audio and audio.tags else {}
            audio_bitrate = audio.info.bitrate if hasattr(audio.info, 'bitrate') else "N/A"
            audio_sample_rate = audio.info.sample_rate if hasattr(audio.info, 'sample_rate') else "N/A"

            # сериализуем теги
            tags_serializable = {key: str(value) for key, value in tags.items()} if is_web else tags

            file_info.update({
                "audio_duration": duration,
                "audio_tags": tags_serializable,
                "audio_bitrate": audio_bitrate,
                "audio_sample_rate": audio_sample_rate,
            })

            # адпейтим множество всех ключей тегов
            self.all_tag_keys.update(tags.keys())

            # добавляем каждый ключ-значение тега в file_info с префиксом "tags_"
            for key, value in tags_serializable.items():
                file_info[f"tags_{key}"] = value

            # уникальные поля для веб-версии
            if is_web:
                file_info["type"] = "audio"

            elapsed_time = time.time() - start_time
            process_logger.info(f"Audio processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_info = {"error": str(e)}
            if is_web:
                error_info["type"] = "audio"
            error_logger.error(f"Error processing audio {filepath}: {e}")
            return error_info


class AudioProcessor(BaseAudioProcessor):
    def process(self, filepath):
        """Процессор для стандартной обработки аудио."""
        return self.process_audio_file(filepath, is_web=False)


class AudioProcessorWeb(BaseAudioProcessor):
    """
    Класс для обработки аудиофайлов для веб-приложений, извлекающий метаданные: продолжительность, теги, битрейт,
    частота дискретизации и сериализуя значения тегов для совместимости с веб-форматами.

    Наследует класс FileProcessor и реализует метод process для обработки аудиофайлов в контексте веб-приложений.
    """
    def process(self, filepath):
        """
        Обрабатывает указанный аудиофайл, извлекая метаданные: продолжительность, теги, битрейт и частоту дискретизации,
        а также сериализует значения тегов для совместимости с веб-форматами.

        Аргументы:
            filepath (str): Путь к аудиофайлу, который необходимо обработать.

        Возвращает:
            dict: Словарь, содержащий метаданные аудиофайла, включая:
                  - 'type': Тип файла, который равен "audio".
                  - 'audio_duration': Продолжительность аудиофайла.
                  - 'audio_tags': Словарь с сериализованными тегами аудиофайла.
                  - 'audio_bitrate': Битрейт аудиофайла.
                  - 'audio_sample_rate': Частота дискретизации аудиофайла.
                  - Другие общие данные о файле, полученные из родительского класса.

                  Если возникает ошибка, возвращается словарь с сообщением об ошибке и типом файла.
        """
        return self.process_audio_file(filepath, is_web=True)
