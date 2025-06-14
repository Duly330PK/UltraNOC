import logging

logger = logging.getLogger("ultranoc")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

def get_logger():
    return logger
