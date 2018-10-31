# -*- coding: utf-8 -*-

import logging


def get_logger(log_level=logging.INFO):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
    logger = logging.getLogger("siren")
    logger.setLevel(log_level)
    return logger
