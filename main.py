import logging
import time

from images_loader import load_images
from inference import classify_image
from logger import setup_logger

if __name__ == '__main__':
    setup_logger()

    image_dir = 'sauvegarde_alex'
    output_file = 'classification_results.txt'

    images_to_sort = load_images(image_dir)

    logging.info(f"Inference starting")

    with open(output_file, "w") as result_file:
        for image_file in images_to_sort:
            logging.debug(f"Inference on {image_file}")
            predicted_class = classify_image(image_file)
            result_file.write(f"Image: {image_file}, class: {predicted_class}\n")

    logging.info(f"Inference over")
