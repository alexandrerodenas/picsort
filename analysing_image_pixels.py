import logging

import cv2
import numpy as np


def _get_white_percentage(image_path):
    image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
    n_white_pix = np.sum(image == 255)
    return (n_white_pix / image.size) * 100


def compute_white_percentage(images_to_sort):
    logging.info("Computing percentage of white in images")
    images = []
    for image_file in images_to_sort:
        images.append({
            "image_file": image_file,
            "white_percentage": _get_white_percentage(image_file)
        })
    logging.info("Computing done")
    return images


def save_in_file(analysis, output_file):
    with open(output_file, "w") as result_file:
        for entry in analysis:
            result_file.write(f"image: {entry['image_file']}, white_percentage: {entry['white_percentage']}\n")

