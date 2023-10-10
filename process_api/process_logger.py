import logging
import io
import os


class ProcessLogger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger("process_api")
        self.log_buffer = io.StringIO()

        self.stream_handler = logging.StreamHandler(self.log_buffer)
        self.stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.stream_handler.setFormatter(formatter)
        self.logger.addHandler(self.stream_handler)
        self.has_error = False
        self.error_count = 0

    def __del__(self):
        self.stream_handler.close()
        self.log_buffer.close()

    def set_level(self, level):
        if level == "debug":
            logging.getLogger().setLevel(logging.DEBUG)
        elif level == "info":
            logging.getLogger().setLevel(logging.INFO)
        elif level == "warning":
            logging.getLogger().setLevel(logging.WARNING)
        elif level == "error":
            logging.getLogger().setLevel(logging.ERROR)
        elif level == "critical":
            logging.getLogger().setLevel(logging.CRITICAL)

    def clear_log(self):
        # Reset the content of the log buffer
        self.log_buffer.truncate(0)
        self.log_buffer.seek(0)
        self.has_error = False
        self.error_count = 0

    def print(self):
        log_content = self.log_buffer.getvalue()
        print(log_content)

    def save_to_file(self, file_name):
        log_content = self.log_buffer.getvalue()

        try:
            directory = os.path.dirname(file_name)

            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_name, 'w') as file:
                file.write(log_content)
            print(f"Log content saved to {file_name}")
        except Exception as e:
            print(f"Error saving log content to {file_name}: {str(e)}")

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        self.has_error = True
        self.error_count += 1

    def critical(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        self.has_error = True
        self.error_count += 1

    def fatal(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
        self.has_error = True
        self.error_count += 1
