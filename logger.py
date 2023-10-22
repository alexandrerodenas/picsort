import logging
import sys


def setup_logger(base_level):
    root = logging.getLogger()
    root.setLevel(base_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(base_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
