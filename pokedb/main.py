import os
import logging
from datetime import datetime
from module.module import Module


def setup_logging(logging_level=logging.DEBUG):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)

    # Set up a stream handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s:%(lineno)s %(levelname)s p:%(processName)s t:%(threadName)s: %(message)s"
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    log_directory = "./logs"
    os.makedirs(log_directory, exist_ok=True)

    # Set up a file handler to log to a file with name based on the date
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_directory, f"{current_date}.log")
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def main():
    setup_logging()

    m = Module()
    m.do_stuff()
    logging.info("Log in main")


if __name__ == "__main__":
    main()
