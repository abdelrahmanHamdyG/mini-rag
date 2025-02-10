import logging
import os

class Logger:
    def __init__(self, log_file: str = "mini_rag.log", log_level: int = logging.DEBUG):
        """
        Custom Logger class to log application-specific messages to a file.

        :param log_file: File where logs will be stored.
        :param log_level: Logging level (default: DEBUG).
        """
        self.logger = logging.getLogger("mini_rag")  # Unique logger name
        self.logger.setLevel(log_level)  # Set log level

        # Prevent Uvicorn logs from propagating to this logger
        self.logger.propagate = False  

        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create file handler (append mode)
        file_handler = logging.FileHandler(log_file, mode="a")

        # Define log format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add the handler only if it's not already added
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def get_logger(self):
        """Return the configured logger instance."""
        return self.logger
