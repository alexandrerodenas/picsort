import logging
import os
import cv2
import pandas as pd

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


class ImageDataLoader:
    def __init__(self, image_dir):
        self.images_dataframe = self._create_image_dataframe(image_dir)

    def _create_image_dataframe(self, image_dir):
        logging.info(f"Loading images")
        image_list = self._get_images_paths(image_dir)

        # Create an empty DataFrame
        df = pd.DataFrame(columns=['path', 'content'])

        for image_path in image_list:
            image_content = self._load_image_content(image_path)
            if image_content is not None:
                new_row = {'path': image_path, 'content': image_content}
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

        logging.info(f"Found {len(image_list)} images")
        return image_list

    @staticmethod
    def _load_image_content(image_path):
        try:
            # Load the image using OpenCV
            image = cv2.imread(image_path)

            if image is not None:
                # Convert the image to bytes
                image_content = cv2.imencode('.jpg', image)[1].tobytes()
                return image_content
            else:
                logging.error(f"Failed to load image at {image_path}")
                return None
        except Exception as e:
            logging.error(f"Error loading image {image_path}: {str(e)}")
            return None

    def get_dataframe(self):
        return self.images_dataframe
