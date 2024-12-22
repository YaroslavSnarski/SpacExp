import cv2
from .base_processor import FileProcessor
import logging
import time

error_logger = logging.getLogger('error')
process_logger = logging.getLogger('process')

class VideoProcessor(FileProcessor):
    def process(self, filepath):
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
    def process(self, filepath):
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
