import logging

import cv2
import numpy as np
from pytesseract import pytesseract

from src.pre_analysis.image_analysis import ImagePreAnalysis


class PreAnalyzer:
    def __init__(self, tesseract_path):
        self.tesseract_path = tesseract_path

    def run(self, row) -> ImagePreAnalysis:
        image_pre_analysis = ImagePreAnalysis(
            row["path"],
            self._get_blur_level(row["grayscale"]),
            self._get_white_percentage(row["grayscale"]),
            self._get_text(row["content"])
        )
        return image_pre_analysis

    @staticmethod
    def _get_white_percentage(image_grayscale):
        logging.debug("Computing percentage of white")
        n_white_pix = np.sum(image_grayscale == 255)
        return int((n_white_pix / image_grayscale.size) * 100)

    @staticmethod
    def _get_blur_level(image_grayscale):
        try:
            laplacian_var = cv2.Laplacian(image_grayscale, cv2.CV_64F).var()
            return int(laplacian_var)
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")

    def _get_text(self, image_content) -> str:
        pytesseract.tesseract_cmd = self.tesseract_path
        return pytesseract.image_to_string(image_content).encode("unicode_escape").decode("utf-8")
