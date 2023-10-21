import logging
import os

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


def load_images(image_dir):
    logging.info(f"Loading images")
    image_list = []

    for root, _, files in os.walk(image_dir):
        logging.debug(f"Analysing {files}")
        for image_file in files:
            if image_file.lower().endswith(IMAGE_EXTENSIONS):
                image_path = os.path.join(root, image_file)
                image_list.append(image_path)

    logging.info(f"Found {len(image_list)} images")
    return image_list
