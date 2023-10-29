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

    def get_white_percentage(self, image_content):
        logging.debug("Computing percentage of white")
        image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_GRAYSCALE)
        n_white_pix = np.sum(image == 255)
        return int((n_white_pix / image.size) * 100)

    def get_blur_level(self, image_content):
        try:
            image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_GRAYSCALE)
            laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
            return int(laplacian_var)
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")

    def get_text(self, image_content):
        pytesseract.tesseract_cmd = self.tesseract_path
        return pytesseract.image_to_string(image_content).encode("unicode_escape").decode("utf-8")