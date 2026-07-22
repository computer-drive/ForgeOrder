import logging

max_name_length = 0
max_level_length = 0

class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        global max_level_length, max_name_length

        if len(record.levelname) > max_level_length:
            max_level_length = len(record.levelname)

        record.levelname = record.levelname.lower().ljust(max_level_length)

        if len(record.name) > max_name_length:
            max_name_length = len(record.name)

        record.name = record.name.ljust(max_name_length)

        record.reset = '\033[0m'


        match record.levelname.strip():
            case 'info':
                record.color = ''
                record.levelname = f'\033[34m{record.levelname}\033[0m'
            case 'warning':
                record.color = '\033[33m'
            case 'error':
                record.color = '\033[31m'
            case _:
                record.color = ''
            

        return super().format(record)



def get_console_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()

        console_handler.setLevel(logging.INFO)
        formatter = Formatter("%(color)s%(name)s %(levelname)s %(message)s%(reset)s")
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger

