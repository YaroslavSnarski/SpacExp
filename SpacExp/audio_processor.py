# audio_processor.py
import time
import logging
from mutagen import File as MutagenFile 
from .base_processor import FileProcessor

class AudioProcessor(FileProcessor):
    def __init__(self):
        # initialising a set to keep track of all unique tag keys
        self.all_tag_keys = set()
    def process(self, filepath):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            # using Mutagen to get info on audio
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
            # updating the set of all tag keys
            self.all_tag_keys.update(tags.keys())

            # adding each tag key-value pair to file_info with "tags_" prefix
            for key, value in tags.items():
                file_info[f"tags_{key}"] = value

            elapsed_time = time.time() - start_time
            logging.info(f"Audio processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            logging.error(f"Error processing audio {filepath}: {e}")
            return {"error": str(e)}

class AudioProcessorWeb(FileProcessor):
    def __init__(self):
        # a set to keep track of all unique tag keys
        self.all_tag_keys = set()

    def process(self, filepath):
        try:
            start_time = time.time()
            file_info = self.get_generic_info(filepath)

            audio = MutagenFile(filepath)
            duration = audio.info.length if audio and audio.info else "N/A"
            tags = audio.tags if audio and audio.tags else {}
            audio_bitrate = audio.info.bitrate if hasattr(audio.info, 'bitrate') else "N/A"
            audio_sample_rate = audio.info.sample_rate if hasattr(audio.info, 'sample_rate') else "N/A"

            # serialising tags
            tags_serializable = {key: str(value) for key, value in tags.items()}

            file_info.update({
                "type": "audio", 
                "audio_duration": duration,
                "audio_tags": tags_serializable,
                "audio_bitrate": audio_bitrate,
                "audio_sample_rate": audio_sample_rate,
            })
            self.all_tag_keys.update(tags.keys())

            # adding each tag key-value pair to file_info with "tags_" prefix
            for key, value in tags_serializable.items():
                file_info[f"tags_{key}"] = value

            elapsed_time = time.time() - start_time
            logging.info(f"Audio processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            logging.error(f"Error processing audio {filepath}: {e}")
            return {"type": "audio", "error": str(e)}  # Устанавливаем тип даже при ошибке

