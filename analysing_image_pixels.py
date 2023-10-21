import concurrent.futures
import logging

import cv2
import numpy as np


class PixelAnalysis:

    def __init__(self, images):
        self.white_analysis = self._compute_white_percentage(images)

    @staticmethod
    def _get_white_percentage(image_path):
        image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
        n_white_pix = np.sum(image == 255)
        return (n_white_pix / image.size) * 100

    def _compute_white_percentage(self, images_to_sort):
        logging.info("Computing percentage of white in images")

        def process_image(image_file):
            try:
                return {
                    "image_file": image_file,
                    "white_percentage": self._get_white_percentage(image_file)
                }
            except:
                logging.error(f"An exception occurred with {image_file}")
                return {
                    "image_file": image_file,
                    "white_percentage": None  # Handle exceptions gracefully
                }

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_image, images_to_sort))

        white_analysis = [result for result in results if result["white_percentage"] is not None]

        logging.info("Computing done")
        return white_analysis

    def save_white_analysis_in_file(self, output_file):
        with open(output_file, "w") as result_file:
            for entry in self.white_analysis:
                result_file.write(f"image: {entry['image_file']}, white_percentage: {int(entry['white_percentage'])}\n")
