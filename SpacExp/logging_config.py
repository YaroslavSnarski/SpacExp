# logging_config.py
import logging
import os

def setup_logging(project_root):
    """Настраивает логирование."""
    log_file = os.path.join(project_root, 'file_analyzer.log')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Логгер для ошибок
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)

    # Логгер для процесса
    process_logger = logging.getLogger('process')
    process_logger.setLevel(logging.INFO)

    return process_logger, error_logger
