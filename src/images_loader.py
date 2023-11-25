import logging
import os
import cv2
import numpy as np
import pandas as pd

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


class ImageDataLoader:
    def __init__(self, input_dir):
        self.input_dir = input_dir

    def create_image_dataframe(self) -> pd.DataFrame:
        image_list = self._get_images_paths(self.input_dir)
        logging.info(f"Looking over {len(image_list)} images")
        df = pd.DataFrame(columns=['path', 'content'])

        for image_path in image_list:
            image_content, image_grayscale_encoded = self._read_image_content(image_path)
            if image_content is not None or image_grayscale_encoded is not None:
                new_row = {'path': image_path, 'content': image_content, 'grayscale': image_grayscale_encoded}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        logging.info(f"Loaded {len(df)} images into the DataFrame")
        return df

    @staticmethod
    def _get_images_paths(image_dir):
        logging.info(f"Loading images")
        image_list = []

        for root, _, files in os.walk(image_dir):
            logging.debug(f"Analysing {files}")
            for image_file in files:
                if (image_file.lower().endswith(IMAGE_EXTENSIONS)
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
