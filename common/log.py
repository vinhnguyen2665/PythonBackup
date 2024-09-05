import logging
from datetime import datetime


def error(e):
    print(e)
    logging.info(datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")[:-3])
    logging.error(e)


def info(info):
    print(info)
    logging.info(datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")[:-3])
    logging.info(info)
