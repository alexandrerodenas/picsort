import logging
import os
from typing import List

import cv2


class ImagesLoader:
    def __init__(self, input_dir: str, image_extensions: List[str]):
        self.input_dir = input_dir
        self.image_extensions = tuple(image_extensions)

    def extract_paths(self):
        logging.info(f"Loading images")
        image_list = []

        for root, _, files in os.walk(self.input_dir):
            logging.debug(f"Analysing {files}")
            for image_file in files:
                if (image_file.lower().endswith(self.image_extensions)
                        and not os.path.basename(image_file).lower().startswith("_")):
                    image_path = os.path.join(root, image_file)
                    image_list.append(image_path)
        return image_list

    @staticmethod
    def _read_image_content(image_path):
        try:
            image_content = cv2.imread(image_path)
            image_grayscale_encoded = cv2.cvtColor(image_content, cv2.COLOR_BGR2GRAY)
            return image_content, image_grayscale_encoded
        except Exception as e:
            logging.error(f"Error loading image {image_path}: {str(e)}")
            return None
