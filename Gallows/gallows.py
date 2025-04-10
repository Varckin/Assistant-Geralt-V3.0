from Logging.logger import get_logger
from random import choice
import os


logger = get_logger(__name__)


class Gallows():
    def __init__(self):
        self.tries: int = 8
    
    def list_words(self) -> list:
        try:
            with open(os.getenv('GALLOWS_PATH'), 'r', encoding='utf-8') as file:
                list_words: list = file.read().split()
                return list_words
        except FileNotFoundError as e:
            logger.error(f'File not found: {e}')
        except PermissionError as e:
            logger.error(f'No permission: {e}')

    def gif_load(self) -> str:
        try:
            return os.getenv('GALLOWS_LOSE_PATH')
        except ValueError as e:
            logger.error(f'Value error: {e}')
    
    def choice_word(self) -> str:
        return choice(self.list_words()).lower()
