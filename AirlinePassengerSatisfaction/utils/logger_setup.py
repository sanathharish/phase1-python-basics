import logging
import os

def setup_logger(log_file="Logs/data_processing.log", log_levels=None):
    """
    Set up a logger that writes to Logs/ directory.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    if log_levels is None:
        log_levels = ["INFO", "ERROR"]

    logger = logging.getLogger("DataProcessingLogger")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Filter logs based on selected levels
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }

    if "ALL" in log_levels:
        selected_levels = list(level_map.values())
    else:
        selected_levels = [level_map[l] for l in log_levels if l in level_map]

    class MultiLevelFilter(logging.Filter):
        def filter(self, record):
            return record.levelno in selected_levels

    file_handler.addFilter(MultiLevelFilter())
    logger.addHandler(file_handler)

    print(f"📜 Logging active — Levels: {', '.join(log_levels)} | File: {log_file}")
    return logger
