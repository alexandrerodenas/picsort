import logging

import cv2
import numpy as np
from pytesseract import pytesseract


class PreAnalyzer:

    @staticmethod
    def get_white_percentage(image_grayscale):
        logging.debug("Computing percentage of white")
        n_white_pix = np.sum(image_grayscale == 255)
        return int((n_white_pix / image_grayscale.size) * 100)

    @staticmethod
    def get_blur_level(image_grayscale):
        try:
            laplacian_var = cv2.Laplacian(image_grayscale, cv2.CV_64F).var()
            return int(laplacian_var)
        except Exception as e:
            logging.error(f"Error analyzing image: {str(e)}")

    @staticmethod
    def get_text(image_content, tesseract_path) -> str:
        pytesseract.tesseract_cmd = tesseract_path
        return pytesseract.image_to_string(image_content).encode("unicode_escape").decode("utf-8")
