
import logging
from tkinter.scrolledtext import ScrolledText


class TextHandler(logging.Handler):
    """ A logging handler that outputs logs to a Tkinter Text widget and a file. """
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        # Safely append to text widget
        if self.text_widget.winfo_exists():  # Check if widget still exists
            self.text_widget.config(state='normal')
            self.text_widget.insert('end', msg + '\n')
            self.text_widget.config(state='disabled')
            self.text_widget.yview('end')

def setup_logging(text_widget):
    logger = logging.getLogger('AppLogger')
    logger.setLevel(logging.DEBUG)

    # Ensure the logger has no other handlers configured previously
    if not logger.handlers:
        # Create and configure text handler
        text_handler = TextHandler(text_widget)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        text_handler.setFormatter(formatter)
        logger.addHandler(text_handler)

        # Create and configure file handler
        file_handler = logging.FileHandler('application.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
