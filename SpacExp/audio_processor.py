
# audio_processor.py

import os
import time
import logging
from mutagen import File as MutagenFile  # Импорт библиотеки Mutagen
from .base_processor import FileProcessor  # Use absolute import

class AudioProcessor(FileProcessor):
    def __init__(self):
        # Initialize a set to keep track of all unique tag keys
        self.all_tag_keys = set()
    def process(self, filepath):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            # Используем библиотеку Mutagen для получения информации о аудио
            audio = MutagenFile(filepath)
            duration = audio.info.length if audio and audio.info else "N/A"
            tags = audio.tags if audio and audio.tags else {}
            audio_bitrate = audio.info.bitrate if hasattr(audio.info, 'bitrate') else "N/A"
            audio_sample_rate = audio.info.sample_rate if hasattr(audio.info, 'sample_rate') else "N/A"

            file_info.update({
                "audio_duration": duration,
                "audio_tags": tags,
                "audio_bitrate": audio_bitrate,
                "audio_sample_rate": audio_sample_rate,
            })
            # Update the set of all tag keys encountered
            self.all_tag_keys.update(tags.keys())

            # Add each tag key-value pair to file_info with "tags_" prefix
            for key, value in tags.items():
                file_info[f"tags_{key}"] = value

            elapsed_time = time.time() - start_time
            logging.info(f"Audio processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            logging.error(f"Error processing audio {filepath}: {e}")
            return {"error": str(e)}

