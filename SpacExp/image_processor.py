
from PIL import Image, ExifTags
from .base_processor import FileProcessor
import logging
import time

error_logger = logging.getLogger('error')
process_logger = logging.getLogger('process')

class ImageProcessor(FileProcessor):
    def process(self, filepath):
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

            elapsed_time = time.time() - start_time
            process_logger.info(f"Image processed: {filepath} in {elapsed_time:.2f} seconds")

            return file_info
        except Exception as e:
            error_logger.error(f"Error processing image {filepath}: {e}")
            return {"error": str(e)}
