import logging

import cv2
import numpy as np


def _is_mostly_white(image_path, threshold=80):
    image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
    n_white_pix = np.sum(image == 255)
    white_percentage = (n_white_pix / image.size) * 100
    return white_percentage >= threshold


def filtering_mostly_white_images(images_to_sort):
    logging.info("Filtering mostly white images")
    mostly_white_images = []
    for image_file in images_to_sort:
        if _is_mostly_white(image_file):
            mostly_white_images.append(image_file)
    logging.info(f"Found {len(mostly_white_images)} images")
    return mostly_white_images
