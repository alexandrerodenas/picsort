import logging
from abc import ABCMeta, abstractmethod

import cv2
import numpy as np
from pytesseract import pytesseract


class ImageAnalyzer(metaclass=ABCMeta):
    @abstractmethod
    def get_white_percentage(self, image_content) -> int:
        pass

    @abstractmethod
    def get_blur_level(self, image_content) -> int:
        pass

    @abstractmethod
    def get_text(self, image_content):
        pass


class SimpleAnalyzer(ImageAnalyzer):
    def __init__(self, blurriness_threshold, tesseract_path):
        self.blurriness_threshold = blurriness_threshold
        self.tesseract_path = tesseract_path

    def get_white_percentage(self, image_grayscale):
        logging.debug("Computing percentage of white")
        n_white_pix = np.sum(image_grayscale == 255)
        return int((n_white_pix / image_grayscale.size) * 100)

    def get_blur_level(self, image_grayscale):
        try:
            laplacian_var = cv2.Laplacian(image_grayscale, cv2.CV_64F).var()
            return int(laplacian_var)
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")

    def get_text(self, image_content):
        pytesseract.tesseract_cmd = self.tesseract_path
        return pytesseract.image_to_string(image_content).encode("unicode_escape").decode("utf-8")
